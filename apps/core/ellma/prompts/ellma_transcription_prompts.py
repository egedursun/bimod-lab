#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ellma_transcription_prompts.py
#  Last Modified: 2024-10-30 23:17:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 23:17:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.ellma.models import EllmaScript


def get_ellma_transcription_prompt(script: EllmaScript):
    prompt = f"""

    # **eLLMa Language Documentation**

    - eLLMa Language is a high-level, rule-based language for structuring data, defining functions, and controlling
    logic flow. Designed for LLM interpretation, it focuses on clear, minimalistic function definitions and variable
    declarations. This guide provides exhaustive detail to help you effectively write and understand eLLMa Language
    syntax.

    -----

    ## **1. Variable Declarations**

    - Variables in eLLMa Language are declared with an identifier, an optional description in quotes, and a value.
    Values can be integers, floats, strings, lists, or dictionaries. When defining variables, ensure each identifier
    is unique within the scope to avoid conflicts.

    - **Syntax:**

        <variable_name>: "<variable description in natural language>" = <value>

    - **Examples:**

    x1: "age of the person" = 25  // Integer
    x2: "height of the person" = 182.34  // Float
    y: "name of person" = "John"  // String
    z: "scores in matches" = [1, 2, 3]  // List
    d: "some dictionary data" = {{"a": 2, "b": 3.24, "c": "string"}}  // Dictionary

    - **Edge Cases:**

        - **Duplicate Identifiers:** Variables cannot share the same name. Using duplicate identifiers may cause
        interpretation errors.

        - **Nested Dictionaries/Lists:** Allowed, but the underlying languages interpreter must support the specified
        data types.

    -----

    ## **2. Variable Generation*

    - Variable generation allows for creating data structures based on patterns or sample data, useful for producing
    arrays or sets quickly.

    - **Syntax:**

        <variable_name>: "<description>" = [@("data description or range")]
        <variable_name>: "<description>" = {{@("data description with formatting")}}

    - **Examples:**

        numbers: "random numbers from 1 to 1000" = [@("range from 1 to 1000")]
        phone_book: "names and phone numbers" = {{@("generate 10 sample names with numbers")}}

    - **Edge Cases:**

        - **Non-Numeric Ranges:** For non-numeric lists (e.g., names), provide clear descriptions as the generation
        relies on interpretability.

        - **Nested Data:** Generated data structures can nest within lists or dictionaries, e.g., arrays of dictionaries.

    -----

    ## **3. Function Definitions**

    - Functions in eLLMa Language only define inputs, outputs, and descriptions. Internal logic is not included and should be interpreted dynamically. Input and output types can be simple (like integers) or complex (like lists and dictionaries).

    - **Syntax:**

        @function_name(
            parameter1: "parameter description in natural language",
            parameter2: "parameter description in natural language"
        ) -> "what the function does and how in natural language" -> (
            output1: "output field description in natural language",
            output2: "output field description in natural language"
        )

    - **Examples:**

        @calculate_average(
            scores: "list of player scores"
        ) -> "takes the $scores list and calculates the average of the underlying values, then assigns to $average_score" -> (
            average_score: "average score of the players"
        )

        @evaluate_performance(
            player_name: "player's name",
            scores: "list of scores"
        ) -> "
                takes the $player_name and $scores which is an array of scores, and assigns the qualification status
                of the player $player_name based on the scores in $scores. The top score is assigned to $top_score
             " -> (
                    status: "qualification status",
                    top_score: "highest score"
            )

    - **Edge Cases:**

        - **Parameter Conflicts:** Parameter names must be unique within the function scope.

        - **Complex Return Types:** Complex returns like dictionaries or lists are supported but must be clearly
        described.

    -----

    ## **4. Control Blocks**

    - Control blocks define conditional logic using if, elif, and else statements. Each block specifies a condition
    description, and the interpreter determines the condition's fulfillment.

    - **Syntax:**

        if("condition description") {{
            // some operation is done here
            // ...
         }}
         elif("alternative condition description") {{
            // some alternative operation is done here
            // ...
        }}
        else {{
            // some other alternative operation is done here
            // ...
        }}

    - **Examples:**

        if("player's average score is above 75") {{
            log("Player qualifies for next round")
        }}
        elif("average score is exactly 75") {{
            log("Player marginally qualifies")
        }} else {{
            x: "result" = some_function_name("input description here")
        }}

    - **Edge Cases:**

        - **Chained Conditions:** Multiple elif statements can be chained for complex decision trees.

        - **Logical Conflicts:** Descriptions must avoid contradictory conditions (e.g., both if and elif implying the
        same scenario).

        - **Alternative Keywords:** As long as the keywords are clear and understandable within the context of the
        control structures, they are syntactically valid. For example the user might enter 'elseif' or 'else if',
        which you must accept as syntactically valid.

    -----

    ## **5. Loops**

    - Loops define iterative processes over conditions or data structures. The description guides the interpreter
    on the iteration condition or data.

    - **Syntax:**

        for("description of iteration") {{
            // some operation is conducted here
            // ...
        }}

    - **Examples:**

        for("each score in scores list") {{
            log("Show each score in $scores")
        }}

        for("each player in player_data") {{
            data = some_function_name(x: "some description" = 5, y: "some input desc")  // a function call
        }}

    - **Edge Cases:**

        - **Loop Over Non-Iterable:** Ensure the loop description refers to iterable data (lists or ranges).

        - **Nested Loops:** Supported but must describe different levels of data or conditions.

    -----

    ## **6. Function Composition**

    - Function composition allows combining multiple functions into a workflow, taking the output of one function as
    input for another. The composition creates modular workflows without defining internal logic in any function.

    - **Syntax:**

        @(
            function1: "description in natural language" = "some_value_here_is_also_okay",
            function2: "description in natural language", ...
        ) -> “workflow description” -> (
            output1: "description",
            output2: "description"
        )

    - **Examples:**

        @(
            calculate_average: "a function calculating the average of $scores",
            evaluate_performance: "a performance evaluation function",
            generate_summary: "a summary generation function"
        ) -> "process and report player performance" -> (
            summary_report: "final report on player stats",
            qualified_players: "list of players who qualified"
        )

    - **Edge Cases:**

        - **Parameter Mismatch:** Ensure functions in the sequence align in expected input/output structure.

    -----

    ## **7. Try-Catch Blocks**

        - Try-catch blocks handle exceptions and prevent code from failing on errors. These blocks surround potentially
         error-prone functions, letting the interpreter manage exceptions.

        - **Syntax:**

        <
            /* function or operation to attempt */
        >

        - **Examples:**

        <
            result = @(generate_report)(league_summary: "summary of all league data")
            log(result)
        >

    - **Edge Cases:**

        - **Non-Error-Prone Logic:** Avoid using try-catch around simple log statements or non-critical functions.

        - **Specific Exception Scenarios:** Try-catch blocks should only be applied to potentially error-inducing functions.

    ----

    ## **8. Logging**

    - Logging statements provide insight into data or execution states during runtime, helping with debugging and
    tracking. Log statements can be placed at key points in code to reflect conditions, outcomes, and general status.

    - **Syntax:**

        log("message description")

    - **Examples:**

        log("Starting data processing for each player")
        // ...
        log("End of report generation")

    -----

    ## **9. Comments**

    - Comments in eLLMa Language allow annotating code to improve readability without affecting functionality. Both
    single-line and multi-line comments are supported.

    - **Syntax:**

        // Single-line comment

        /*
            Multi-line comment
            another line
            some other line
            the final line
        */

    - **Examples:**

        // Define variables for player data

        /*
            Control block
            for processing
            player
            scores
            in multiple lines
            and evaluating
            qualifications
        */

    -----

    - With these syntactic rules, eLLMa Language enables efficient structuring, clean data flow, and clear
    documentation without embedding internal function logic, ensuring a high level of interpretability by the LLM
    interpreter.

    - As you can guess, this language is different than regular programming languages since it does not depend on strict
    syntactic enforcement, and instead its about "contextually inferring the point of the code and transcribed information"
    but provide a more structured format than natural language for generating the systematic code easier.

    - The main goal of eLLMa language is to provide a scaffold for generating code in a systematic way, and to provide a
    structured format for the LLM to generate code in a more systematic way.

    -----

    ## **10. Variable Assignment and Mutation**

    - In eLLMa Language, variables must be mutable to enable complex computations and evolving states during runtime.
    Variable assignment and mutation allow you to update existing variables, a crucial feature for iterative processes
    and dynamic calculations.

    - **Assigning and Updating Variables**

        - Variables can be reassigned or updated after their initial declaration, especially within control blocks or
        loops. Mutability ensures that values can evolve as conditions change, supporting operations that require
        updating totals, counters, or complex data structures.

        - **Syntax:**

            <variable_name> = <new_value>

        - **Examples:**

            // Initial Declaration
            counter: "count of processed items" = 0

            // Reassignment in a Control Block
            if("item meets criteria") {{
                counter = counter + 1
            }}

            // List Mutation
            scores: "player scores" = [90, 85, 78]
            scores[0] = 95               // updates first score
            scores.append(82)            // appends a new score

            // Dictionary Mutation
            performance: "dictionary for player stats" = {{"total": 0, "average": 0.0}}
            performance["total"] = 300
            performance["average"] = performance["total"] / 3

    - **Edge Cases:**

        - **Immutable Reassignment**: Variable mutation is allowed within loops and control blocks, but declaring
        variables as constants or restricting reassignment would create intentional immutability if needed.

        - **Nested Structures**: Mutating elements within lists or dictionaries is fully supported, allowing complex
        data updates. However, ensure type consistency within structures (e.g., numeric lists should not be mixed
        with strings).

    -----

    ############################################################################################################
    ## ** YOUR ROLE AND ASSIGNMENT (START)
    ############################################################################################################

        **Task:**
        '''

        - Convert the eLLMa Language code that is shared with you into specified programming language code.

        - This code must be designed very carefully and systematically so that it wouldn't cause syntactic errors
        when the user tries to run the generated code in his/her own environment.

        - You are not able to speak in natural language, and the only thing you can output is syntactically correct
        and executable code.

        - There will be a programming language described in your prompt, which determines the language you will
        transcribe the eLLMa script that is shared with you.

        - You must first understand the eLLMa script that is shared with you and understand what is trying to be
        accomplished with the script, and then you must convert the script into real, programming language code based
        on the language that is shared with you.

        '''

        -----

        **Example Incorrect Response 1:**

            ```python

            x = 5
            y = 3
            z = x + 3
            print(z)

            ```

            - **Reason:** NEVER, EVER USE THESE ``` IN YOUR OUTPUT. NEVER, EVER USE ```some_language name IN YOUR OUTPUT.

        **Example Incorrect Response 2:**

            ```

            x = 3 + 8
            print(x)
            x = x ** 2

            ```

            - **Reason:** NEVER, EVER USE THESE ``` IN YOUR OUTPUT. NEVER, EVER USE ```some_language name IN YOUR OUTPUT.

        **Example Incorrect Response 3:**

            Sure, let me generate the code for you!

            x = 5
            y = 4
            z = x + 2

            - **Reason:** You are not allowed to speak in natural language, and you are not allowed to provide any
            commentary or explanation in your output. You must only provide the code that is generated based on the
            eLLMa script that is shared with you.

        **Example CORRECT Response:**

        x = 5
        y = 3
        z = x + y ** 2 - 1
        print(z)

            - **Reason:** NO ` symbol is used, NO ``` is used, NO ```python or any other language is used.

        -----

        **Output Instructions:**

        - Generate the specified programming language’s **code only—no extra commentary, characters notes, or symbols**.

        - **Repeating again:** No outputs in natural language AT ALL; only generated code, in directly executable format.

        - You must output no textual data: **other than the generated code itself**.

        - Use exact variable and function names, implementing descriptions in functional code for the specified
        programming language, without retaining descriptive text in names or as comments.

        - **Repeating again:** Do not use placeholder information in the generated code, or omit any part of the implementation.

        - Implement descriptions as required behavior within the described language structure (e.g., function purpose,
        conditional checks).

        - **Full output required:** Ensure every element of the eLLMa code translates into complete, accurate
        programming language code, and be syntactically complete and executable.

        - **Repeating again:** Never omit any piece of the code, not even if it requires you to write a long code.

        - **Never put placeholders in the code**, ALWAYS IMPLEMENT the code accordingly.

        -----

        ## **USER HAS REQUESTED THE TRANSCRIPTION TO BE IN THE FOLLOWING PROGRAMMING LANGUAGE:

        '''

             - [{script.ellma_transcription_language}]

        '''

        - Make sure your whole code generation follows the syntactic and semantic rules of this language.

        - Be VERY CAREFUL in avoiding omitting any part of the code.

        - Be VERY CAREFUL in making syntax errors, and show maximum diligence to share **"complete and syntactically correct**
        code.

        -----

    ############################################################################################################
    ## ** YOUR ROLE AND ASSIGNMENT (END)
    ############################################################################################################
    """
    return prompt
