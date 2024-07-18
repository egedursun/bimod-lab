
### TODO LIST

---

- [X] Handling the negative balance and stopping transactions when required. Also, for adding negative balances (-123), there needs to be a validation to prevent.
- [X] Rate limiting the usage for safety.
- [X] Real media management with AWS S3 Storages (e.g. profile pictures, organization images, etc.)
- [X] Partial page refresh for permission additions, since it is tiring. If it does not work, instead use forms to save and update
- [ ] Integrating the Payment Gateway to get the payment done (for balance) + credit card safety / storage and usage
- [ ] Additional cost column for custom tools. (start + continuation)
- [ ] Real PostgreSQL DBMS integration.
- [ ] Real E-mail SMTP integration.
- [ ] Stop Sequence Integration
- [ ] HTTPS Configuration for the application + CORS configuration.
- [ ] Better validation and logging system.
- [ ] Deploy / DEBUG to PRODUCTION changes and possible updates for the better usage.
- [ ] Privacy Policy and Terms of Service development & integration for the application.
- [ ] Proper Documentation & tutorial, instructions (FAQ and Support) for the application.
- [ ] Automated balance top-ups (monthly or as it goes low).
- [ ] Exclude the media from Git versioning (IMPORTANT!!)
- [ ] Fix the search bar for having correct redirection links.

---

### TECHNICAL CONSIDERATIONS

- [ ] Docker compose YAML file design.
- [ ] GitHub work-flows for CI/CD and integration testing with the application on the cloud.
- [ ] Development of the unit and integration tests for the application.


---


### HELPER PAGES

- [X] Profile page for the user.
- [X] Settings page for miscellaneous settings related to the account. (Adding/Modifying/Deleting credit card, deleting account, etc.)
- [X] F.A.Q. page for the users and explanations regardign the application.
- [X] Documentation page for explaining how the application works, and tutorials for the users.
- [X] Support page for the users to contact the support team.
- [X] Landing page for the application:
  - [X] Main section + Navigation.
  - [X] Main illustration.
  - [X] About section.
  - [X] Services section.
  - [X] Features section.
  - [X] Team section.
  - [X] Testimonials / Clients section.
  - [X] Pricing section.
  - [X] Contact Us section.
  - [X] Footer section.


---


### QUICK FIXES

- [X] Add the page to include users to other organizations / remove them.
- [X] Add an active field to permissions. When the user is deactivated, the permissions are also deactivated. When the user is reactivated, the permissions are also reactivated.
- [X] The LLM models are all over the place, they are not unique to the organization anymore. Either we need to change how balance calculation works in the transactions page, or we need to make the LLM models unique to the organization.
- [X] Handle the additional information in the registration page.
- [X] Integrate the chat deletion page and functionality.
- [X] Connect user message creation form.
- [X] Connect assistant response framework.
- [X] Test the flow of chat.
- [X] When the chat is created the first time, there is a bug preventing the user message to be sent.
- [X] Fix the documentation page and include content.
- [X] Fix the FAQ page and include content.
- [X] Transactions must also include the responsible user, to associate the costs with the users.
- [X] Show a loading bar while the message response is being calculated.
- [X] Show the messages in mark-down format.
- [X] Add memory objects to the permission management.
- [X] Add the API endpoint not only when the server is started, but also when an endpoint is created.
- [X] Limit the number of exports users can create for each organization.
- [X] Show the number of exports remaining for the user.
- [X] Implement the rest of the pages for the export assistants application.
- [X] Check if the transactions are deleted when an ORGANIZATION is deleted, it must not be the case.
- [X] There is a bug when updating the time & place awareness of the assistant. Fix it.
- [X] Integrate the permissions for the export assistants.
- [X] Transaction calculations are not correct, system messages are not added to the calculation,
                  creating discrepancies in the balance. Additionally, the logic somehow does not work for
                  the API exports. Fix these issues.
- [X] Whenever an organization is deleted, the balance must be transferred to another organization. The
                  last organization cannot be deleted to avoid this problem.
- [X] Implement pagination for the transactions page.
- [X] Currently, when a user is disassociated from organizations, but not deleted from the system, there
                  is no way to add that user back to the organization since the user is permanently disassociated 
                  from the organization. We need to think of a possible way to add that user back to the organization
                  without having to delete the account then re-register the user.
