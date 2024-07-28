
### TODO LIST

---

- [X] Handling the negative balance and stopping transactions when required. Also, for adding negative balances (-123), there needs to be a validation to prevent.
- [X] Rate limiting the usage for safety.
- [X] Real media management with AWS S3 Storages (e.g. profile pictures, organization images, etc.)
- [X] Partial page refresh for permission additions, since it is tiring. If it does not work, instead use forms to save and update
- [ ] Integrating the Payment Gateway to get the payment done (for balance) + credit card safety / storage and usage
- [ ] Real PostgreSQL DBMS integration.
- [ ] Real E-mail SMTP integration.
- [ ] Stop Sequence Integration
- [ ] HTTPS Configuration for the application + CORS configuration.
- [ ] Better logging system.
- [ ] Deploy / DEBUG to PRODUCTION changes and possible updates for the better usage.
- [ ] Privacy Policy and Terms of Service development & integration for the application.
- [ ] Proper Documentation & tutorial, instructions (FAQ and Support) for the application.
- [ ] Exclude the media from Git versioning (IMPORTANT!!)
- [ ] Fix the main search bar for having correct redirection links.
- [ ] Integrate paginations and global searches for the relevant pages.

---

### TECHNICAL CONSIDERATIONS

- [ ] Docker compose YAML file design.
- [ ] GitHub work-flows for CI/CD and integration testing with the application on the cloud.
- [ ] Development of the unit and integration tests for the application.


---


### HELPER PAGES

- [X] Profile page for the user.
- [X] Settings page for miscellaneous settings related to the account. (Adding / Modifying / Deleting credit card, deleting account, etc.)
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
  - [ ] Improve F.A.Q. page
  - [ ] Improve Documentation page
  - [ ] Improve Privacy Policy page
  - [ ] Improve Terms of Service page
  - [ ] Improve Support page


---


### QUICK FIXES

- [ ] Implement the Browsing tool for the web browser & web scraping features.
  - [ ] Browsing must have a choice to select "data cautiousness": "high", "medium", "low".
  - [ ] Browsed pages must be stored in a knowledge base for future reference. 
  - [ ] A data model for the browsed pages must also be designed.
  - [ ] Admin model + save() and save_model() methods must also be needed to integrated.
  - [ ] The browser plugins must be installed: scraper? + driver? + parser?
  - [ ] There must be a page for the users to see the metadata stored pages (summarized form only).
  - [ ] Implementation of the prompt for the browsing tool.
  - [ ] Integration of the prompt to the chat.
  - [ ] Testing within the chat and evaluation of the performance.

<br><br>

- [ ] **NEW FEATURE IDEA:** Discuss ERP integration and assistant interpretation module. [BIG]
- [ ] **NEW FEATURE IDEA:** Discuss the Chrome Extension to automatically understand the web pages etc. [BIG]
- [ ] **NEW FEATURE IDEA:** Boilerplate knowledge bases for direct integration with assistants. [BIG]
- [ ] **NEW FEATURE IDEA:** Text-to-Speech and Speech-to-Text integration for the assistants. [BIG]
- [ ] **NEW FEATURE IDEA:** Word Plugin and possibly other MS Office tools to auto-complete and active help. [BIG]
- [ ] **NEW FEATURE IDEA:** Drive and dropbox integration for media and document storage & automated transfer within the system and knowledge bases. [BIG]
---


### NEXT INTEGRATIONS

*Milestone-1* : ACHIEVED
*Milestone-2* : ACHIEVED

- [ ] Integrate the web browser & web scraping features.
- [ ] Git repository / Code repository integration module.

*Milestone-3*

- [ ] Integrate the Scheduled jobs multi-modality.
- [ ] Integrate the Scripts multi-modality.
- [ ] Integrate the Webhooks / triggers multi-modality.
- [ ] Integrate Media generation multi-modality.
- [ ] Develop functions for different "industries".

*Milestone-4*

- [ ] Dashboard Integration
- [ ] Integrate the orchestration pages.
- [ ] Integrate "Integrations multi-modality".
- [ ] Integrate "Meta-Integrations multi-modality".


---

### BUSINESS SIDE IMPROVEMENTS FOR APPLICATION

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

**Active Tools for Testing:**

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

- Start Date: 2024-06-29

- Total Lines of Code by 2024-07-13: (Day: 15)
  - **1,090,000** 

- Total Lines of Code by 2024-07-14: (Day: 16)
  - **1,315,000**

- Total Lines of Code by 2024-07-15: (Day: 17)
  - **1,118,000**

- Total Lines of Code by 2024-07-16: (Day: 18)
  - **1,476,000**

