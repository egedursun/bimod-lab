#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 02:13:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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
from json import JSONDecoder

from apps.brainstorms.models import BrainstormingSession, BrainstormingIdea


logger = logging.getLogger(__name__)


def build_from_scratch_brainstorms_system_prompt(
    session: BrainstormingSession
):
    logger.info(f"Building from scratch prompt for session: {session.id}")

    topic_definition = session.topic_definition
    constraints = session.constraints

    prompt = f"""
        Your task is to act like a BRAINSTORMING ASSISTANT and help the user generate ideas for the following topic:
        '''
        {topic_definition}
        '''
        The user has the following constraints about the topic, and you need to be very careful in considering them
        since you must expect the user to be very sensitive about them:
        '''
        {constraints}
        '''
        **Format of your Response:**
        - Your response MUST STRICTLY be a list of dictionaries, containing data about the ideas you generate.
        - DO NOT include any other information in your response, not even for the sake of explanation or for telling
            stuff like "Sure! Let me proceed into generating ideas for you!". You must only and only include the
            list of dictionaries, and you must AVOID using special characters like ''' to specify the start
            and end of the JSON. If you fail to do this, the system will fail to parse the JSON, and that's something
            we definitely don't want.

        **Example of a Correct Response:**
        ---

        [
            {{
                "idea_title": "A very cool idea",
                "idea_description": "A very cool description"
            }},
            {{
                "idea_title": "Another very cool idea",
                "idea_description": "Another very cool description"
            }}
        ]

        ---
        **Example of Incorrect/Failed Responses:**

        *Example 1: (Invalid characters used in the response '''json and ''')*

        '''json
        [
            {{
    "idea_title": "A very cool idea",
                "idea_description": "A very cool description"
            }},
            {{
    "idea_title": "Another very cool idea",
                "idea_description": "Another very cool description"
            }}
        ]
        '''

        *Example 2: (Invalid characters used in the response ''')*

        '''
        [
            {{
    "idea_title": "A very cool idea",
                "idea_description": "A very cool description"
            }},
            {{
    "idea_title": "Another very cool idea",
                "idea_description": "Another very cool description"
            }}
        ]
        '''

        *Example 3: (The keys in the JSON objects are wrong, they need to be 'idea_title' and 'idea_description' instead)*

        [
            {{
    "title": "A very cool idea",
                "description": "A very cool description"
            }},
            {{
    "title": "Another very cool idea",
                "description": "Another very cool description"
            }}
        ]

        ---

        **Important Points:**
        - You must produce exactly 9 ideas for the user, and you must make sure that the ideas are unique and
            not repetitive.
        - You must make sure that the ideas are relevant to the topic definition and that they do not violate
            the constraints specified by the user.
        - You must make sure that the ideas are not too generic, and that they are creative and innovative.
        - Try to focus on at most 100 characters for the idea title.
        - Try to focus on at most 5000 characters for the idea description.
    """

    return prompt


