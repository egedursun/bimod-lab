from apps.leanmod.models import LeanAssistant, ExpertNetwork, ExpertNetworkAssistantReference


def build_expert_networks_multi_modality_prompt_leanmod(lean_assistant: LeanAssistant):
    # Retrieve the functions of the assistant
    expert_networks = lean_assistant.expert_networks.all()
    # Build the prompt
    response_prompt = """
                *EXPERT NETWORKS*

                '''
                """

    for i, expert_network in enumerate(expert_networks):
        expert_network: ExpertNetwork
        response_prompt += f"""
                    [Network Name: {expert_network.name}]
                    [Network Description: {expert_network.meta_description}]
                    """
        assistant_references = expert_network.assistant_references.all()
        for j, assistant_reference in enumerate(assistant_references):
            assistant_reference: ExpertNetworkAssistantReference
            assistant = assistant_reference.assistant
            response_prompt += f"""
                        [Assistant ID: {assistant_reference.id}]
                        [Assistant Name: {assistant.name}]
                        [Assistant Description: {assistant_reference.context_instructions}]
            """

    response_prompt += """
                ---

                '''
                Assistant ID: ID of the expert assistant.
                Assistant Name: Name of the expert assistant.
                Assistant Description: Description explaining specialties of expert.

                ---
                """

    return response_prompt
