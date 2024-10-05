#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: generator.py
#  Last Modified: 2024-10-05 02:13:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

import random as r

from apps._meta.voidforger.test_helpers.mock_stream_text import MOCK_STREAM_STRATEGIST, MOCK_STREAM_BACKTESTING, \
    MOCK_STREAM_TRADER, MOCK_STREAM_RISK_MANAGER, MOCK_STREAM_PORTFOLIO_MANAGER
from apps._meta.voidforger.test_helpers.mocker import mock_legion_nodes, mock_operation_nodes, generate_stream_data, \
    mock_trading


def generate_for_time_step():
    # generate legion nodes
    legion_nodes = mock_legion_nodes()
    # generate operation nodes
    operation_nodes = mock_operation_nodes()
    # generate stream text
    picklist = [
        MOCK_STREAM_STRATEGIST,
        MOCK_STREAM_BACKTESTING,
        MOCK_STREAM_TRADER,
        MOCK_STREAM_RISK_MANAGER,
        MOCK_STREAM_PORTFOLIO_MANAGER
    ]
    # generate trading text
    trading_text = mock_trading()

    selected_legion_node = r.choice(picklist)
    stream_text = generate_stream_data(selected_legion_node)

    return {
        "legion_nodes": legion_nodes,
        "operation_nodes": operation_nodes,
        "stream_text": stream_text,
        "trading_text": trading_text
    }


