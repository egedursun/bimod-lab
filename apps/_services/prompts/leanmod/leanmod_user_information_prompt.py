from django.contrib.auth.models import User


def build_structured_user_information_prompt_leanmod(user: User):
    return f"""
            *USER*

            '''
            Name: {user.profile.first_name} {user.profile.last_name}
                Mail: {user.email}
                City: {user.profile.city}
                Country: {user.profile.country}
                B.Day: {user.profile.birthdate}
            '''

            NOTE: This is info about chatting user.
        """
