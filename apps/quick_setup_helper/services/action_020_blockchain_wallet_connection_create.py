#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_020_blockchain_wallet_connection_create.py
#  Last Modified: 2024-11-18 22:26:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:26:25
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

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

from apps.smart_contracts.models import (
    BlockchainWalletConnection
)

from apps.smart_contracts.utils import (
    BlockchainTypesNames
)

logger = logging.getLogger(__name__)


def action__020_blockchain_wallet_connection_create(
    metadata__user,
    metadata__organization,
    response__blockchain_wallet_address,
    response__blockchain_wallet_private_key
):
    try:
        new_wallet_connection = BlockchainWalletConnection.objects.create(
            organization=metadata__organization,
            blockchain_type=BlockchainTypesNames.ETHEREUM,
            nickname=f"Primary Wallet Connection for {metadata__organization.name} {generate_random_object_id_string()}",
            description=f"This is the primary Blockchain / Ethereum wallet connection for organization {metadata__organization.name}.",
            wallet_address=response__blockchain_wallet_address,
            wallet_private_key=response__blockchain_wallet_private_key,
            created_by_user=metadata__user
        )

    except Exception as e:
        logger.error(f"Error on action__020_blockchain_wallet_connection_create: {e}")

        return False, None

    logger.info(f"New blockchain wallet connection created for user: {metadata__user.username}")

    return True, new_wallet_connection
