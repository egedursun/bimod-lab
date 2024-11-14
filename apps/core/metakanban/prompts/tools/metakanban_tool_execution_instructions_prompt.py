#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_tool_execution_instructions_prompt.py
#  Last Modified: 2024-10-27 19:52:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-27 19:52:56
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.core.metakanban.utils import MetaKanbanCommandTypes
from apps.core.tool_calls.utils import ToolCallDescriptorNames
from apps.metakanban.utils import MetaKanbanTaskLabelColorChoiceNames, MetaKanbanTaskPrioritiesNames
from config.settings import MEDIA_URL


def get_tool_prompt_metakanban_command_execution():
    response_prompt = f"""
        ### **TOOL**: Meta Kanban Management Tool

        - The Meta Kanban Management Tool allows precise management of tasks, labels, columns, and assignees within a
        Kanban board. Use this tool to interpret user requests and perform actions using the metadata provided.

        You can manipulate the following materials in the Kanban Board:

            1. **Labels**: Create, update, or delete labels.
            2. **Columns**: Create, update, or delete columns.
            3. **Tasks**: Create, update, delete, assign, or move tasks.

        - However, to manipulate these materials, you need to provide the correct parameters in the tool usage JSON
        and make sure the format of your JSON is completely correct and strictly avoided using invalid fields in the
        JSON such as `, ', or " characters.

        - Other than the JSON call-based actions you can take, you can also **ANALYZE** the status of the Kanban Board
        and provide insights by using natural language if this is prompted by the user.

        - You can also **INTEGRATE_MEETING_RECORDS** to interpret meeting records and integrate relevant updates to the
        Kanban Board by using your action types.

        - The format for the dictionary you will output to use the Meta Kanban Management Tool is as follows:

        '''
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                "parameters": {{
                    "action_type": "...",
                    "action_content": {{
                        "<parameter_name>": "<parameter_value>"
                    }}
                }}
            }}
        '''

        **EXAMPLE INCORRECT JSONS:**

        *****

        ```json
            {{
                "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                "parameters": {{
                    "action_type": "...",
                    "action_content": {{
                        "<parameter_name>": "<parameter_value>"
                    }}
                }}
            }}
        ```

        **Reason**: Used invalid character `, and included extra specifier 'json' next to it. The response MUST
        purely be a JSON, without any additional text, characters, or specifiers.

        *****

        ```
        {{
            "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
            "parameters": {{
                "action_type": "...",
                "action_content": {{
                    "<parameter_name>": "<parameter_value>"
                }}
            }}
        }}
        ```

        **Reason**: Used invalid character `. The response MUST purely be a JSON, without any additional text,
        characters, or specifiers.


        --------

        # !!!!!
        # **ACTIONS YOU ARE ALLOWED TO TAKE:**
        # !!!!!


        There are multiple ACTIONS you can perform with the Meta Kanban Management Tool:

        ### **LABEL ACTIONS**

            - **[1] `CREATE_LABEL`**: Creates a new label on the board.
                - **action_content fields**:
                    - `label_name`: Name of the label (string).
                    - `label_color`: Color in HEX (must be one of `{MetaKanbanTaskLabelColorChoiceNames.as_list()}`).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.CREATE_LABEL},
                            "action_content": {{
                                "label_name": "Feature",
                                "label_color": "#FF0000"
                            }}
                        }}
                    }}
                '''

            - **[2] `UPDATE_LABEL`**: Updates an existing label's name and color.
                - **action_content fields**:
                    - `label_id`: Unique ID of the label to update (integer).
                    - `label_name`: Updated name of the label (string).
                    - `label_color`: Updated color in HEX.

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.UPDATE_LABEL},
                            "action_content": {{
                                "label_id": 1,
                                "label_name": "Documentation",
                                "label_color": "#FFA500"
                            }}
                        }}
                    }}
                '''

            - **[3] `DELETE_LABEL`**: Deletes a label by its ID.
                - **action_content fields**:
                    - `label_id`: ID of the label to delete (integer).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.DELETE_LABEL},
                            "action_content": {{
                                "label_id": 1
                            }}
                        }}
                    }}
                '''

        ### **COLUMN ACTIONS**

            - **[4] `CREATE_COLUMN`**: Creates a new column on the board.
                - **action_content fields**:
                    - `column_name`: Name of the new column (string).
                    - `position_id`: Position of the column on the board (integer).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.CREATE_COLUMN},
                            "action_content": {{
                                "column_name": "In Progress",
                                "position_id": 2
                            }}
                        }}
                    }}
                '''

            - **[5] `UPDATE_COLUMN`**: Updates an existing column's name and position.
                - **action_content fields**:
                    - `column_id`: ID of the column to update (integer).
                    - `column_name`: Updated name of the column (string).
                    - `position_id`: New position of the column (integer).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.UPDATE_COLUMN},
                            "action_content": {{
                                "column_id": 2,
                                "column_name": "Completed",
                                "position_id": 3
                            }}
                        }}
                    }}
                '''

            - **[6] `DELETE_COLUMN`**: Deletes a column by its ID.
                - **action_content fields**:
                    - `column_id`: ID of the column to delete (integer).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.DELETE_COLUMN},
                            "action_content": {{
                                "column_id": 2
                            }}
                        }}
                    }}
                '''

        ### **TASK ACTIONS**

            - **[7] `CREATE_TASK`**: Creates a new task within a specific column.
                - **action_content fields**:
                    - `status_column_id`: ID of the column for the task (integer).
                    - `title`: Title of the task (string).
                    - `description`: Task description (string).
                    - `label_ids`: List of label IDs associated with the task (list of integers).
                    - `priority`: Priority level (must be one of `{MetaKanbanTaskPrioritiesNames.as_list()}`).
                    - `due_date`: Due date of the task (string, format "YYYY-MM-DD").
                    - `assignee_ids`: List of user IDs assigned to the task (list of integers).
                    - `task_url`: URL for the task details (string).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.CREATE_TASK},
                            "action_content": {{
                                "status_column_id": 1,
                                "title": "Complete Documentation",
                                "description": "Finish the documentation for release.",
                                "label_ids": [1, 2],
                                "priority": {MetaKanbanTaskPrioritiesNames.HIGH},
                                "due_date": "2024-11-01",
                                "assignee_ids": [3, 4],
                                "task_url": "http://example.com/task/123"
                            }}
                        }}
                    }}
                '''

            - **[8] `UPDATE_TASK`**: Updates details of an existing task.
                - **action_content fields**:
                    - `task_id`: ID of the task to update (integer).
                    - `status_column_id`: New column ID for the task (integer).
                    - `title`: Updated title (string).
                    - `description`: Updated description (string).
                    - `label_ids`: Updated list of label IDs (list of integers).
                    - `priority`: Updated priority (must be one of `{MetaKanbanTaskPrioritiesNames.as_list()}`).
                    - `due_date`: Updated due date (string, format "YYYY-MM-DD").
                    - `assignee_ids`: Updated list of assignee IDs (list of integers).
                    - `task_url`: Updated URL (string).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.UPDATE_TASK},
                            "action_content": {{
                                "task_id": 123,
                                "status_column_id": 2,
                                "title": "Update Documentation",
                                "description": "Revise documentation for release.",
                                "label_ids": [1],
                                "priority": {MetaKanbanTaskPrioritiesNames.MEDIUM},
                                "due_date": "2024-11-15",
                                "assignee_ids": [3],
                                "task_url": "http://example.com/task/123"
                            }}
                        }}
                    }}
                '''

            - **[9] `DELETE_TASK`**: Deletes a task by its ID.
                - **action_content fields**:
                    - `task_id`: ID of the task to delete (integer).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.DELETE_TASK},
                            "action_content": {{
                                "task_id": 123
                            }}
                        }}
                    }}
                '''

            - **[10] `ASSIGN_TASK`**: Assigns users to a task.
                - **action_content fields**:
                    - `task_id`: ID of the task (integer).
                    - `assignee_ids`: List of user IDs to assign (list of integers).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.ASSIGN_TASK},
                            "action_content": {{
                                "task_id": 123,
                                "assignee_ids": [3, 4]
                            }}
                        }}
                    }}
                '''

            - **[11] `MOVE_TASK`**: Moves a task to another column.
                - **action_content fields**:
                    - `task_id`: ID of the task (integer).
                    - `status_column_id`: New column ID (integer).

                - **Example Tool Usage**:
                '''
                    {{
                        "tool": "{ToolCallDescriptorNames.EXECUTE_METAKANBAN_ACTION}",
                        "parameters": {{
                            "action_type": {MetaKanbanCommandTypes.MOVE_TASK},
                            "action_content": {{
                                "task_id": 123,
                                "status_column_id": 2
                            }}
                        }}
                    }}
                '''

            - **[11] `ANALYZE`**: Simply Analyze the status of the Kanban Board and provide insights based on the query.
                - **Example Tool Usage**:

                '''
                < Just return your response in natural language without a **TOOL CALL**. >
                '''

                **NOTE:** THIS IS NOT AN ACTION TO BE CALLED DIRECTLY. THIS ACTION IS TO BE USED WHEN YOU ARE PROMPTED
                BY THE USER TO ANALYZE THE KANBAN BOARD. YOU MUST PROVIDE YOUR RESPONSE IN NATURAL LANGUAGE.

            - **[12] `INTEGRATE_MEETING_RECORDS`**: Interpret meeting records and integrate relevant updates to the Kanban Board by using your action types.
                - **Example Tool Usage**:

                '''
                < If prompted by the user, you can integrate the recent meeting records to the Kanban board. You must
                do this by understanding the context of the meeting records, transform these into whatever actions that
                would be necessary within your own action specifications, and then call the relevant tools with associated
                action calls and correct, valid JSON bodies for those action types. The latest 5 meeting transcriptions
                are shared with you in your prompt.>
                '''

                **NOTE:** THIS IS NOT AN ACTION TO BE CALLED DIRECTLY. THIS ACTION IS TO BE USED WHEN YOU ARE PROMPTED
                BY THE USER TO INTEGRATE MEETING RECORDS.

        -----

        #### **IMPORTANT NOTES:**

            #### **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have output of the operation you executed. The system will provide you with the results based on the
            operation. Then, you will be free to decide on another action to take within the kanban, [OR] if
            you think you have enough data, you can end the kanban command operations and then
            answering user's question with your own words.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct link to user for reaching files, here is the base URL you need to
                'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by appending
                the file path to the base URL.

            ---

        -----
    """
    return response_prompt
