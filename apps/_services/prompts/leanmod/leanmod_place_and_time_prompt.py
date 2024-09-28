from datetime import datetime

from django.contrib.auth.models import User


def build_structured_place_and_time_prompt_leanmod(user: User):
    # Build the prompt
    response_prompt = """
            *PLACE AND TIME*

            '''
            """
    # Get the location of the user
    user_location = f"""
            User Address: {user.profile.address}
                City: {user.profile.city}
                Country: {user.profile.country}
                Postal Code: {user.profile.postal_code}
                Coordinates: [Infer on Address]
        """

    # Get the current time
    current_time = f"""
            ---
            [UTC] Current Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    - Retrieved by datetime.datetime.now().
            [Local] Current Time: [Infer on Country/City & Date]
            '''

            NOTE: For local time, infer it from user's country/city and don't forget the Daylight Saving Time.
            """

    response_prompt += user_location + current_time
    return response_prompt
