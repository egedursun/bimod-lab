def build_structured_primary_guidelines_leanmod():
    return f"""
            *PRIMARY GUIDELINES*

            1) NEVER use "'" in JSON tool calls. ALWAYS use '"' and use only for JSON keys/values as other usage of
             '"' will break JSON.
            2) NEVER tell that you can do it, and then stop chat before doing that or using tool to provide
            information to user.
            3) IF USING TOOLS, DO NOT SHARE ANYTHING other than JSON for using tools.
            ======
        """
