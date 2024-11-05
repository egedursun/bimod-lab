#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: path_consts.py
#  Last Modified: 2024-10-05 15:31:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:24:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

class DataPaths:
    class Forum:
        CATEGORIES = "data/community/forum/categories.json"
        THREADS = "data/community/forum/threads.json"

    class Blog:
        BLOGS = "data/community/blog/blogs.json"

    class Academy:
        INSTRUCTORS = "data/community/academy/instructors.json"
        COURSES = "data/community/academy/courses.json"
        COURSE_SECTIONS = "data/community/academy/course_sections.json"
        COURSE_VIDEOS = "data/community/academy/course_videos.json"

    class Functions:
        FUNCTIONS = "data/marketplace/functions/custom_functions.json"

    class APIs:
        APIs = "data/marketplace/apis/custom_apis.json"

    class Scripts:
        SCRIPTS = "data/marketplace/scripts/custom_scripts.json"

    class KnowledgeBases:
        KNOWLEDGE_BASES = "data/marketplace/knowledge_bases/boilerplate_knowledge_bases.json"

    class AssistantIntegrations:
        ASSISTANT_INTEGRATIONS = "data/meta_features/assistant_integrations/custom_assistants.json"

    class OrchestrationMetaIntegrations:
        ORCHESTRATION_META_INTEGRATIONS = "data/meta_features/orchestration_meta_integrations/custom_orchestrations.json"
