import datetime

from django.contrib.auth.models import User


def build_structured_place_and_time_prompt(user: User):
    # Build the prompt
    response_prompt = """
        **PLACE AND TIME AWARENESS:**

        '''
        """
    # Get the location of the user
    user_location = f"""
        Registered Address of the User: {user.profile.address}
        Registered City of the User: {user.profile.city}
        Registered Country of User: {user.profile.country}
        Postal Code of User's Address: {user.profile.postal_code}
        Coordinates: [Infer from the User's Address, City, and Country, giving an approximate.]
    """

    # Get the current time
    current_time = f"""
        ---
        [UTC] Current Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                - The date above has been retrieved with standard datetime.datetime.now() function.
        [Local Time] Current Time: [Infer from the User's Country & City. Do not forget considering the season.]
        '''

        **NOTE**: Make sure to keep the user's location and the current time in mind while responding to the
        user's messages. For the local time, you can infer it from the user's country and city but make sure
        to consider the season (which might affect the Daylight Saving Time). If this part is EMPTY, you can
        respond to the user's messages without any specific considerations.

        **YOUR TOOL USAGE ABILITY:** You are also able to 'design/write' your OWN SQL queries to fetch data from
        the SQL Database Connections if you think none of the custom queries are suitable for the user's request.
        Keep this ability in mind while responding to the user's messages.
        """

    response_prompt += user_location + current_time
    return response_prompt