- [X] Implement the SQL data source integration & management.
- [X] There must be limits for "how many times the same tool can be reached one after another", and "how many different
      tools can be piped one after another".
- [X] Agent tool pipelines must be chainable to be able to use multiple tools one after another, prompt must include 
      specifiers such as "use tool" or "respond", etc.
- [X] Storing the text for the transactions cause a heavy overload on the tables, which is something
                  we need to avoid. So, I will remove the text field from the transactions, and calculate the token
                  cost beforehand (instead of doing it in save method of the models.py), and store the token cost
                  in the transaction. This way, we can avoid the heavy load on the database.
- [X] It seems like the tool retry & chain retry limits are not working as intended. Debug and fix this.
- [X] 'INTRINSIC_ONE_TIME_SQL_RETRIEVAL_LIMIT (max=100)' must be determined by the assistant's configuration 
                    according to the user's preferences. Plus, there needs to be a 'ONE_TIME_SQL_RETRIEVAL_TOKEN_LIMIT 
                    (max=10_000)' to prevent using too many tokens, and to prevent very large results. 
- [X] Implement the context cut-off tool to prevent context window from overflowing.
- [X] Implement the Knowledge Base tool for the web browser & web scraping features.
- [X] Implement the Vectorizer Memory for context overflows, within the same class with knowledge base.
- [X] Create the indexes for all data models to increase the performance.
- [X] Template messages must show up next to the message creation form.
- [X] Implement the permissions for the file system tool.
- [X] Implement the permissions for the media storage tool.
- [ ] Implement the Browsing tool for the web browser & web scraping features.
  - [ ] Browsing must have a choice to select "data cautiousness": "high", "medium", "low", which will determine
          how difficult the agent will trust on an online source.
  - [ ] Browsed pages must be stored in a knowledge base for future reference. 
  - [ ] A data model for the browsed pages must also be designed.
  - [ ] Admin model + save() and save_model() methods must also be needed to integrated.
  - [ ] The browser plugins must be installed: scraper? + driver? + parser?
  - [ ] There must be a page for the users to see the metadata stored pages (summarized form only).
  - [ ] Implementation of the prompt for the browsing tool.
  - [ ] Integration of the prompt to the chat.
  - [ ] Testing within the chat and evaluation of the performance.
- [X] Implement the File System tool for the file system manipulation features.
- [ ] Implement the ML Model tool for the ML models usage features.
- [ ] Implement the media storage features.
  - [X] Implement the media item description field for the upload staging section.
  - [X] Implement the list media items page.
  - [ ] Implement the retrieval function for the assistant.
  - [ ] Implement the image interpretation tool.
  - [ ] Integrate the prompts.
  - [ ] Test the functionality.

<br><br>

- [ ] Refine ideas regarding the dashboard page & management.
- [ ] **NEW FEATURE IDEA:** Discuss the "GitHub Repo Integration" and assistant interpretation module.
- [ ] **NEW FEATURE IDEA:** Discuss ERP integration and assistant interpretation module.
- [ ] **NEW FEATURE IDEA:** Discuss the Chrome Extension to automatically understand the web pages etc.
- [ ] **NEW FEATURE IDEA:** Glossaries for Technical Terminology integration to the chats. ( can take up space in terms of tokens )
- [ ] **NEW FEATURE IDEA:** Boilerplate knowledge bases for direct integration with assistants.
- [ ] **NEW FEATURE IDEA:** Text-to-Speech and Speech-to-Text integration for the assistants.
- [ ] **NEW FEATURE IDEA:** Word Plugin and possibly other MS Office tools to auto-complete and active help.
- [ ] **NEW FEATURE IDEA:** Drive and dropbox integration for media and document storage & automated transfer within the system and knowledge bases.
---


### NEXT INTEGRATIONS

