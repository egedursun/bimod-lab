from django.contrib.auth.models import User

from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection


def build_browsing_datasource_prompt(assistant: Assistant, user: User):
    # Gather the Browsing datasource connections of the assistant
    browsing_datasources = DataSourceBrowserConnection.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **BROWSING CONNECTIONS:**

            '''
            """

    for i, browsing_datasource in enumerate(browsing_datasources):
        response_prompt += f"""
                [Browsing Datasource ID: {browsing_datasource.id}]
                    Browser Type: {browsing_datasource.browser_type}
                    Name: {browsing_datasource.name}
                    Description: {browsing_datasource.description}
                    Data Selectivity: {browsing_datasource.data_selectivity}
                    Minimum Investigation Sites: {browsing_datasource.minimum_investigation_sites}
                    Whitelisted Extensions: {browsing_datasource.whitelisted_extensions}
                    Blacklisted Extensions: {browsing_datasource.blacklisted_extensions}
                    Reading Abilities: {browsing_datasource.reading_abilities}
                    Created At: {browsing_datasource.created_at}
                    Updated At: {browsing_datasource.updated_at}
                """

    response_prompt += """
            -------

            '''

            **NOTE**: These are the browsing datasource connections available for use. You can use these connections
            to execute browsing operations on the web. You can connect to a browser, close a browser, search for
            information on the web, and click on URLs in search results. Make sure you are using the correct
            browsing datasource connection ID when executing browsing operations.

            - Description value is shared with you for you to have an idea about the browsing datasource connection
            and the overall goal of the browsing operations within the context of this connection.

            **VERY IMPORTANT NOTE ABOUT 'BROWSING MODES':**
            - The browsing datasource connections have three modes: 'standard', 'whitelist', and 'blacklist'.

            [1] If the connection does not have any 'whitelisted_extensions' or 'blacklisted_extensions',
            the mode is 'standard'. In that case, the browsing operations are executed as usual.

            [2] If the connection has 'whitelisted_extensions' defined, the mode is 'whitelist'. In that case,
            only the URLs with the extensions defined in the 'whitelisted_extensions' field are allowed. Therefore,
            it is not expected for you to be able to see URLs with extensions that are not defined in the
            'whitelisted_extensions' field. Even if you see any, NEGLECT them.

            [3] If the connection has 'blacklisted_extensions' defined, the mode is 'blacklist'. In that case,
            the URLs with the extensions defined in the 'blacklisted_extensions' field are not allowed. Therefore,
            it is not expected for you to be able to see URLs with extensions that are defined in the
            'blacklisted_extensions' field. Even if you see any, NEGLECT them.

            [4] If the connection has both 'whitelisted_extensions' and 'blacklisted_extensions' defined, the mode is
            'blacklist', at least it will be treated this way. Proceed as you normally do, but after you answer the
            users question, let him/her know about the issue and the mutually exclusive nature of the two fields.

            [5] The 'minimum_investigation_sites' field defines the minimum number of sites to investigate before
            returning the results to the user. Make sure you have investigated at least the number of sites defined
            in the 'minimum_investigation_sites' field before returning the results to the user. If you don't have
            enough resources even if you have tried to look for different pages of the search engine, you can return
            the results to the user with the information you have gathered so far and let him/her know about the
            situation.

            [6] The 'reading_abilities' field defines the 'HTML Cleaning Strategy' that the browser uses in the background,
            thus it affects your ability to see and interpret the HTML content of the web pages. The fields labeled
            as 'True' in the 'reading_abilities' field are the ones that are "hidden/removed" from the HTML content
            by the LXML-HTML Cleaner. Therefore, you should not expect to see those fields in the HTML content.

            **VERY IMPORTANT NOTE ABOUT 'data_selectivity':**
            - The 'data_selectivity' field in the browsing datasource connection defines the data selectivity
            of the browsing operations. The data selectivity is a value between 0.0 and 1.0.

            - If the 'data_selectivity' is 1.0, the browsing operations are executed with the highest data selectivity.
            In that case, you need to be VERY STRICT about trusting the data you see in the browsing operations. You
            MUST only trust the reliable sources such as the official websites of the organizations, the official
            documentation, academic papers, institutional websites with high credibility, etc.

            - If the 'data_selectivity' is 0.5, the browsing operations are executed with a moderate data selectivity.
            In that case, you need to be MODERATELY STRICT about trusting the data you see in the browsing operations.
            You can trust the data you see in the browsing operations with moderate credibility, with at least some
            level of reliability and referencable information. However, you should be cautious about the data you see
            since the user asked for a middle level of data selectivity.

            - If the 'data_selectivity' is 0.0, the browsing operations are executed with the lowest data selectivity.
            In that case, you can trust the data you see in the browsing operations with the lowest credibility.

            - Treat the values in between accordingly based on the data selectivity value explanations shared
            with you above.

            - Data selectivity value is a hyper-parameter that will be given to you by the user and you have no chance
            to modify it. You must use the data selectivity value as it is given to you, and determine your trust level
            based on the data selectivity value.

            -------
            """

    return response_prompt


def build_lean_browsing_datasource_prompt():
    # Build the prompt
    response_prompt = """
            **BROWSING CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            **NOTE**: These are the browsing datasource connections available for use. You can use these connections
            to execute browsing operations on the web. You can connect to a browser, close a browser, search for
            information on the web, and click on URLs in search results. Make sure you are using the correct
            browsing datasource connection ID when executing browsing operations.

            - Description value is shared with you for you to have an idea about the browsing datasource connection
            and the overall goal of the browsing operations within the context of this connection.

            **VERY IMPORTANT NOTE ABOUT 'BROWSING MODES':**
            - The browsing datasource connections have three modes: 'standard', 'whitelist', and 'blacklist'.

            [1] If the connection does not have any 'whitelisted_extensions' or 'blacklisted_extensions',
            the mode is 'standard'. In that case, the browsing operations are executed as usual.

            [2] If the connection has 'whitelisted_extensions' defined, the mode is 'whitelist'. In that case,
            only the URLs with the extensions defined in the 'whitelisted_extensions' field are allowed. Therefore,
            it is not expected for you to be able to see URLs with extensions that are not defined in the
            'whitelisted_extensions' field. Even if you see any, NEGLECT them.

            [3] If the connection has 'blacklisted_extensions' defined, the mode is 'blacklist'. In that case,
            the URLs with the extensions defined in the 'blacklisted_extensions' field are not allowed. Therefore,
            it is not expected for you to be able to see URLs with extensions that are defined in the
            'blacklisted_extensions' field. Even if you see any, NEGLECT them.

            [4] If the connection has both 'whitelisted_extensions' and 'blacklisted_extensions' defined, the mode is
            'blacklist', at least it will be treated this way. Proceed as you normally do, but after you answer the
            users question, let him/her know about the issue and the mutually exclusive nature of the two fields.

            [5] The 'minimum_investigation_sites' field defines the minimum number of sites to investigate before
            returning the results to the user. Make sure you have investigated at least the number of sites defined
            in the 'minimum_investigation_sites' field before returning the results to the user. If you don't have
            enough resources even if you have tried to look for different pages of the search engine, you can return
            the results to the user with the information you have gathered so far and let him/her know about the
            situation.

            [6] The 'reading_abilities' field defines the 'HTML Cleaning Strategy' that the browser uses in the background,
            thus it affects your ability to see and interpret the HTML content of the web pages. The fields labeled
            as 'True' in the 'reading_abilities' field are the ones that are "hidden/removed" from the HTML content
            by the LXML-HTML Cleaner. Therefore, you should not expect to see those fields in the HTML content.

            **VERY IMPORTANT NOTE ABOUT 'data_selectivity':**
            - The 'data_selectivity' field in the browsing datasource connection defines the data selectivity
            of the browsing operations. The data selectivity is a value between 0.0 and 1.0.

            - If the 'data_selectivity' is 1.0, the browsing operations are executed with the highest data selectivity.
            In that case, you need to be VERY STRICT about trusting the data you see in the browsing operations. You
            MUST only trust the reliable sources such as the official websites of the organizations, the official
            documentation, academic papers, institutional websites with high credibility, etc.

            - If the 'data_selectivity' is 0.5, the browsing operations are executed with a moderate data selectivity.
            In that case, you need to be MODERATELY STRICT about trusting the data you see in the browsing operations.
            You can trust the data you see in the browsing operations with moderate credibility, with at least some
            level of reliability and referencable information. However, you should be cautious about the data you see
            since the user asked for a middle level of data selectivity.

            - If the 'data_selectivity' is 0.0, the browsing operations are executed with the lowest data selectivity.
            In that case, you can trust the data you see in the browsing operations with the lowest credibility.

            - Treat the values in between accordingly based on the data selectivity value explanations shared
            with you above.

            - Data selectivity value is a hyper-parameter that will be given to you by the user and you have no chance
            to modify it. You must use the data selectivity value as it is given to you, and determine your trust level
            based on the data selectivity value.

            -------

            """

    return response_prompt
