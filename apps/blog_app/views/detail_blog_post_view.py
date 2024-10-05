#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: detail_blog_post_view.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: detail_blog_post_view.py
#  Last Modified: 2024-09-26 18:30:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:20:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.blog_app.models import BlogPost
from web_project import TemplateLayout


class BlogPostDetailView(LoginRequiredMixin, TemplateView):
    """
    Displays the details of a specific blog post.

    The view fetches a blog post based on its slug and displays its content.
    Additionally, it retrieves and displays a list of related posts based on shared tags.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(BlogPost, slug=post_slug, status='published')
        context['post'] = post

        # Fetch SEO metadata if available
        if hasattr(post, 'seo_meta'):
            context['seo_meta'] = post.seo_meta

        # for related posts, get posts with the same tags
        related_posts = BlogPost.objects.filter(tags__in=post.tags.all()).exclude(id=post.id).distinct()[:3]
        context['related_posts'] = related_posts
        return context
