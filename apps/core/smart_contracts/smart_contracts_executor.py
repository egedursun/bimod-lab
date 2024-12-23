#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: smart_contracts_executor.py
#  Last Modified: 2024-10-19 23:14:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 23:14:13
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
import logging

from django.utils import timezone
from solcx.exceptions import SolcError
from web3 import Web3
from solcx import compile_source
from web3.exceptions import TimeExhausted

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles,
    find_tool_call_from_json,
)

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.core.smart_contracts.builders import (
    build_smart_contract_generation_prompt,
    build_smart_contract_refinement_prompt
)

from apps.core.smart_contracts.prompts import (
    contract_natural_language_context_explanation_prompt
)

from apps.core.smart_contracts.utils import (
    DEFAULT_TRANSACTION_RECEIPT_CHECK_TIMEOUT_SECONDS,
    DEFAULT_TRANSACTION_RECEIPT_CHECK_POLL_LATENCY_SECONDS
)

from apps.llm_core.models import LLMCore
from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

from apps.smart_contracts.models import (
    BlockchainSmartContract,
    BlockchainWalletConnection
)

from apps.smart_contracts.utils import (
    DeploymentStatusesNames,
)

from config import settings

logger = logging.getLogger(__name__)


class SmartContractsExecutionManager:
    def __init__(
        self,
        smart_contract_object: BlockchainSmartContract,
        llm_model: LLMCore
    ):

        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        self.contract_obj: BlockchainSmartContract = smart_contract_object
        self.wallet: BlockchainWalletConnection = smart_contract_object.wallet

        self.llm_model: LLMCore = llm_model

        self.c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

        # self._install_solc_safe()

    @staticmethod
    def _install_solc_safe(version="0.8.7"):

        import solcx

        try:
            # Check if the required version of solc is already installed
            installed_versions = solcx.get_installed_solc_versions()

            if version in installed_versions:
                logging.info(f"Solidity compiler version {version} is already installed.")

            else:
                logging.info(f"Installing Solidity compiler version {version}...")
                solcx.install_solc(version)
                logging.info(f"Solidity compiler version {version} installed successfully.")

            solcx.set_solc_version(version)
            logging.info(f"Using Solidity compiler version {version}.")

        except Exception as e:
            logging.error(f"An error occurred while installing or setting Solidity version {version}: {str(e)}")

    @staticmethod
    def is_valid_solidity_syntax(solidity_code: str):

        try:
            compiled_sol = compile_source(solidity_code)
            logger.info(f"Solidity code passed the syntax check.")

            # Extract the ABI (Application Binary Interface)
            contract_interface = compiled_sol.popitem()[1]
            contract_abi = contract_interface['abi']
            return contract_abi, None

        except SolcError as e:
            logger.error(f"Solidity syntax check failed: {e}")
            return False, str(e)

    def parse_and_save_generated_contract_functions(self):

        contract_explanation_data = self.contract_obj.generated_solidity_code_natural_language

        try:
            json_object = find_tool_call_from_json(contract_explanation_data)

        except Exception as e:
            logger.error(f"Smart Contract JSON Response Parsing Failed: {e}")
            return False

        if len(json_object) == 0:
            logger.error(f"Smart Contract JSON Response Parsing Failed: No valid JSON Found.")
            return False

        else:
            json_object = json_object[0]

        extraction_object = json_object
        topic = extraction_object.get("topic", "N/A")
        protocol_details = extraction_object.get("protocol_details", "N/A")
        summary = extraction_object.get("summary", "N/A")

        parties = extraction_object.get("parties", [])
        clauses = extraction_object.get("clauses", [])
        functions = extraction_object.get("functions", [])
        contract_args = extraction_object.get("contract_args", {})

        self.contract_obj.post_gen_topic = topic
        self.contract_obj.post_gen_protocol_details = protocol_details
        self.contract_obj.pot_gen_summary = summary
        self.contract_obj.post_gen_parties = parties

        self.contract_obj.post_gen_clauses = clauses
        self.contract_obj.post_gen_functions = functions
        self.contract_obj.contract_args = contract_args
        self.contract_obj.save()

        logger.info(f"Smart Contract Functions Saved Successfully.")
        return True

    def _ai_generate_contract_code(
        self,
        messages: list,
        previous_mistakes_prompt
    ):
        final_response, error = "N/A", None

        try:
            system_prompt = build_smart_contract_generation_prompt(
                contract_object=self.contract_obj,
                previous_mistakes_prompt=previous_mistakes_prompt
            )

            tx = LLMTransaction.objects.create(
                organization=self.wallet.organization,
                model=self.llm_model,
                responsible_user=self.wallet.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(system_prompt),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION
            )

            tx.save()

            logger.info(f"[create_contract] Smart Contract System Prompt Creation Transaction Created.")

            structured_messages = [
                {
                    "role": ChatRoles.SYSTEM,
                    "content": system_prompt
                }
            ]

            conversation_messages = structured_messages + messages

            llm_response = self.c.chat.completions.create(
                model=self.llm_model.model_name,
                messages=conversation_messages,
                # temperature=float(self.llm_model.temperature),
                # frequency_penalty=float(self.llm_model.frequency_penalty),
                # presence_penalty=float(self.llm_model.presence_penalty),
                # max_tokens=int(self.llm_model.maximum_tokens),
                # top_p=float(self.llm_model.top_p)
            )

            choices = llm_response.choices
            first_choice = choices[0]

            choice_message = first_choice.message
            choice_message_content = choice_message.content

            final_response = choice_message_content
            logger.info(f"AI Generated Smart Contract Code.")

        except Exception as e:
            error = e
            logger.error(f"AI Smart Contract Generation Failed: {e}")

        return final_response, error

    ###

    def _create_contract(
        self,
        previous_mistakes_prompt
    ):

        output, contract_explanation, error = "N/A", "N/A", None
        n_iterations = self.contract_obj.refinement_iterations_before_evaluation

        messages = []
        contract_abi = []

        for i in range(0, n_iterations, 1):

            assistant_response, error = self._ai_generate_contract_code(
                messages=messages,
                previous_mistakes_prompt=previous_mistakes_prompt
            )

            if error is not None:
                logger.error(f"Smart Contract Generation Failed: {error}")
                return None, None, error

            logger.info(f"Smart Contract Generated for iteration: {i}.")

            messages.append(
                {
                    "role": ChatRoles.ASSISTANT,
                    "content": str(assistant_response)
                }
            )

            tx = LLMTransaction.objects.create(
                organization=self.wallet.organization,
                model=self.llm_model,
                responsible_user=self.wallet.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(assistant_response),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION
            )

            tx.save()

            logger.info(f"[create_contract] Smart Contract Assistant Prompt Creation Transaction Created.")

            tx = LLMTransaction(
                organization=self.wallet.organization,
                model=self.llm_model,
                responsible_user=self.wallet.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.SmartContractCreation.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION,
                is_tool_cost=True
            )

            tx.save()

            logger.info(f"[create_contract] Smart Contract Creation Tool Cost Transaction Created.")

            if i < (n_iterations - 1):

                refinement_prompt = build_smart_contract_refinement_prompt(
                    contract_object=self.contract_obj,
                    previous_mistakes_prompt=previous_mistakes_prompt
                )

                messages.append(
                    {
                        "role": ChatRoles.USER,
                        "content": refinement_prompt
                    }
                )

                contract_abi, syntax_error = self.is_valid_solidity_syntax(
                    solidity_code=self.contract_obj.generated_solidity_code
                )

                if contract_abi is False:
                    logger.error(f"Smart Contract Generation Failed: {syntax_error}")
                    refinement_prompt += f"""
                        =================================================================================
                        # **SYNTAX ERROR IN PREVIOUS SOLIDITY CODE:**

                        - The code you have implemented at first has been detected to have syntax errors.
                        - Please observe the errors below and fix them:

                        '''

                        {syntax_error}

                        '''
                        =================================================================================

                    -----
                    """

                tx = LLMTransaction.objects.create(
                    organization=self.wallet.organization,
                    model=self.llm_model,
                    responsible_user=self.wallet.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(refinement_prompt),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.USER,
                    transaction_source=LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION
                )

                tx.save()

                logger.info(f"[create_contract] Smart Contract User Prompt Creation Transaction Created.")

            else:
                logger.info(f"Smart Contract Generation Completed.")
                break

        if len(messages) > 0:
            final_contract_code = messages[-1]['content']

            logger.info(f"Smart Contract Message output has been retrieved successfully.")

        else:
            error = "No messages were generated."

            logger.error(f"Smart Contract Generation Failed: {error}")

            return None, None, error

        self.contract_obj.generated_solidity_code = final_contract_code
        self.contract_obj.contract_abi = contract_abi

        self.contract_obj.save()

        nlp_feed_prompt = contract_natural_language_context_explanation_prompt(
            contract_object=self.contract_obj
        )

        if nlp_feed_prompt is not None and nlp_feed_prompt != "":
            try:
                tx = LLMTransaction.objects.create(
                    organization=self.wallet.organization,
                    model=self.llm_model,
                    responsible_user=self.wallet.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(nlp_feed_prompt),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION
                )

                tx.save()

                logger.info(f"[create_contract] Smart Contract NLP Feed Prompt Creation Transaction Created.")

                structured_messages = [
                    {
                        "role": ChatRoles.SYSTEM,
                        "content": nlp_feed_prompt
                    }
                ]

                contract_description_llm_response = self.c.chat.completions.create(
                    model=self.llm_model.model_name,
                    messages=structured_messages,
                    # temperature=float(self.llm_model.temperature),
                    # frequency_penalty=float(self.llm_model.frequency_penalty),
                    # presence_penalty=float(self.llm_model.presence_penalty),
                    # max_tokens=int(self.llm_model.maximum_tokens),
                    # top_p=float(self.llm_model.top_p)
                )

                tx = LLMTransaction.objects.create(
                    organization=self.wallet.organization,
                    model=self.llm_model,
                    responsible_user=self.wallet.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(contract_description_llm_response),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=LLMTransactionSourcesTypesNames.SMART_CONTRACT_CREATION
                )

                tx.save()

                logger.info(
                    f"[create_contract] Smart Contract NLP Feed Prompt Assistant Response Transaction Created.")

                choices = contract_description_llm_response.choices
                first_choice = choices[0]

                choice_message = first_choice.message
                choice_message_content = choice_message.content

                contract_explanation = choice_message_content

                logger.info(f"Smart Contract Explanation Generated.")

            except Exception as e:
                error = e
                logger.error(f"AI Smart Contract Generation Failed: {e}")

                return None, None, error

        self.contract_obj.generated_solidity_code_natural_language = contract_explanation
        self.contract_obj.save()

        response = self.parse_and_save_generated_contract_functions()

        if response is False:
            error = "Smart Contract Function Parsing Failed: No valid JSON Found."
            logger.error(f"Smart Contract Generation Failed: No valid JSON Found.")

            return None, None, error

        logger.info(f"Smart Contract Generation & Explanation Completed.")

        return final_contract_code, contract_explanation, error

    def generate_contract_and_save_content(
        self,
        previous_mistakes_prompt
    ):
        try:
            contract_code, contract_explanation, error = self._create_contract(
                previous_mistakes_prompt=previous_mistakes_prompt
            )

            if error is not None:
                logger.error(f"Smart Contract Generation Failed: {error}")
                return False, error

            # Clean the output
            contract_code = contract_code.replace("'''solidity", "")
            contract_code = contract_code.replace("```solidity", "")
            contract_code = contract_code.replace("'''", "")
            contract_code = contract_code.replace("```", "")

            contract_explanation = contract_explanation.replace("'''json", "")
            contract_explanation = contract_explanation.replace("```json", "")
            contract_explanation = contract_explanation.replace("'''", "")
            contract_explanation = contract_explanation.replace("```", "")

            self.contract_obj.generated_solidity_code = contract_code
            self.contract_obj.generated_solidity_code_natural_language_explanation = contract_explanation
            self.contract_obj.deployment_status = DeploymentStatusesNames.GENERATED_UNSIGNED
            self.contract_obj.save()

            logger.info(f"Smart Contract Content Saved.")

            return True, error

        except Exception as e:
            error = e
            logger.error(f"Smart Contract Generation Failed: {error}")

            return False, error

    @staticmethod
    def deploy_contract(contract_obj):

        is_success, error = False, None

        c_obj: BlockchainSmartContract = contract_obj
        contract_text = c_obj.generated_solidity_code
        contract_args = c_obj.contract_args

        try:
            c_obj.deployment_status = DeploymentStatusesNames.TRANSACTION_STAGED
            c_obj.save()

            # Set up Web3 connection to Ethereum mainnet
            infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
            web3 = Web3(Web3.HTTPProvider(infura_url))

            if not web3.is_connected():
                error = "Web3 Connection Failed."
                logger.error(f"Smart Contract Deployment Failed: {error}")

                return False, error

            logger.info(f"Web3 Connection Established Successfully.")

            # Compile contract code using SOLCX
            compiled_sol = compile_source(contract_text)
            contract_interface = compiled_sol.popitem()[1]

            logger.info(f"Smart Contract Compiled Successfully.")

            # Prepare contract to deploy
            contract = web3.eth.contract(
                abi=contract_interface['abi'],
                bytecode=contract_interface['bin']
            )

            logger.info(f"Smart Contract Prepared for Deployment.")

            # Get account & private key
            account = c_obj.wallet.wallet_address
            private_key = c_obj.wallet.wallet_private_key

            logger.info(f"Account and Private Key Retrieved Successfully.")

            # Build the contract deploy tx
            nonce = web3.eth.get_transaction_count(account)

            transaction = contract.constructor(**contract_args).build_transaction(
                {
                    'from': account,
                    'nonce': nonce,
                    'gas': c_obj.maximum_gas_limit,
                    'gasPrice': web3.to_wei(
                        f'{c_obj.gas_price_gwei}',
                        'gwei'
                    )
                }
            )

            logger.info(f"Smart Contract Deployment Transaction Built Successfully.")

            # Sign the blockchain tx with the private key
            signed_txn = web3.eth.account.sign_transaction(
                transaction,
                private_key=private_key
            )

            logger.info(f"Smart Contract Deployment Transaction Signed Successfully.")

            # Send the blockchain tx
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

            logger.info(f"Smart Contract Deployment Transaction Sent Successfully.")

            # Save the hash to the contract
            c_obj.tx_hash = tx_hash
            c_obj.deployment_status = DeploymentStatusesNames.WAITING_FOR_MINING

            c_obj.save()

            logger.info(f"Smart Contract Deployment Transaction Hash Saved Successfully.")

        except Exception as e:
            error = e
            logger.error(f"Smart Contract Deployment Failed: {error}")

            return False, error

        logger.info(f"Smart Contract Deployed Successfully.")

        return True, error

    @staticmethod
    def check_deployment_status(
        contract_obj: BlockchainSmartContract
    ):
        output, error = False, None

        c_obj: BlockchainSmartContract = contract_obj

        tx_hash = c_obj.tx_hash

        if tx_hash is None:
            error = "No transaction hash found."
            logger.error(f"Smart Contract Deployment Status Check Failed: {error}")

            return False, error

        try:
            infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
            web3 = Web3(Web3.HTTPProvider(infura_url))

            if not web3.is_connected():
                error = "Web3 Connection Failed."
                logger.error(f"Smart Contract Status check has Failed: {error}")

                return False, error

            try:
                tx_receipt = web3.eth.wait_for_transaction_receipt(
                    tx_hash,
                    timeout=DEFAULT_TRANSACTION_RECEIPT_CHECK_TIMEOUT_SECONDS,
                    poll_latency=DEFAULT_TRANSACTION_RECEIPT_CHECK_POLL_LATENCY_SECONDS
                )

            except TimeExhausted as e:
                error = e
                logger.error(f"Smart Contract Status Check Timeout: {error}")

                return False, error

            except Exception as e:
                error = e
                logger.error(f"Smart Contract Status Check Failed: {error}")

                return False, error

            logger.info(f"Smart Contract Deployment Transaction Receipt Retrieved Successfully.")

            c_obj.contract_address = tx_receipt.get("contractAddress", "Corrupted Data")
            c_obj.deployment_status = DeploymentStatusesNames.DEPLOYED
            c_obj.tx_receipt_raw = json.dumps(tx_receipt)
            c_obj.deployed_at = timezone.now()

            c_obj.save()

            return True, error

        except Exception as e:
            error = e
            logger.error(f"Smart Contract Deployment Status Check Failed: {error}")

            return False, error

    #####

    def call_smart_contract_function(
        self,
        function_name: str,
        function_kwargs: dict
    ):

        c_obj: BlockchainSmartContract = self.contract_obj
        contract_address = c_obj.contract_address

        if contract_address is None:
            error = "No contract address found."
            logger.error(f"Smart Contract Function Execution Failed: {error}")

            return error

        try:
            infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
            web3 = Web3(Web3.HTTPProvider(infura_url))

            if not web3.is_connected():
                error = "Web3 Connection Failed."
                logger.error(f"Smart Contract Function Execution Failed: {error}")

                return error

            contract_abi = c_obj.contract_abi

            contract = web3.eth.contract(
                address=contract_address,
                abi=contract_abi
            )

            function_metadata = next(
                (
                    f for f in c_obj.post_gen_functions if f["function_name"] == function_name
                ),
                None
            )

            if function_metadata is None:
                error = f"Function {function_name} not found in the stored contract functions."
                logger.error(f"Smart Contract Function Execution Failed: {error}")

                return error

            input_params_metadata = function_metadata.get('input_parameters', [])

            expected_param_names = [
                param['name'] for param in input_params_metadata
            ]

            for param in expected_param_names:

                if param not in function_kwargs:
                    error = f"Missing required parameter: {param}"
                    logger.error(f"Smart Contract Function Execution Failed: {error}")

                    return error

            function_args = [
                function_kwargs[
                    param
                ] for param in expected_param_names
            ]

            contract_function = getattr(
                contract.functions,
                function_name
            )

            response_of_call = contract_function(*function_args).call()

            logger.info(f"Smart Contract Function Executed Successfully.")

        except Exception as e:
            error = e
            logger.error(f"Smart Contract Function Execution Failed: {error}")

            return error

        logger.info(f"Smart Contract Function Execution Completed.")
        final_response = str(response_of_call)

        return final_response
