#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: web_datasource_prompt.py
#  Last Modified: 2024-10-16 01:33:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.assistants.models import Assistant
from apps.datasource_browsers.models import DataSourceBrowserConnection


def build_sheetos_browsing_data_source_prompt(assistant: Assistant):
    browsing_data_sources = DataSourceBrowserConnection.objects.filter(assistant=assistant)
    response_prompt = """
            ### **BROWSING CONNECTIONS:**

            '''
            """

    for i, browsing_datasource in enumerate(browsing_data_sources):
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
                """

    response_prompt += """
            -------

            '''

            #### **NOTE**: These are the browsing tools available for you to use. You can use these connections
            to execute browsing operations on web. You can connect to a browser, close a browser, search for
            info on web, and click on URLs in searches. Make sure you are using the correct browsing datasource
            connection ID when executing browsing.

            - The 'description' is shared for you to have an idea about the browsing connection and the goal of the
            browsing operations within context. In other words, it is given to you for you to understand the
            context more.

            #### **IMPORTANT NOTE ABOUT 'BROWSING MODES':**
            - The browsing connections have 3 MODES:
                i. 'standard'
                ii. 'whitelist'
                iii. 'blacklist'

            [1] If the connection does not have any 'whitelisted_extensions' or 'blacklisted_extensions',
            the mode is 'standard' by DEFAULT. In that case, the operations are executed as usual.

            [2] If the connection has 'whitelisted_extensions' defined, the mode is 'whitelist'. In that case,
            only URLs with the extensions defined in the 'whitelisted_extensions' field are allowed. Thus,
            it is not expected for you to see URLs with extensions that are not defined in the 'whitelisted_extensions'
            field. Even if you see any, NEGLECT them.

            [3] If the connection has 'blacklisted_extensions' defined, the mode is 'blacklist'. In that case,
            the URLs with the extensions defined in the 'blacklisted_extensions' field are NOT allowed. Thus,
            it is not expected for you to see URLs with extensions that are defined in the 'blacklisted_extensions'
            field. Even if you see any, NEGLECT them.

            [4] If the connection has both 'whitelisted_extensions' and 'blacklisted_extensions' defined, the mode is
            'blacklist', at least it MUST and WILL be treated this way by the tool and the internal algorithms of the
            browsing system. Proceed as you normally do, but after you answer the question, let the user know about
            the issue and the mutually exclusive nature of the 2 fields.

            [5] The 'minimum_investigation_sites' defines the minimum number of sites to investigate before
            answering the user. Make sure you investigated at least the number of sites defined in this field before
            returning the results. If you don't have enough resources even if you tried to look for different web pages,
            you can return the results to the user with the info you have gathered so far and let them know about the
            situation.

            [6] The 'reading_abilities' defines the 'HTML Cleaning Strategy' the browser uses in the background,
            thus it affects your ability to see and interpret the HTML content of the pages. The fields labeled
            as 'True' in the 'reading_abilities' field are the ones that are "hidden/removed" from the HTML by the
            LXML-HTML Cleaner. Thus, you should not expect to see the hidden fields in the HTML content. Yet, if
            they are not hidden, you can expect to see tags and contents associated with those fields.

            ---

            #### **IMPORTANT NOTE ABOUT 'data_selectivity':**
            - The 'data_selectivity' in the browsing connection defines the data selectivity of the browsing
            operations. The data selectivity is a value between 0.0 and 1.0.

            - If the 'data_selectivity' is 1.0 (theoretical maximum) the operations are executed with the highest
            data selectivity. In that case, you need to be VERY STRICT about trusting the data you see on web.
            You MUST only trust the reliable sources such as the official websites of the organizations, the official
            documentations, academic papers, institutional websites with high credibility, etc. Unlike whitelisted
            and blacklisted extensions/domains, this is NOT automatically handled by the tool; and you are primarily
            responsible for deciding whether or not a given source is reliable or not.

            - If the 'data_selectivity' is 0.5, the operations are executed with a moderate data selectivity.
            In that case, you need to be MODERATELY STRICT about trusting the data you see online. You can trust the
            data you see in the browsing operations with moderate credibility, with at least some level of reliability
            and citable information. Yet, you must be moderately cautious about the data you see as the user asked
            for a middle level of data selectivity, since the value is just in the middle.

            - If the 'data_selectivity' is 0.0 (theoretical minimum), the operations are executed with the lowest
            data selectivity. In that case, you can include the data you see in the browsing operations with the
            lowest credibility and don't need to apply any filtering to the sources you gathered through browsing.

            - Treat the values in between accordingly based on the data selectivity value shared with you. For example
            a value of 0.8 must make you pretty strict in selectivity, yet not AS MUCH strict as you would be for a
            value of 1.0. Similarly, a 0.2 is a lower selectivity, yet it is not as generous as a value of 0.0, so
            there must be a little selectivity.

            - Data selectivity is a hyper-parameter that will be given to you by the user and you have no chance
            to modify it. You must use the data selectivity as it is give, and determine your trust level based on the
            value. Be very careful about this issue. Yet, if the user prompts you to be less or more selective
            'explicitly', you must prioritize the user's desires.

            ---
            """

    return response_prompt

