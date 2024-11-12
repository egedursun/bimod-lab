#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from django.contrib.auth.models import User

from apps.blog_app.models import BlogTag, BlogPost
from apps.community_forum.models import ForumCategory, ForumThread
from apps.bmd_academy.models import AcademyCourse, AcademyCourseVideo, AcademyCourseSection, AcademyCourseInstructor
from apps.integrations.models import AssistantIntegrationCategory, AssistantIntegration
from apps.meta_integrations.models import MetaIntegrationTeam, MetaIntegrationCategory
from apps.semantor.models import IntegrationVectorData
from config.settings import SKIP_FIXTURE_EMBEDDINGS
from .path_consts import DataPaths

logger = logging.getLogger(__name__)


class BoilerplateDataLoader:

    @staticmethod
    def load():
        try:
            BoilerplateDataLoader._load_forum_data()
            # print("[BoilerplateDataLoader.load_forum_data] Forum data loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_forum_data] Error while loading forum data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_blog_data()
            # print("[BoilerplateDataLoader.load_blog_data] Blog data loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_blog_data] Error while loading blog data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_academy_data()
            # print("[BoilerplateDataLoader.load_academy_data] Academy data loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_academy_data] Error while loading academy data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_functions_data()
            # print("[BoilerplateDataLoader.load_functions_data] Functions data loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_functions_data] Error while loading functions data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_apis_data()
            # print("[BoilerplateDataLoader.load_apis_data] APIs data loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_apis_data] Error while loading APIs data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_scripts_data()
            # print("[BoilerplateDataLoader.load_scripts_data] Scripts data loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_scripts_data] Error while loading scripts data: {e}")
        ####
        try:
            BoilerplateDataLoader._load_knowledge_bases_data()
            # print("[BoilerplateDataLoader.load_knowledge_bases_data] Knowledge bases data loaded successfully")
        except Exception as e:
            logger.error(
                f"[BoilerplateDataLoader.load_knowledge_bases_data] Error while loading knowledge bases data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_ml_models_data()
            # print("[BoilerplateDataLoader.load_ml_models_data] ML models data loaded successfully")
        except Exception as e:
            logger.error(
                f"[BoilerplateDataLoader.load_ml_models_data] Error while loading ML models data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_assistant_integrations_data()
            # print("[BoilerplateDataLoader.load_assistant_integrations_data] Assistant integrations data "
            #      "loaded successfully")
        except Exception as e:
            logger.error(f"[BoilerplateDataLoader.load_assistant_integrations_data] Error while loading assistant "
                         f"integrations data: {e}")
        #####
        try:
            BoilerplateDataLoader._load_categories_and_teams_meta_integrations_data()
            # print("[BoilerplateDataLoader.load_categories_and_teams_meta_integrations_data] Categories and teams "
            #      "integrations data loaded successfully")
        except Exception as e:
            logger.error(
                f"[BoilerplateDataLoader.load_categories_and_teams_meta_integrations_data] Error while loading "
                f"categories and teams integrations data: {e}")
        #####
        logger.info("[BoilerplateDataLoader.load] Boilerplate data loaded successfully")

    @staticmethod
    def _load_forum_data():
        categories_data_path = DataPaths.Forum.CATEGORIES
        threads_data_path = DataPaths.Forum.THREADS

        with open(categories_data_path, "r") as categories_file:
            categories_data_json = json.load(categories_file)
            for c in categories_data_json:
                c_name = c["name"]
                item = ForumCategory.objects.get_or_create(
                    name=c_name,
                    defaults={
                        **c
                    }
                )
                if item[1] is False:
                    # If item exists, update the item
                    item[0].name = c["name"]
                    item[0].description = c["description"]
                    item[0].save()
                    logger.info(f"[BoilerplateDataLoader._load_forum_data] Updated category: {c['name']}")
            # print(f"[BoilerplateDataLoader._load_forum_data] Pre-loaded {len(categories_data_json)} categories")
            pass

        # Load threads
        with open(threads_data_path, "r") as threads_file:
            threads_data_json = json.load(threads_file)
            for t in threads_data_json:
                t_title = t["title"]
                t_category_name = t["category"]
                t_category_object = ForumCategory.objects.get(name=t_category_name)
                item = ForumThread.objects.get_or_create(
                    title=t_title,
                    category=t_category_object
                )
                if item[1] is False:
                    # If item exists, update the item
                    item[0].category = t_category_object
                    item[0].save()
                    logger.info(f"[BoilerplateDataLoader._load_forum_data] Updated thread: {t['title']}")
            # print(f"[BoilerplateDataLoader._load_forum_data] Pre-loaded {len(threads_data_json)} threads")
            pass
        return

    @staticmethod
    def _load_blog_data():
        blogs_data_path = DataPaths.Blog.BLOGS

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
                else:
                    b_new.author = b_author_object
                    b_new.content = b_content
                    b_new.thumbnail_image = b_thumbnail_image
                    b_new.status = b_status
                    b_new.save()
                    b_new.tags.set(b_tag_objects)
            # print(f"[BoilerplateDataLoader._load_blog_data] Pre-loaded {len(blogs_data_json)} blog posts")
            pass
        return

    @staticmethod
    def _load_academy_data():
        instructors_data_path = DataPaths.Academy.INSTRUCTORS
        courses_data_path = DataPaths.Academy.COURSES
        sections_data_path = DataPaths.Academy.COURSE_SECTIONS
        videos_data_path = DataPaths.Academy.COURSE_VIDEOS

        # Load instructors
        existing_instructor_ids = []
        with open(instructors_data_path, "r") as instructors_file:
            instructors_data_json = json.load(instructors_file)
            for i in instructors_data_json:
                i_user = User.objects.get(username=i["user"])
                item = AcademyCourseInstructor.objects.get_or_create(
                    user=i_user,
                    defaults={
                        "full_name": i["full_name"],
                        "course_instructor_bio": i["course_instructor_bio"]
                    }
                )
                existing_instructor_ids.append(item[0].id)
                if item[1] is False:
                    # If item exists, update the item
                    item[0].full_name = i["full_name"]
                    item[0].course_instructor_bio = i["course_instructor_bio"]
                    item[0].save()
                    logger.info(f"[BoilerplateDataLoader._load_academy_data] Updated instructor: {i['full_name']}")
            # print(f"[BoilerplateDataLoader._load_academy_data] Pre-loaded {len(instructors_data_json)} instructors")
            pass
        # Delete others
        AcademyCourseInstructor.objects.exclude(id__in=existing_instructor_ids).delete()

        # Load courses
        existing_course_ids = []
        with open(courses_data_path, "r") as courses_file:
            courses_data_json = json.load(courses_file)
            for c in courses_data_json:
                c_instructor = AcademyCourseInstructor.objects.get(user__username=c["instructor"])
                item = AcademyCourse.objects.get_or_create(
                    course_title=c["course_title"],
                    defaults={
                        "course_thumbnail_image_url": c["course_thumbnail_image_url"],
                        "course_description": c["course_description"],
                        "course_language": c["course_language"],
                        "course_instructor": c_instructor,
                        "course_under_construction": c["course_under_construction"],
                        "tags": c["tags"]
                    }
                )
                existing_course_ids.append(item[0].id)
                if item[1] is False:
                    # If item exists, update the item
                    item[0].course_description = c["course_description"]
                    item[0].course_language = c["course_language"]
                    item[0].course_instructor = c_instructor
                    item[0].course_thumbnail_image_url = c["course_thumbnail_image_url"]
                    item[0].course_under_construction = c["course_under_construction"]
                    item[0].tags = c["tags"]
                    item[0].save()
                    logger.info(f"[BoilerplateDataLoader._load_academy_data] Updated course: {c['course_title']}")
            # print(f"[BoilerplateDataLoader._load_academy_data] Pre-loaded {len(courses_data_json)} courses")
            pass
        # Delete others
        AcademyCourse.objects.exclude(id__in=existing_course_ids).delete()

        # Load sections
        existing_section_ids = []
        with open(sections_data_path, "r") as sections_file:
            sections_data_json = json.load(sections_file)
            for s in sections_data_json:
                s_course = AcademyCourse.objects.get(course_title=s["course"])
                item = AcademyCourseSection.objects.get_or_create(
                    course=s_course,
                    section_name=s["section_name"],
                    defaults={
                        "section_description": s["section_description"]
                    }
                )
                existing_section_ids.append(item[0].id)
                if item[1] is False:
                    # If item exists, update the item
                    item[0].section_description = s["section_description"]
                    item[0].save()
                    logger.info(f"[BoilerplateDataLoader._load_academy_data] Updated section: {s['section_name']}")
            # print(f"[BoilerplateDataLoader._load_academy_data] Pre-loaded {len(sections_data_json)} sections")
            pass
        # Delete others
        AcademyCourseSection.objects.exclude(id__in=existing_section_ids).delete()

        # Load videos
        existing_video_ids = []
        with open(videos_data_path, "r") as videos_file:
            videos_data_json = json.load(videos_file)
            for v in videos_data_json:
                v_section = AcademyCourseSection.objects.get(section_name=v["course_section"],
                                                             course__course_title=v["course"])
                item = AcademyCourseVideo.objects.get_or_create(
                    course_section=v_section,
                    video_title=v["video_title"],
                    defaults={
                        "video_description": v["video_description"],
                        "video_content_url": v["video_content_url"]
                    }
                )
                existing_video_ids.append(item[0].id)
                if item[1] is False:
                    # If item exists, update the item
                    item[0].video_description = v["video_description"]
                    item[0].video_content_url = v["video_content_url"]
                    item[0].save()
                    logger.info(f"[BoilerplateDataLoader._load_academy_data] Updated video: {v['video_title']}")
            # print(f"[BoilerplateDataLoader._load_academy_data] Pre-loaded {len(videos_data_json)} videos")
            pass
        # Delete others
        AcademyCourseVideo.objects.exclude(id__in=existing_video_ids).delete()

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
    def _load_ml_models_data():
        ml_models_data_path = DataPaths.MLModels.ML_MODELS
        # TODO:
        #   1. Read the relevant data fixture JSON file
        #   2. Get or create the data
        #   3. Save the database
        #   4. Provide the required logs
        return

    @staticmethod
    def _load_assistant_integrations_data():
        assistant_integration_categories_data_path = DataPaths.AssistantIntegrations.ASSISTANT_INTEGRATION_CATEGORIES
        assistant_integrations_data_path = DataPaths.AssistantIntegrations.ASSISTANT_INTEGRATIONS

        # Categories
        with open(assistant_integration_categories_data_path, "r") as categories_file:
            categories_data_json = json.load(categories_file)

            for c in categories_data_json:
                c_name = c["category_name"]
                item = AssistantIntegrationCategory.objects.get_or_create(
                    category_name=c_name,
                    defaults={
                        "category_description": c["category_description"],
                        "category_image_url": c["category_image_url"],
                        "tags": c["tags"]
                    }
                )
                if item[1] is False:
                    # If item exists, update the item
                    item[0].category_name = c["category_name"]
                    item[0].description = c["category_description"]
                    item[0].category_image_url = c["category_image_url"]
                    item[0].tags = c["tags"]
                    item[0].save()
                    logger.info(
                        f"[BoilerplateDataLoader._load_assistant_integrations_data] Updated category: {c['category_name']}")
            # print(f"[BoilerplateDataLoader._load_assistant_integrations_data] Pre-loaded {len(categories_data_json)} categories")
            pass

        # Assistant Integrations
        with open(assistant_integrations_data_path, "r") as assistant_integrations_file:
            assistant_integrations_data_json = json.load(assistant_integrations_file)
            for a in assistant_integrations_data_json:
                a_category = AssistantIntegrationCategory.objects.get(category_name=a["integration_category"])
                item = AssistantIntegration.objects.get_or_create(
                    integration_name=a["integration_name"],
                    integration_category=a_category,
                    defaults={
                        "integration_description": a["integration_description"],
                        "integration_instructions": a["integration_instructions"],
                        "integration_audience": a["integration_audience"],
                        "integration_tone": a["integration_tone"],
                        "tags": a["tags"]
                    }
                )
                if item[1] is False:
                    # If item exists, update the item
                    item[0].integration_category = a_category
                    item[0].integration_description = a["integration_description"]
                    item[0].integration_instructions = a["integration_instructions"]
                    item[0].integration_audience = a["integration_audience"]
                    item[0].integration_tone = a["integration_tone"]
                    item[0].tags = a["tags"]
                    item[0].save()
                    logger.info(
                        f"[BoilerplateDataLoader._load_assistant_integrations_data] Updated assistant integration: {a['integration_name']}")

                    # Get or create the vector data
                    if SKIP_FIXTURE_EMBEDDINGS is False:
                        vector_data, created = IntegrationVectorData.objects.get_or_create(integration_assistant=item[0])
                        if created:
                            logger.info(
                                f"[BoilerplateDataLoader._load_assistant_integrations_data] Vector data created for assistant: {a['integration_name']}")
                        else:
                            logger.info(
                                f"[BoilerplateDataLoader._load_assistant_integrations_data] Vector data already exists; updating for assistant: {a['integration_name']}")
                            vector_data.save()
                    else:
                        logger.info(
                            f"[BoilerplateDataLoader._load_assistant_integrations_data] Skipping vector data creation for assistant: {a['integration_name']}")

            # print(f"[BoilerplateDataLoader._load_assistant_integrations_data] Pre-loaded {len(assistant_integrations_data_json)} assistant integrations")
            pass
        return

    @staticmethod
    def _load_categories_and_teams_meta_integrations_data():
        categories_meta_integrations_data_path = DataPaths.CategoriesAndTeamsMetaIntegrations.CATEGORIES_META_INTEGRATIONS
        teams_meta_integrations_data_path = DataPaths.CategoriesAndTeamsMetaIntegrations.TEAMS_META_INTEGRATIONS

        # Categories
        with open(categories_meta_integrations_data_path, "r") as categories_file:
            categories_data_json = json.load(categories_file)

            for c in categories_data_json:
                c_name = c["category_name"]
                item = MetaIntegrationCategory.objects.get_or_create(
                    category_name=c_name,
                    defaults={
                        "category_description": c["category_description"],
                        "category_image_url": c["category_image_url"],
                        "tags": c["tags"]
                    }
                )
                if item[1] is False:
                    # If item exists, update the item
                    item[0].category_name = c["category_name"]
                    item[0].description = c["category_description"]
                    item[0].category_image_url = c["category_image_url"]
                    item[0].tags = c["tags"]
                    item[0].save()
                    logger.info(
                        f"[BoilerplateDataLoader._load_categories_and_teams_meta_integrations_data] Updated category: {c['category_name']}")
            # print(f"[BoilerplateDataLoader._load_categories_and_teams_meta_integrations_data] Pre-loaded {len(categories_data_json)} categories")
            pass

        # Teams Integrations
        with open(teams_meta_integrations_data_path, "r") as teams_integrations_file:
            teams_integrations_data_json = json.load(teams_integrations_file)
            for t in teams_integrations_data_json:
                t_category = MetaIntegrationCategory.objects.get(category_name=t["meta_integration_category"])
                t_integration_assistants = AssistantIntegration.objects.filter(
                    integration_category__category_name=t_category,
                    integration_name__in=t["integration_assistants"]
                )
                combined_tags = []
                for ta in t_integration_assistants:
                    combined_tags = list(set(combined_tags + ta.tags))
                combined_tags = list(set(combined_tags))
                item = MetaIntegrationTeam.objects.get_or_create(
                    meta_integration_name=t["meta_integration_name"],
                    meta_integration_category=t_category,
                    defaults={
                        "meta_integration_description": t["meta_integration_description"],
                        "tags": combined_tags
                    }
                )
                # Update assistant integrations list
                item[0].integration_assistants.set(t_integration_assistants)
                item[0].save()

                if item[1] is False:
                    # If item exists, update the item
                    item[0].meta_integration_category = t_category
                    item[0].meta_integration_description = t["meta_integration_description"]
                    item[0].tags = combined_tags
                    item[0].save()

                    # Update assistant integrations list
                    item[0].integration_assistants.set(t_integration_assistants)
                    item[0].save()

                    logger.info(
                        f"[BoilerplateDataLoader._load_categories_and_teams_meta_integrations_data] Updated team integration: {t['meta_integration_name']}")
            # print(f"[BoilerplateDataLoader._load_categories_and_teams_meta_integrations_data] Pre-loaded {len(teams_integrations_data_json)} teams integrations")
            pass
        return
