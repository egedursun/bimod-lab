#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: core_service_code_base_query.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.codebase.codebase_decoder import CodeBaseDecoder
from apps.datasource_codebase.models import CodeRepositoryStorageConnection


def run_query_code_base(c_id: int, query_content_str: str, semantic_alpha: float):
    conn = CodeRepositoryStorageConnection.objects.get(id=c_id)
    try:
        cli = CodeBaseDecoder().get(connection=conn)
        output = cli.search_hybrid(query=query_content_str, alpha=semantic_alpha)
    except Exception as e:
        error = f"There has been an unexpected error on running the codebase query: {e}"
        return error
    return output
