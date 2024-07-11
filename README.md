
### TODO LIST

---

- [ ] Integrating the Payment Gateway to get the payment done (for balance)
- [X] Handling the negative balance and stopping transactions when required. Also, for adding negative balances (-123), there needs to be a validation to prevent.
- [ ] Rate limiting the usage for safety.
- [ ] Additional cost column for custom tools. (start + continuation)
- [ ] Real PostgreSQL DBMS integration.
- [ ] Real e-mail SMTP integration.
- [ ] HTTPS Configuration for the application + CORS configuration.
- [X] Real media management with AWS S3 Storages (e.g. profile pictures, organization images, etc.)
- [ ] Better validation and logging system.
- [X] Partial page refresh for permission additions, since it is tiring. If it does not work, instead use forms to save and update
- [ ] Deploy / DEBUG to PRODUCTION changes and possible updates for the better usage.
- [ ] Privacy Policy and Terms of Service development & integration for the application.
- [ ] Stop Sequence Integration
- [ ] A better payment method management (for credit card storage and usage).
- [ ] Proper documentation & tutorial.
- [ ] Sample instructions to help the people through the application.
- [ ] Dev instructions markdown to help people setup the project in their own computers / repositories.

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
- [ ] **URGENT:** Implement the SQL data source integration & management.
  - [X] Implement the creation for data source.
  - [X] Implement the listing for the data source.
  - [X] Implement the update for the data source.
  - [X] Implement the deletion for the data source.
  - [X] Integrate the user permissions to the views.
  - [X] Implement the creation for the custom queries
  - [X] Implement the listing for the custom queries
  - [X] Implement the update for the custom queries
  - [X] Implement the deletion for the custom queries
  - [X] Implement the integration of the data source to the main chat feature of the AI assistants.
    - [X] Custom query execution. (Read and write controlled by is_read_only field)
    - [X] Query generation + execution (Read and write controlled by is_read_only field)
    - [X] Integration to the chat multimodality.
    - [X] Test mysql retrieval
    - [ ] Test postgresql retrieval
    - [ ] Test -no- permission write request.
    - [ ] Test permission write request.
    - [ ] Test run custom query (read)
    - [ ] Test run custom query (write)
    - [ ] Tweak the UI to make the messages look better with the tool retrievals.
- [ ] **URGENT:** There must be limits for "how many times the same tool can be reached one after another", and "how many different
      tools can be piped one after another".
- [ ] Implement the NOSQL data source integration & management. (MongoDB)
- [X] Agent tool pipelines must be chainable to be able to use multiple tools one after another, prompt must include 
      specifiers such as "use tool" or "respond", etc.

<br><br>

- [ ] Refine ideas regarding the dashboard page & management.
- [ ] Discuss the "GitHub repo integration" and assistant interpretation module.
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
- [ ] Integrate the orchestration pages.
- [X] Integrate the registration page.
- [ ] Integrate SQL database features.
- [ ] Integrate NOSQL database features.
- [ ] Integrate the knowledge base & document features.
- [ ] Integrate the web browser & web scraping features.
- [ ] Integrate ML models usage features.
- [ ] Integrate the image storage features.
- [ ] Integrate the video storage features.
- [ ] Integrate the audio storage features.
- [ ] Integrate the file system manipulation features.
- [ ] Integrate the functions multi-modality.
- [ ] Integrate the API multi-modality.
- [ ] Integrate the Conditionals multi-modality.
- [ ] Integrate the Scheduled jobs multi-modality.
- [ ] Integrate the Webhooks / triggers multi-modality.
- [ ] Integrate Image generation multi-modality.
- [ ] Integrate Audio generation multi-modality.
- [ ] Develop functions for different "industries".
- [ ] Integrate "Integrations multi-modality".
- [ ] Integrate "Meta-Integrations multi-modality".


---

### PRODUCTION LEVEL IMPROVEMENTS

- [ ] Develop the data privacy policy and terms of service to the application. (LEGAL)
- [ ] Integrate social media accounts on: Facebook, Twitter, LinkedIn, Instagram. (Hüseyin)
- [ ] Marketing via Webrazzi, Product Hunt, Hacker News, Reddit, etc. (Hüseyin)
- [ ] Company formation + Crunchbase Profile. (Ege)
- [ ] Incubation center + investor meetings. (Ege & Hüseyin)
- [ ] SEO optimization for the application. (Emre?)
- [ ] Blog application on the website for better SEO management. (Selin)
- [ ] Customer meetings. (Ege & Hüseyin)

---

### CUSTOM REMINDERS

**Tools we Use for Testing:**
- Login Credentials: 
  - **@Via Google Account** -> edogandursun@gmail.com
- SQL DB Data Source Tests - Aiven Console.
  - Has a PostgreSQL instance.
  - Has a MySQL instance.

---
