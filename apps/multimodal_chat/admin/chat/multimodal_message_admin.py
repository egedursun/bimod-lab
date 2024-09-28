#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


from django.contrib import admin

from apps.multimodal_chat.models import MultimodalChatMessage


@admin.register(MultimodalChatMessage)
class MultimodalChatMessageAdmin(admin.ModelAdmin):
    list_display = ['multimodal_chat', 'sender_type', 'sent_at']
    list_filter = ['multimodal_chat', 'sender_type', 'sent_at']
    search_fields = ['multimodal_chat', 'sender_type', 'sent_at']
    readonly_fields = ['sent_at']
    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_select_related = False
    list_display_links_details = False
