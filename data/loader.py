#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: loader.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:25:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

import json

from django.contrib.auth.models import User

from apps.blog_app.models import BlogTag, BlogPost
from apps.community_forum.models import ForumCategory, ForumThread
from auth.models import Profile
from .path_consts import DataPaths


class BoilerplateDataLoader:

    @staticmethod
    def load():
        try:
            BoilerplateDataLoader._load_forum_data()
            print("[BoilerplateDataLoader.load_forum_data] Forum data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_forum_data] Error while loading forum data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_blog_data()
            print("[BoilerplateDataLoader.load_blog_data] Blog data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_blog_data] Error while loading blog data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_functions_data()
            print("[BoilerplateDataLoader.load_functions_data] Functions data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_functions_data] Error while loading functions data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_apis_data()
            print("[BoilerplateDataLoader.load_apis_data] APIs data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_apis_data] Error while loading APIs data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_scripts_data()
            print("[BoilerplateDataLoader.load_scripts_data] Scripts data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_scripts_data] Error while loading scripts data: {e}")
        ####
        try:
            BoilerplateDataLoader._load_knowledge_bases_data()
            print("[BoilerplateDataLoader.load_knowledge_bases_data] Knowledge bases data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_knowledge_bases_data] Error while loading knowledge bases data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_assistant_integrations_data()
            print("[BoilerplateDataLoader.load_assistant_integrations_data] Assistant integrations data "
                  "loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_assistant_integrations_data] Error while loading assistant "
                  f"integrations data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_orchestration_meta_integrations_data()
            print("[BoilerplateDataLoader.load_orchestration_meta_integrations_data] Orchestration meta integrations "
                  "data loaded successfully")
        except Exception as e:
            print(f"[BoilerplateDataLoader.load_orchestration_meta_integrations_data] Error while loading "
                  f"orchestration meta integrations data: {e}")
        #####

    @staticmethod
    def _load_forum_data():
        categories_data_path = DataPaths.Forum.CATEGORIES
        threads_data_path = DataPaths.Forum.THREADS

        # Load categories
        categories_data_json = None
        with open(categories_data_path, "r") as categories_file:
            categories_data_json = json.load(categories_file)
            for c in categories_data_json:
                c_name = c["name"]
                _ = ForumCategory.objects.get_or_create(
                    name=c_name,
                    defaults={
                        **c
                    }
                )
            print(f"[BoilerplateDataLoader._load_forum_data] Pre-loaded {len(categories_data_json)} categories")

        # Load threads
        threads_data_json = None
        with open(threads_data_path, "r") as threads_file:
            threads_data_json = json.load(threads_file)
            for t in threads_data_json:
                t_title = t["title"]
                t_category_name = t["category"]
                t_category_object = ForumCategory.objects.get(name=t_category_name)
                _ = ForumThread.objects.get_or_create(
                    title=t_title,
                    category=t_category_object
                )
            print(f"[BoilerplateDataLoader._load_forum_data] Pre-loaded {len(threads_data_json)} threads")
        return

    @staticmethod
    def _load_blog_data():
        blogs_data_path = DataPaths.Blog.BLOGS

        blogs_data_json = None
        with open(blogs_data_path, "r") as blogs_file:
            blogs_data_json = json.load(blogs_file)
            for b in blogs_data_json:
                b_title = b["title"]
                b_slug = b["slug"]
                b_content = b["content"]
                b_thumbnail_image = b["thumbnail_image"]
                b_status = b["status"]

                b_author_name = b["author"]
                b_author_object = User.objects.get(username=b_author_name)

                b_tags_unstructured = b["tags"]
                b_tag_objects = []
                for t in b_tags_unstructured:
                    t_name = t["name"]
                    t_slug = t["slug"]
                    t, _ = BlogTag.objects.get_or_create(
                        name=t_name,
                        slug=t_slug
                    )
                    b_tag_objects.append(t)

                b_new, created_now = BlogPost.objects.get_or_create(
                    title=b_title,
                    slug=b_slug,
                    defaults={
                        "author": b_author_object,
                        "content": b_content,
                        "thumbnail_image": b_thumbnail_image,
                        "status": b_status
                    }
                )
                if created_now:
                    b_new.tags.set(b_tag_objects)
            print(f"[BoilerplateDataLoader._load_blog_data] Pre-loaded {len(blogs_data_json)} blog posts")
        return

    @staticmethod
    def _load_functions_data():
        functions_data_path = DataPaths.Functions.FUNCTIONS
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        return

    @staticmethod
    def _load_apis_data():
        apis_data_path = DataPaths.APIs.APIs
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        return

    @staticmethod
    def _load_scripts_data():
        scripts_data_path = DataPaths.Scripts.SCRIPTS
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        pass

    @staticmethod
    def _load_knowledge_bases_data():
        knowledge_bases_data_path = DataPaths.KnowledgeBases.KNOWLEDGE_BASES
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        return

    @staticmethod
    def _load_assistant_integrations_data():
        assistant_integrations_data_path = DataPaths.AssistantIntegrations.ASSISTANT_INTEGRATIONS
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        return

    @staticmethod
    def _load_orchestration_meta_integrations_data():
        orchestration_meta_integrations_data_path = DataPaths.OrchestrationMetaIntegrations.ORCHESTRATION_META_INTEGRATIONS
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        return