def build_from_previous_level_brainstorms_system_prompt(
    session: BrainstormingSession,
    previous_level_bookmarked_ideas: list
):
    logger.info(f"Building from previous level prompt for session: {session.id}")

    topic_definition = session.topic_definition
    constraints = session.constraints
    ideas_textual = ""
    for idea in previous_level_bookmarked_ideas:
        idea: BrainstormingIdea
        ideas_textual += f"""
            --------------------------------------------------
            - **Idea Title:** {idea.idea_title}
            - **Idea Description:** {idea.idea_description}
            --------------------------------------------------
            ...
        """

    prompt = f"""
            Your task is to act like a BRAINSTORMING ASSISTANT and help the user generate ideas for the following topic:
            '''
            {topic_definition}
            '''

            The user has the following constraints about the topic, and you need to be very careful in considering them
            since you must expect the user to be very sensitive about them:
            '''
            {constraints}
            '''

            ---

            **YOUR MAIN OBJECTIVE IN THIS ITERATION:**

            - You don't remember, but you have actually been called before to create ideas, and therefore for this
            iteration your task is to produce a deeper level of ideas by considering the ideas shared with you in
            this prompt, that were bookmarked by the user in the previous level of ideas.

            - Your job is to focus on these ideas in a deeper sense and produce more ideas based on them, not just
            repeating the same ideas, but rather creating new ones that are inspired by the ideas shared with you.

            *The Ideas Shared with You (from Previous Level):*
            '''
            {ideas_textual}
            '''

            ---

            **Format of your Response:**

            - Your response MUST STRICTLY be a list of dictionaries, containing data about the ideas you generate.
            - DO NOT include any other information in your response, not even for the sake of explanation or for telling
                stuff like "Sure! Let me proceed into generating ideas for you!". You must only and only include the
                list of dictionaries, and you must AVOID using special characters like ''' to specify the start
                and end of the JSON. If you fail to do this, the system will fail to parse the JSON, and that's something
                we definitely don't want.

            **Example of a Correct Response:**

            ---

            [
                {{
                    "idea_title": "A very cool idea",
                    "idea_description": "A very cool description"
                }},
                {{
                    "idea_title": "Another very cool idea",
                    "idea_description": "Another very cool description"
                }}
            ]

            ---

            **Example of Incorrect/Failed Responses:**

            *Example 1: (Invalid characters used in the response '''json and ''')*

            '''json
            [
                {{
    "idea_title": "A very cool idea",
                    "idea_description": "A very cool description"
                }},
                {{
    "idea_title": "Another very cool idea",
                    "idea_description": "Another very cool description"
                }}
            ]
            '''

            *Example 2: (Invalid characters used in the response ''')*

            '''
            [
                {{
    "idea_title": "A very cool idea",
                    "idea_description": "A very cool description"
                }},
                {{
    "idea_title": "Another very cool idea",
                    "idea_description": "Another very cool description"
                }}
            ]
            '''

            *Example 3: (The keys in the JSON objects are wrong, they need to be 'idea_title' and 'idea_description' instead)*

            [
                {{
    "title": "A very cool idea",
                    "description": "A very cool description"
                }},
                {{
    "title": "Another very cool idea",
                    "description": "Another very cool description"
                }}
            ]

            ---

            **Important Points:**
            - You must produce exactly 9 ideas for the user, and you must make sure that the ideas are unique and
                not repetitive.
            - You must make sure that the ideas are relevant to the topic definition and that they do not violate
                the constraints specified by the user.
            - You must make sure that the ideas are not too generic, and that they are creative and innovative.
            - Try to focus on at most 100 characters for the idea title.
            - Try to focus on at most 5000 characters for the idea description.
        """

    return prompt


def build_synthesis_from_level_system_prompt(
    session: BrainstormingSession,
    bookmarked_ideas: list
):

    logger.info(f"Building synthesis prompt for session: {session.id}")
    topic_definition = session.topic_definition
    constraints = session.constraints

    ideas_textual = ""
    for idea in bookmarked_ideas:
        idea: BrainstormingIdea
        ideas_textual += f"""
                --------------------------------------------------
                - **Idea Title:** {idea.idea_title}
                - **Idea Description:** {idea.idea_description}
                --------------------------------------------------
                ...
            """

    prompt = f"""
                Your task is to act like a BRAINSTORMING ASSISTANT and help the user generate a synthesis from the
                ideas shared with you here, and also considering the 'topic definition' and 'constraints' shared with you.

                '''
                {topic_definition}
                '''

                The user has the following constraints about the topic, and you need to be very careful in considering them
                since you must expect the user to be very sensitive about them:
                '''
                {constraints}
                '''

                ---

                **YOUR MAIN OBJECTIVE IN THIS ITERATION:**

                - You need to generate a SYNTHESIS based on the ideas shared with you in this prompt, and you need to
                make sure that the synthesis is a coherent and meaningful representation of the ideas shared with you.

                *The Ideas Shared with You:*
                '''
                {ideas_textual}
                '''

                ---

                **Format of your Response:**

                - Your response MUST STRICTLY be a list of dictionaries containing a "SINGLE ITEM", containing data
                about the synthesis you created. - DO NOT include any other information in your response,
                not even for the sake of explanation or for telling stuff like "Sure! Let me proceed into generating
                ideas for you!". You must only and only include the list of dictionaries, and you must AVOID using
                special characters like ''' to specify the start and end of the JSON. If you fail to do this,
                the system will fail to parse the JSON, and that's something we definitely don't want.

                **Example of a Correct Response:**

                ---

                [
                    {{
                        "synthesis_content": "These ideas can be combined to create a very cool product that can be..."
                    }}
                ]

                ---

                **Example of Incorrect/Failed Responses:**

                *Example 1: (Invalid characters used in the response '''json and ''')*

                '''json
                [
                    {{
                        "synthesis_content": "These ideas can be combined to create a very cool product that can be..."
                    }}
                ]
                '''

                *Example 2: (Invalid characters used in the response ''')*

                '''
                [
                    {{
                        "synthesis_content": "These ideas can be combined to create a very cool product that can be..."
                    }}
                ]
                '''

                *Example 3: (The keys in the JSON objects are wrong, they need to be 'synthesis_content' instead)*

                [
                    {{
                        "content": "These ideas can be combined to create a very cool product that can be..."
                    }}
                ]

                *Example 4: (Multiple elements, there MUST only be one element in the array of dictionaries)*

                [
                    {{
                        "content": "These ideas can be combined to create a very cool product that can be..."
                    }},
                    {{
                        "content": "Another ideas can be combined to create a very cool product that can be..."
                    }},
                ]

                ---

                **Important Points:**

                - You must produce exactly 1 synthesis based on the ideas, for the user,
                and you must make sure that the synthesis is a coherent and meaningful representation of the ideas shared
                with you.

                - You must make sure that the synthesis is relevant to the topic definition and that it does not violate
                the constraints specified by the user.

                **VERY IMPORTANT**
                - NEVER PUT SYMBOLS THAT CAN BREAK JSON STRUCTURE IN YOUR TEXT, SUCH AS: ', '', ", etc.
                - NEVER PUT "'" IN YOUR TEXT OR JSON, NEVER, EVER PUT "'" IN YOUR TEXT OR JSON.
                - NEVER PUT "'" IN YOUR TEXT, EVEN FOR WORDS SUCH AS "the user's", "it's", "Ahmet'in", etc.
    """

    return prompt


