#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_blog_post_view.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.blog_app.models import BlogPost
from web_project import TemplateLayout, TemplateHelper

logger = logging.getLogger(__name__)


class BlogPostView_Detail(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout": "blank", "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(BlogPost, slug=post_slug, status='published')
        context['post'] = post
        if hasattr(post, 'seo_meta'):
            context['seo_meta'] = post.seo_meta
        related_posts = BlogPost.objects.filter(tags__in=post.tags.all()).exclude(id=post.id).distinct()[:3]
        context['related_posts'] = related_posts
        logger.info(f"Blog Post {post.title} was viewed.")
        return context
