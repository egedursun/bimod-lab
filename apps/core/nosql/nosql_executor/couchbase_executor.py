#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: couchbase_executor.py
#  Last Modified: 2024-10-10 16:20:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-10 16:20:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.nosql.utils import before_execute_nosql_query, can_write_to_database
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames

from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, QueryOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
from apps.core.generative_ai.utils import ChatRoles


class CouchbaseNoSQLExecutor:
    def __init__(self, connection: NoSQLDatabaseConnection):
        before_execute_nosql_query(connection)
        self.conn_params = {
            'bucket_name': connection.bucket_name,
            'user': connection.username,
            'password': connection.password,
            'host': connection.host
        }
        self.connection_object = connection

    def execute_read(self, query, parameters=None):
        output = {"status": True, "error": ""}
        try:
            cluster = Cluster(f"couchbase://{self.conn_params['host']}", ClusterOptions(
                PasswordAuthenticator(self.conn_params['user'], self.conn_params['password'])))
            if parameters:
                result = cluster.query(query, QueryOptions(named_parameters=parameters))
            else:
                result = cluster.query(query)
            output['result'] = [row for row in result]
        except CouchbaseException as e:
            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.connection_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLReadExecutor.COST, transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_READ, is_tool_cost=True)
        new_tx.save()
        return output

    def execute_write(self, query, parameters=None) -> dict:
        if not can_write_to_database(self.connection_object):
            return {"status": False, "error": "No write permission within this database connection."}

        output = {"status": True, "error": ""}
        try:
            cluster = Cluster(f"couchbase://{self.conn_params['host']}", ClusterOptions(
                PasswordAuthenticator(self.conn_params['user'], self.conn_params['password'])))
            if parameters:
                cluster.query(query, QueryOptions(named_parameters=parameters))
            else:
                cluster.query(query)
        except CouchbaseException as e:
            output["status"] = False
            output["error"] = str(e)

        new_tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.connection_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.NoSQLWriteExecutor.COST, transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.NOSQL_WRITE, is_tool_cost=True)
        new_tx.save()
        return output
