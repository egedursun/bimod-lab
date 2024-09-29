#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: mocker.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 21:59:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import random as r

from apps._meta.voidforger.test_helpers.mock_stream_text import MOCK_TRADING_ACTIVITY, \
    MOCK_TRADING_SYMBOL, MOCK_LEVERAGE


class MockLegionNodeStatusNames:
    IDLE = "idle"
    PROCESSING = "processing"
    SENDING = "sending"
    RECEIVING = "receiving"

    @staticmethod
    def as_list():
        return [
            MockLegionNodeStatusNames.IDLE,
            MockLegionNodeStatusNames.PROCESSING,
            MockLegionNodeStatusNames.SENDING,
            MockLegionNodeStatusNames.RECEIVING,
        ]


class MockOperationNodeStatusNames:
    ST0 = "ST0"
    STA = "STA"
    STB = "STB"
    STC = "STC"


def mock_legion_node_status():
    return r.choice(MockLegionNodeStatusNames.as_list())


def mock_legion_nodes(n_nodes=5):
    legion_node_status_mocks = []
    for i in range(n_nodes):
        legion_node_status_mocks.append(mock_legion_node_status())
    return legion_node_status_mocks


def mock_operation_node_status():
    likelihood_st0 = 0.50
    likelihood_sta = 0.30
    likelihood_stb = 0.15

    val_operation_node = r.random()
    if val_operation_node < likelihood_st0:
        return MockOperationNodeStatusNames.ST0
    elif val_operation_node < likelihood_st0 + likelihood_sta:
        return MockOperationNodeStatusNames.STA
    elif val_operation_node < likelihood_st0 + likelihood_sta + likelihood_stb:
        return MockOperationNodeStatusNames.STB
    else:
        return MockOperationNodeStatusNames.STC


def mock_operation_nodes(n_nodes=9):
    operation_node_status_mocks = []
    for i in range(n_nodes):
        operation_node_status_mocks.append(mock_operation_node_status())
    return operation_node_status_mocks


def generate_stream_data(picklist):
    # pick status
    status_text = r.choice(picklist)
    return status_text


def mock_trading():
    prob_buy = 0.04
    prob_sell = 0.04
    prob_close = 0.08
    activity_num = r.random()
    if activity_num < prob_buy:
        activity_text = MOCK_TRADING_ACTIVITY[0]
    elif activity_num < prob_buy + prob_sell:
        activity_text = MOCK_TRADING_ACTIVITY[1]
    elif activity_num < prob_buy + prob_sell + prob_close:
        activity_text = MOCK_TRADING_ACTIVITY[2]
    else:
        activity_text = MOCK_TRADING_ACTIVITY[3]

    leverage_text = ""
    symbol_text = ""
    if activity_text != MOCK_TRADING_ACTIVITY[2] and activity_text != MOCK_TRADING_ACTIVITY[3]:
        prob_x1 = 0.500
        prob_x2 = 0.250
        prob_x3 = 0.125
        prob_x4 = 0.062
        prob_x5 = 0.031
        prob_x6 = 0.016
        prob_x8 = 0.008
        prob_x10 = 0.004
        prob_x20 = 0.002
        leverage_num = r.random()
        if leverage_num < prob_x1:
            leverage_text = MOCK_LEVERAGE[0]
        elif leverage_num < prob_x1 + prob_x2:
            leverage_text = MOCK_LEVERAGE[1]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3:
            leverage_text = MOCK_LEVERAGE[2]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3 + prob_x4:
            leverage_text = MOCK_LEVERAGE[3]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3 + prob_x4 + prob_x5:
            leverage_text = MOCK_LEVERAGE[4]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3 + prob_x4 + prob_x5 + prob_x6:
            leverage_text = MOCK_LEVERAGE[5]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3 + prob_x4 + prob_x5 + prob_x6 + prob_x8:
            leverage_text = MOCK_LEVERAGE[6]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3 + prob_x4 + prob_x5 + prob_x6 + prob_x8 + prob_x10:
            leverage_text = MOCK_LEVERAGE[7]
        elif leverage_num < prob_x1 + prob_x2 + prob_x3 + prob_x4 + prob_x5 + prob_x6 + prob_x8 + prob_x10 + prob_x20:
            leverage_text = MOCK_LEVERAGE[8]
        else:
            leverage_text = MOCK_LEVERAGE[9]

    if activity_text != MOCK_TRADING_ACTIVITY[3]:
        symbol_text = r.choice(MOCK_TRADING_SYMBOL)

    final_text = activity_text + symbol_text + leverage_text
    return final_text