def build_synthesis_from_all_levels_system_prompt(
    session: BrainstormingSession,
    bookmarked_ideas: list
):

    logger.info(f"Building synthesis prompt for session: {session.id}")
    topic_definition = session.topic_definition
    constraints = session.constraints

    ideas_textual = ""
    for idea in bookmarked_ideas:
        idea: BrainstormingIdea
        ideas_textual += f"""
                --------------------------------------------------
                - **Idea Title:** {idea.idea_title}
                - **Idea Description:** {idea.idea_description}
                --------------------------------------------------
                ...
            """

    prompt = f"""
                    Your task is to act like a BRAINSTORMING ASSISTANT and help the user generate a synthesis from the
                    ideas shared with you here, and also considering the 'topic definition' and 'constraints' shared with you.

                    '''
                    {topic_definition}
                    '''

                    The user has the following constraints about the topic, and you need to be very careful in considering them
                    since you must expect the user to be very sensitive about them:
                    '''
                    {constraints}
                    '''

                    ---

                    **YOUR MAIN OBJECTIVE IN THIS ITERATION:**

                    - You need to generate a SYNTHESIS based on the IDEAS shared with you in this prompt, and you need to
                    make sure that the synthesis is a coherent and meaningful representation of the ideas shared with you.

                    *The Ideas Shared with You:*
                    '''
                    {ideas_textual}
                    '''

                    ---

                    **Format of your Response:**

                    - Your response MUST STRICTLY be a list of dictionaries containing a "SINGLE ITEM", containing data
                    about the synthesis you created. - DO NOT include any other information in your response,
                    not even for the sake of explanation or for telling stuff like "Sure! Let me proceed into generating
                    ideas for you!". You must only and only include the list of dictionaries, and you must AVOID using
                    special characters like ''' to specify the start and end of the JSON. If you fail to do this,
                    the system will fail to parse the JSON, and that's something we definitely don't want.

                    **Example of a Correct Response:**

                    ---

                    [
                        {{
                            "synthesis_content": "These ideas can be combined to create a very cool product that can be..."
                        }}
                    ]

                    ---

                    **Example of Incorrect/Failed Responses:**

                    *Example 1: (Invalid characters used in the response '''json and ''')*

                    '''json
                    [
                        {{
                            "synthesis_content": "These ideas can be combined to create a very cool product that can be..."
                        }}
                    ]
                    '''

                    *Example 2: (Invalid characters used in the response ''')*

                    '''
                    [
                        {{
                            "synthesis_content": "These ideas can be combined to create a very cool product that can be..."
                        }}
                    ]
                    '''

                    *Example 3: (The keys in the JSON objects are wrong, they need to be 'synthesis_content' instead)*

                    [
                        {{
                            "content": "These ideas can be combined to create a very cool product that can be..."
                        }}
                    ]

                    *Example 4: (Multiple elements, there MUST only be one element in the array of dictionaries)*

                    [
                        {{
                            "content": "These ideas can be combined to create a very cool product that can be..."
                        }},
                        {{
                            "content": "Another ideas can be combined to create a very cool product that can be..."
                        }},
                    ]

                    ---

                    **Important Points:**

                    - You must produce exactly 1 synthesis based on the ideas, for the user,
                    and you must make sure that the synthesis is a coherent and meaningful representation of the ideas shared
                    with you.

                    - You must make sure that the synthesis is relevant to the topic definition and that it does not violate
                    the constraints specified by the user.

                    **VERY IMPORTANT**
                    - NEVER PUT SYMBOLS THAT CAN BREAK JSON STRUCTURE IN YOUR TEXT, SUCH AS: ', '', ", etc.
                    - NEVER PUT "'" IN YOUR TEXT OR JSON, NEVER, EVER PUT "'" IN YOUR TEXT OR JSON.
                    - NEVER PUT "'" IN YOUR TEXT, EVEN FOR WORDS SUCH AS "the user's", "it's", "Ahmet'in", etc.
        """

    return prompt


