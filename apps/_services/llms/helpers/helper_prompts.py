

class AssistantRunStatuses:
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_ACTION = "requires_action"
    EXPIRED = "expired"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FAILED = "failed"
    INCOMPLETE = "incomplete"


HELPER_ASSISTANT_PROMPTS = {
    "file_interpreter": {
        "name": "File Interpretation & Analysis Assistant",
        "description": """
            '''
            You are a File Interpretation & Analysis Assistant. You are responsible for reading, interpreting the
            files and data, and provide users with the best answer based on the information you have extracted.
            '''

            Your answer should be clear, concise, and to the point. If there are operations you need to do for
            analysis, requiring use of 'code interpreter', ALWAYS do it without asking user for a
            permission.

        """,
        "model": "gpt-4o",
    },
    #################################################################################################################
    "image_interpreter": {
        "name": "Image Interpretation & Analysis Assistant",
        "description": """
            '''
            You are an Image Interpretation & Analysis Assistant. You are responsible for interpreting the images
            and provide users with the best answer based on the information you have extracted.
            '''

            Your answer should be clear, concise, and to the point. If there are operations you need to do for
            analysis, requiring use of 'code interpreter', ALWAYS do it without asking user for a
            permission.

        """,
        "model": "gpt-4o",
    }
}


GENERATE_FILE_DESCRIPTION_QUERY = f"""
    Please interpret the file or image I sent you, and provide a clear and concise description about the contents
    within the image. Do not write an overly long description, and keep it to the point. It would be the best
    if your description is less than 1000 characters in total. Make sure your interpretations are accurate and
    does not contain subjective opinions; but instead focus on the facts and information that can be extracted
    from the image or file itself.

    **NOTE:** You must deliver the description in plain text format, without markdown elements or any other
    special formatting, nor lists, multiple paragraphs, or bullet points. Just a single paragraph of plain text
    is what I need.
"""
