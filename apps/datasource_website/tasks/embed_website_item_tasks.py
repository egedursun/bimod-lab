#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: embed_website_item_tasks.py
#  Last Modified: 2024-12-07 19:49:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:49:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging
import os
from typing import List, Dict
import xml.etree.ElementTree as ET

import faiss
import numpy as np
import requests
from bs4 import BeautifulSoup

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from apps.datasource_website.models import (
    DataSourceWebsiteStorageItem,
    WebsiteItemChunkVectorData,
    DataSourceWebsiteStorageConnection
)

from apps.datasource_website.utils import (
    WebsiteIndexingMethodologyChoicesNames,
    VECTOR_INDEX_PATH_WEBSITE_ITEMS,
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

logger = logging.getLogger(__name__)


def _generate_embedding(vector, raw_data):
    from apps.core.generative_ai.gpt_openai_manager import (
        OpenAIGPTClientManager
    )

    vector: WebsiteItemChunkVectorData

    c = OpenAIGPTClientManager.get_naked_client(
        llm_model=vector.website_item.storage.assistant.llm_model
    )

    raw_data_text = json.dumps(raw_data, indent=2)

    try:

        if vector.website_item.storage.vectorizer == "text2vec-openai":

            response = c.embeddings.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
            )

            embedding_vector = response.data[0].embedding
            vector.vector_data = embedding_vector

        else:
            logger.error(f"Invalid vectorizer type: {vector.website_item.storage.vectorizer}")
            raise Exception("Invalid vectorizer type.")

    except Exception as e:
        logger.error(f"Error in generating embedding: {e}")
        vector.vector_data = []

    vector.raw_data = raw_data
    vector.save()


def _save_embedding(vector, index_path):
    if vector.vector_data:
        x = np.array(
            [vector.vector_data],
            dtype=np.float32
        ).reshape(
            1,
            OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
        )

        xids = np.array([vector.id], dtype=np.int64)

        if not os.path.exists(index_path):
            index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

        else:
            index = faiss.read_index(index_path)
            if not isinstance(index, faiss.IndexIDMap):
                index = faiss.IndexIDMap(index)
            index.remove_ids(xids)

        index.add_with_ids(x, xids)

        faiss.write_index(index, index_path)


def handle_embedding_task(
    vector_id: int,
    raw_data: dict,
):
    vector: WebsiteItemChunkVectorData = WebsiteItemChunkVectorData.objects.get(
        id=vector_id
    )

    storage_id = vector.website_item.storage.id
    index_path = os.path.join(
        VECTOR_INDEX_PATH_WEBSITE_ITEMS,
        f'website_storage_index_{storage_id}.index'
    )

    if not vector:
        logger.error(f"Vector not found with ID: {vector}")
        return False

    _generate_embedding(
        vector=vector,
        raw_data=raw_data
    )

    _save_embedding(
        vector=vector,
        index_path=index_path
    )


def clean_previous_data(item: DataSourceWebsiteStorageItem) -> bool:
    try:

        # Restore item count
        item.n_chunks_indexed_status = 0
        item.n_chunks = 0
        item.save()

        # Determine the index file path
        storage = item.storage
        storage: DataSourceWebsiteStorageConnection
        storage_id = storage.id

        index_path = os.path.join(
            VECTOR_INDEX_PATH_WEBSITE_ITEMS,
            f'website_storage_index_{storage_id}.index'
        )

        # Remove previous vector ORM objects
        previous_vectors = WebsiteItemChunkVectorData.objects.filter(
            website_item=item
        )

        if not previous_vectors.exists():
            logger.info(f"No previous vector data found for website item with ID: {item.id}, skipping...")

        else:
            # Collect vector IDs to remove from FAISS
            vector_ids = list(
                previous_vectors.values_list(
                    'id',
                    flat=True
                )
            )

            # Delete vector ORM objects
            previous_vectors.delete()

            logger.info(f"Deleted {len(vector_ids)} previous vector ORM objects for website item with ID: {item.id}")

            # Clean vectors from FAISS index
            if os.path.exists(index_path):

                index = faiss.read_index(index_path)

                if not isinstance(index, faiss.IndexIDMap):
                    index = faiss.IndexIDMap(index)

                # Remove IDs from the FAISS index
                xids = np.array(vector_ids, dtype=np.int64)
                index.remove_ids(xids)

                # Save the updated FAISS index back to the file
                faiss.write_index(index, index_path)

                logger.info(f"Removed vectors with IDs {vector_ids} from FAISS index for website item {item.id}.")

            else:
                logger.info(f"FAISS index file not found at {index_path}, nothing to clean...")

        logger.info(f"Successfully cleaned the previous data for website item with ID: {item.id}.")
        return True

    except Exception as e:

        logger.error(f"An error occurred while cleaning the previous data for website item with ID: {item.id}: {e}")
        return False