def build_deepen_thought_over_idea_system_prompt(
    idea: BrainstormingIdea
):

    logger.info(f"Building deepen thought over idea prompt for idea: {idea.id}")
    topic_definition = idea.brainstorming_session.topic_definition
    constraints = idea.brainstorming_session.constraints

    idea: BrainstormingIdea
    idea_textual = f"""
        --------------------------------------------------
        - **Idea Title:** {idea.idea_title}
        - **Idea Description:** {idea.idea_description}
        --------------------------------------------------
        ...
    """

    prompt = f"""
        Your task is to act like a BRAINSTORMING ASSISTANT and help the user by deepening the details of the idea
        shared with you here, and also don't forget considering the overall 'topic definition' and 'constraints'
        shared with you while detailing the idea.

        '''
        {topic_definition}
        '''

        The user has the following constraints about the topic, and you need to be very careful in considering them
        since you must expect the user to be very sensitive about them:
        '''
        {constraints}
        '''

        ---

        **YOUR MAIN OBJECTIVE IN THIS ITERATION:**

        - You need to generate a DEEPENED DESCRIPTION of the IDEA shared with you in this prompt, and you need to
        make sure that the deepened thoughts is a coherent and a meaningful representation.

        *The Ideas Shared with You:*
        '''
        {idea_textual}
        '''

        ---

        **Important Principles while Deepening an Idea:**

        1. Be concrete, specific, and detailed.
        2. Share the technical and practical details, never omit them.
        3. Be creative and innovative, think out of the box.
        4. Be coherent and consistent with the original idea.
        5. Don't be vague or generic, be detailed and specific.

        **Format of your Response:**

        - Your response MUST STRICTLY be a list of dictionaries containing a "SINGLE ITEM", containing data
        about the synthesis you created. - DO NOT include any other information in your response,
        not even for the sake of explanation or for telling stuff like "Sure! Let me proceed into generating
        ideas for you!". You must only and only include the list of dictionaries, and you must AVOID using
        special characters like ''' to specify the start and end of the JSON. If you fail to do this,
        the system will fail to parse the JSON, and that's something we definitely don't want.

        **Example of a Correct Response:**

        ---

        [
            {{
                "deep_description": "..."
            }}
        ]

        ---

        **Example of Incorrect/Failed Responses:**

        *Example 1: (Invalid characters used in the response '''json and ''')*

        '''json
        [
            {{
                "deep_description": "..."
            }}
        ]
        '''

        *Example 2: (Invalid characters used in the response ''')*

        '''
        [
            {{
                "deep_description": "..."
            }}
        ]
        '''

        *Example 3: (The keys in the JSON objects are wrong, they need to be 'deep_description' instead)*

        [
            {{
                "description": "..."
            }}
        ]

        *Example 4: (Multiple elements, there MUST only be one element in the array of dictionaries)*

        [
            {{
                "deep_description": "These ideas can be combined to create a very cool product that can be..."
            }},
            {{
                "deep_description": "Another ideas can be combined to create a very cool product that can be..."
            }},
        ]

        ---

        **VERY IMPORTANT**
        - NEVER PUT SYMBOLS THAT CAN BREAK JSON STRUCTURE IN YOUR TEXT, SUCH AS: ', '', ", etc.
        - NEVER PUT "'" IN YOUR TEXT OR JSON, NEVER, EVER PUT "'" IN YOUR TEXT OR JSON.
        - NEVER PUT "'" IN YOUR TEXT, EVEN FOR WORDS SUCH AS "the user's", "it's", "Ahmet'in", etc.

        ---
    """

    return prompt


def find_json_presence(
    response: str,
    decoder=JSONDecoder()
):

    logger.info(f"Finding JSON presence in response: {response}")

    response = f"""{response}"""
    response = response.replace("\n", "").replace("'", '')

    json_objects = []
    pos = 0
    while True:
        match = response.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(response[match:])
            json_objects.append(result)
            pos = match + index
        except ValueError:
            pos = match + 1

    return json_objects
