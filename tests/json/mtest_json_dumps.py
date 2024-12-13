#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mtest_json_dumps.py
#  Last Modified: 2024-10-21 14:54:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 14:54:48
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


def mtest_json_dumps():
    tx = {
        'blockHash': '0xabc123',
        'blockNumber': 1234567,
        'contractAddress': '0xContractAddress',
        'cumulativeGasUsed': 21000,
        'from': '0xSenderAddress',
        'gasUsed': 21000,
        'logs': [],
        'status': 1,
        'to': '0xReceiverAddress',
        'transactionHash': '0xTransactionHash',
        'transactionIndex': 0
    }

    txs = json.dumps(tx)

    with open('txs.txt', 'w') as f:
        f.write(txs)


if __name__ == '__main__':
    mtest_json_dumps()
