from django.contrib.auth.models import User


def build_structured_user_information_prompt(user: User):
    return f"""
        **USER INFORMATION:**

        '''
        User's Full Name: {user.profile.first_name} {user.profile.last_name}
        User's Email: {user.email}
        User's City: {user.profile.city}
        User's Country: {user.profile.country}
        User's Birthday: {user.profile.birthdate}
        '''

        **NOTE**: This is the information about the user you are currently chatting with. Make sure to keep
        this information in mind while responding to the user's messages. If this part is EMPTY, you can
        respond to the user's messages without any specific considerations.
    """
