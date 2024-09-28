from apps._services.tools.utils import ToolTypeNames


def build_structured_tool_prompt__custom_code_execution():
    response_prompt = f"""
            **TOOL**: Custom Function Execution Tool

            - The Custom Function Execution Tool is a tool that allows you to execute custom functions that are
            defined in the system. These custom functions can be used to perform various operations such as
            data processing, data analysis, data transformation, and more. You can use this tool to execute custom
            functions that are defined in the system and receive the results of the execution. The custom functions
            that you can execute using this tool are defined by the system administrators and are available for
            execution in the system, and you only need to call these functions properly by providing the necessary
            input data and the function ID.

            - The standardized format for the dictionary that you will output to use the Custom Function Execution
            Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.CUSTOM_FUNCTION_EXECUTOR}",
                    "parameters": {{
                        "custom_function_reference_id": "...",
                        "input_data": {{
                            "input_variable_name": "input_variable_value_string",
                            "input_variable_name": 284.32948,
                            "input_variable_name": [1, 2, 3, 4, 5],
                            "input_variable_name": {{
                                "dict_variable_sample": "value",
                                "dict_variable_sample": 284.32948,
                                ...
                            }}
                            ...
                        }}
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "custom_function_reference_id" field should be the ID of the custom function that you
            would like to execute. You can find the ID of the custom function that you would like to execute by checking the
            custom functions that are available in the system. The "input_data" field should be a dictionary that contains
            the input data that you would like to provide to the custom function. The input data should be provided in the
            dictionary format, where the keys are the input variable names of the custom function, and the values are the
            input values that you would like to provide to the custom function.


            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "custom_function_reference_id", provide the ID of the custom function that you would like to execute.
            You can find the ID of the custom function by checking the custom functions that are available in the system.

            2. For "input_data", provide a dictionary that contains the input data that you would like to provide to the
            custom function. The keys of the dictionary should be the input variable names of the custom function, and the
            values should be the input values that you would like to provide to the custom function.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words.
        """
    return response_prompt
