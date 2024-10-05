#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: mongodb_mtest.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:37:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

HOST = 'bimodtest.d89cgcx.mongodb.net'
USER = 'root'
PASSWORD = 'V4AXP7dSzeuIaemC'

connection_string = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/?retryWrites=true&w=majority&appName=BimodTest"
client = MongoClient(connection_string, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    col_names = client.get_database('sample_mflix').list_collection_names()
except Exception as e:
    pass