def _crawl(item: DataSourceWebsiteStorageItem, fetch_text_only: bool = False) -> dict:
    item: DataSourceWebsiteStorageItem

    def discover_sitemap(base_url: str) -> str:
        robots_url = f"{base_url}/robots.txt"
        try:
            response = requests.get(robots_url, timeout=10)
            response.raise_for_status()

            for line in response.text.splitlines():
                if line.lower().startswith("sitemap:"):
                    return line.split(":", 1)[1].strip()
        except Exception as e:
            logger.warning(f"Failed to fetch robots.txt: {e}")

        return f"{base_url}/sitemap.xml"

    def fetch_sitemap(url: str) -> List[str]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            sitemap_urls = []

            if 'xml' in response.headers['Content-Type']:
                root = ET.fromstring(response.text)
                for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    sitemap_urls.append(loc.text)
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    sitemap_urls.append(link['href'])

            return sitemap_urls
        except Exception as e:
            logger.error(f"Error fetching sitemap: {e}")
            return []

    def fetch_page_content(url: str) -> Dict:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            if fetch_text_only:
                for element in soup(['script', 'style']):
                    element.decompose()
                content = soup.get_text(separator='\n', strip=True)
            else:
                content = str(soup)

            title = soup.title.string if soup.title else "No Title"

            return {
                "url": url,
                "title": title,
                "content": content,
                "length": len(content),
            }

        except Exception as e:

            logger.warning(f"Failed to fetch page {url}: {e}")

            return None

    logger.info(f"Starting to crawl website with ID: {item.id}")

    # Discover sitemap URL
    sitemap_url = discover_sitemap(item.website_url)
    logger.info(f"Discovered sitemap URL: {sitemap_url}")

    # Fetch and parse the sitemap
    sitemap_pages = fetch_sitemap(sitemap_url)

    # Update the 'sitemap' field of the item
    item.sitemap_content = sitemap_pages
    item.save()

    logger.info(f"Retrieved {len(sitemap_pages)} URLs from the sitemap.")

    # Limit pages to maximum allowed
    relevant_pages = sitemap_pages[:item.storage.maximum_pages_to_index]

    extracted_content = []

    # Crawl and process pages
    for index, page_url in enumerate(relevant_pages):

        logger.info(f"Processing page {index + 1}/{len(relevant_pages)}: {page_url}")

        page_data = fetch_page_content(page_url)

        if page_data:
            extracted_content.append(page_data)

    logger.info(f"Successfully crawled {len(extracted_content)} pages for item ID: {item.id}")

    # Return extracted content
    return {
        "item_id": item.id,
        "total_pages_crawled": len(extracted_content),
        "pages": extracted_content,
    }


def crawl_and_index_website_item(item_id: int, delete_previous=False) -> bool:
    logger.info(f"Crawling and indexing website item with ID: {item_id}")

    item: DataSourceWebsiteStorageItem = DataSourceWebsiteStorageItem.objects.get(
        id=item_id
    )

    if not item:
        logger.error(f"The website item with ID: {item_id} does not exist.")
        return False

    if delete_previous:
        try:
            success = clean_previous_data(item=item)

            if success is False:
                logger.error(f"An error occurred while cleaning the previous data for website item with ID: {item_id}")

                return False

        except Exception as e:
            logger.error(
                f"An error occurred while cleaning the previous data for website item with ID: {item_id}, {e}")

            return False

    fetch_text_only = None

    if item.crawling_methodology == WebsiteIndexingMethodologyChoicesNames.TEXT_CONTENT:
        fetch_text_only = True

    elif item.crawling_methodology == WebsiteIndexingMethodologyChoicesNames.HTML_CONTENT:
        fetch_text_only = False

    complete_content = _crawl(item, fetch_text_only=fetch_text_only)

    print("The complete content for website URL: ", item.website_url,
          " has been retrieved successfully, for storage: ", item.storage.id, " and related assistant: ",
          item.storage.assistant.id)

    # Convert the content to string.
    complete_content_string = json.dumps(complete_content, indent=2)

    # Split it into multiple chunks
    splitter = RecursiveCharacterTextSplitter(
        complete_content_string,
        chunk_size=item.storage.embedding_chunk_size,
        chunk_overlap=item.storage.embedding_chunk_overlap
    )

    chunks = splitter.split_text(complete_content_string)

    # Learn the total number of chunks
    item.n_chunks = int(len(chunks))
    item.save()

    # Embed each chunk into the vector space
    try:
        for i, chunk in enumerate(chunks):

            try:

                chunk_vector_data = WebsiteItemChunkVectorData.objects.create(
                    website_item=item,
                    raw_data=chunk,
                )

                ##############################
                # Save the Index to Vector DB
                ##############################

                handle_embedding_task(
                    vector_id=chunk_vector_data.id,
                    raw_data=chunk_vector_data.raw_data,
                )

                ##############################

                item.n_chunks_indexed_status = int(int(item.n_chunks_indexed_status) + 1)
                item.save()

            except Exception as e:
                logger.error(f"An error occurred while embedding chunk {i + 1}/{len(chunks)}: {e}")
                continue

    except Exception as e:
        logger.error(f"An error occurred while embedding chunk {i + 1}/{len(chunks)}: {e}")
        return False

    logger.info(f"Successfully updated the vector embeddings for WebsiteItem with ID {item.id}.")
    logger.info("All chunks have been embedded successfully.")
    return True