- Total Lines of Code by 2024-07-17: (Day: 19)
  - **1,555,000**

- Total Lines of Code by 2024-07-18: (Day: 20)
  - **1,563,000**

- Total Lines of Code by 2024-07-19: (Day: 21)
  - **1,476,000**

- Total Lines of Code by 2024-07-27: (Day: 29)
  - **1,574,000**

- Current System Prompt Cost: **~19,000 Tokens**
  - **1M Token** = $5,00
  - **System Prompt Unit Cost** = $0,095 (TRY 3.13) (for **GPT**) 

*To count:*

```bash
git ls-files | xargs wc -l
```

---

**THINGS TO REMEMBER:**

*Important:*
- [ ] Integrate the [TRIGGERS] multimodality. (SUNDAY 29/07)
- [ ] Media generation must be embedded as a [TOOL] and a choice (via switch button) for the assistants. (MONDAY 30/07)
- [ ] Integrate [PICONAUT] with GPT-4o-mini. (MONDAY 30/07)
- [ ] Implement the [WEB BROWSING] data source. (TUESDAY, WEDNESDAY, THURSDAY 31/07, 01/08, 02/08)
- [ ] Implement the [CODE REPOSITORY] data source. (FRIDAY, SATURDAY 03/08, 04/08)
- [ ] Implement the [ORCHESTRATION] manager. (SUNDAY, MONDAY 05/08, 06/08)
- [ ] Implement the [DASHBOARD] page. (TUESDAY, WEDNESDAY, THURSDAY 07/08, 08/08, 09/08)

Deployment Changes:
- [ ] Implement [LOGGING] to all pages.
- [ ] Migrate to [POSTGRES] database.
- [ ] Implement [HTTPS] configuration.
- [ ] Implement [CORS] configuration.
- [ ] Implement [SMTP] configuration.
- [ ] Implement [STOP SEQUENCE] integration for the OpenAI API.
- [ ] Implement [PAYMENT GATEWAY] for the application.
- [ ] Implement and fix [MAIN SEARCH BAR] for the application.
- [ ] Develop [INTEGRATION TESTS] for all the functionalities of all applications.
- [ ] GitHub [WORKFLOWS] for CI/CD integration on GitHub.
- [ ] Migrate to [CLOUD STORAGE] for the media files, update all the required places in the code.
- [ ] Delete the [INTERNAL MEDIA DIRECTORY] from the repository.
- [ ] Code [CLEANUP AND REFACTORING].
- [ ] Prepare the [DEPLOYMENT] changes for the production environment.
- [ ] Deploy the [APPLICATION].
- [ ] Protect the [MAIN BRANCH] from direct merges.
- [ ] Create the [DEVELOPMENT BRANCH] from the main branch.
- [ ] Protect [DIRECT MERGES] to the development branch.
- [ ] RELEASE v0.1.0 [RELEASE: BETA] version of the application.
---

*After first deployment:*
- [ ] Named Entity Recognition [NER] integration.
- [ ] [DOCUMENTATION & API GUIDE] page development.
- [ ] [FAQ] page development.
- [ ] [TERMS & CONDITIONS] development with the law firms.
- [ ] [PRIVACY POLICY & DATA POLICY] development with the law firms.
- [ ] Creation of the [BLOG] page.
- [ ] Creation of the [FORUM] page.
- [ ] [TEXT-TO-SPEECH] and [SPEECH-TO-TEXT] integration for the application.
- [ ] [ARCHITECTURE BUILDING ASSISTANT] Integration (Meta control over application).
- [ ] [CHROME EXTENSION] development for the application.
- [ ] [WORD PLUGIN] development for the application.
- [ ] [DRIVE & DROPBOX] integration for the application.
- [ ] RELEASE v0.2.0 [RELEASE: BETA] version of the application.
---


---

*Helper Functionalities:*

- [ ] Helper for building from scratch (meta helper for creating organizations, assistants, connections, etc.)

---

*Issues:*

  - [ ] There is no document_uuid or repository_uuid field in the chunks classes for weaviate, yet they are used in the code
        for deletions, fix this. [INVESTIGATION REQUIRED]

---

*Cosmetic Improvements:*
- [ ] On the registration, add a promo code field for the users to use for free balance top-ups. (~1 hour)
        - PROMO-CODE: connected to user(A), when the user(B) registers; if the user(B) uses the promo code of user(A), 
                      user(A) will get +$X balance, and user(B) will get +$Y balance.
        - PARAMETERS: [promo_beneficiary, promo_beneficiary_gift, promo_invitee_gift, promo_limit, promo_expiry_date]
- [ ] Add copy buttons for the starred messages.

---