- [X] Integrate login.
- [X] Integrate organization management.
- [X] Integrate LLM model management.
- [X] Integrate transaction management.
- [X] Integrate subscription management.
- [X] Integrate user management.
- [X] Integrate permission management.
- [X] Complete the pages for the user permission management.
- [X] Integrate the assistants pages.
- [X] Integrate the chats pages.
- [X] Integrate the export assistant pages.
- [X] Integrate the memories pages.
- [X] Integrate the message templates pages.
- [X] Integrate the starred messages pages.
- [X] Integrate the registration page.
- [X] Integrate SQL database features.
- [X] Integrate the knowledge base & document features.
- [ ] Integrate the web browser & web scraping features.
- [ ] Integrate ML models usage features.
- [ ] Integrate the media storage features (image, audio, video).
- [ ] Integrate the file system manipulation features.
- [ ] Integrate the functions multi-modality.
- [ ] Integrate the API multi-modality.
- [ ] Integrate the Conditionals multi-modality.
- [ ] Integrate the Scheduled jobs multi-modality.
- [ ] Integrate the Webhooks / triggers multi-modality.
- [ ] Integrate Image generation multi-modality.
- [ ] Integrate Audio generation multi-modality.
- [ ] Develop functions for different "industries".
- [ ] Integrate the orchestration pages.
- [ ] Integrate "Integrations multi-modality".
- [ ] Integrate "Meta-Integrations multi-modality".


---

### PRODUCTION LEVEL IMPROVEMENTS

- [ ] Develop the data privacy policy and terms of service to the application. (LEGAL)
- [ ] Integrate social media accounts on: Facebook, Twitter, LinkedIn, Instagram. (Hüseyin)
- [ ] Marketing via Webrazzi, Product Hunt, Hacker News, Reddit, etc. (Hüseyin)
- [ ] Company formation + CrunchBase Profile. (Ege)
- [ ] Incubation center + investor meetings. (Ege & Hüseyin)
- [ ] SEO optimization for the application. (Emre?)
- [ ] Blog application on the website for better SEO management. (Selin)
- [ ] Customer meetings. (Ege & Hüseyin)

---

### CUSTOM REMINDERS

**Tools we Use for Testing:**

- Hosting Service (Hostinger).
  - Login Credentials: 
    - **@Via Google Account** ->
      - **E-mail:** edogandursun@gmail.com
      - **PW:** ***
  - SSH Connection:
    - **Username:** root
    - **PW:** t@G0trEhboeOWWDSi5Bg

- SQL DB Data Source Tests - Aiven Console.
  - Login Credentials: 
    - **@Via Google Account** -> edogandursun@gmail.com
    - Has a PostgreSQL instance.
    - Has a MySQL instance.


---


### FUN FACTS

- Total Lines of Code by 2024-07-13: 
  - **1,090,000** 

- Total Lines of Code by 2024-07-14: 
  - **1,315,000**

- Total Lines of Code by 2024-07-15:
  - **1,118,000**

- Total Lines of Code by 2024-07-16:
  - **1,476,000**

- Total Lines of Code by 2024-07-17:
  - **1,555,000**

- Current System Prompt Cost: **~10,800 Tokens**
  - **1M Token** = $5,00
  - **System Prompt Unit Cost** = $0,054 (TRY 1,80) (for **GPT**) 

*To count:*

```bash
git ls-files | xargs wc -l
```

---

**THINGS TO REMEMBER:**

Templates:
- [ ] Add a save as template button to the chat. (~1 hour)

File Systems:
- [ ] Implement script generation (similar to function generation). (~3-4 hours)

Exported Assistants API:
- [ ] Add the generated file and images thing to the exported assistants. (~3-4 hours)

---

Small Chores:
- [ ] Migrate the image interpretation temperature and token max length. (~0.5 hours)

Important:
- [ ] Show the assistant images in the chat, to the user. -> currently shows up, but the size is too big and awkward. Fix this. (~1-2 hours)
- [ ] Implement direct chat image and file interpretation + show user images in the chat. (~3-4 hours)


Moderate:
- [ ] Implement the image detail page for the media storage items. (~1-2 hours)
- [ ] Implement auto-generated image descriptions for the image detail page. (~1-2 hours)
- [ ] Implement download / retrieve with link page for the media storage items page. (~1-2 hours)
- [ ] Implement download as a tool for chats. (~1-2 hours)

Cosmetic Improvements:
- [ ] For images, on list media items page, show little image thumbnails. (~1 hour)
- [ ] For audios, on list media items page, show little audio players.  (~1 hour)
- [ ] For videos, on list media items page, show little video cover images. (~1 hour)
- [ ] For code and data files, skip...
- [ ] "Add New" buttons for all relevant pages. (~1 hour)

---

Notes:
- [ ] Use the code interpreter tool of GPT assistants as a way to run GPT-generated functions, instead of custom functions.
