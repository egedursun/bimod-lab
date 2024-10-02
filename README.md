### TODO LIST

---

......

- Add the 'VIDEO_GENERATOR=0.0300' cost definition to the .env file of prod and dev servers after you deploy.

- Generate the copyright statements for the HTML templates.

......

---

### BUSINESS SIDE IMPROVEMENTS FOR APPLICATION

1. [ ] [COMPANY FORMATION] for the application. (Ege)
2. [ ] [COMPANY ACCOUNT + CREDIT CARD] for the company. (Ege)
3. [ ] [LEGAL DOCUMENTATION] for the company. (Ege)
4. [ ] [PAID SERVICE ACCOUNTS] for the company and the app, e.g. Hostinger, Bitvault, AWS, Aiven, Weaviate, Sentry,
   GitHub
5. [ ] Development of [BUSINESS PLAN] for the application. (Ege)
6. [ ] Development of [PITCH DECK PRESENTATION] for the application. (Ege)
7. [ ] Development of [PRODUCT CATALOGUE] for the application. (Ege)
8. [ ] Development of [FUNDING & GROWTH PLAN] for the application. (Ege)
9. [ ] Marketing videos: [PROMOTIONAL VIDEO] for the application. (Hüseyin)
10. [ ] Integrate [BIMOD - SOCIAL MEDIA ACCOUNTS] on: [FACEBOOK, TWITTER, LINKEDIN, INSTAGRAM, YOUTUBE, TIKTOK]. (
    Hüseyin)
11. [ ] Ecosystem Marketing via [WEBRAZZI, PRODUCT HUNT, DISCORD, HACKER NEWS, REDDIT], etc. (Hüseyin)
12. [ ] Company [LEGAL FORMATION] and registration for the company. (Ege)
13. [ ] [CRUNCHBASE] Profile. (Ege)
14. [ ] [INCUBATION & ACCELERATION] center
15. [ ] [INVESTMENT] meetings. (Ege & Hüseyin)
16. [ ] [SEO OPTIMIZATION] for the application. (Emre?)
17. [ ] [BLOG] application on the website for better SEO management. (Selin)
18. [ ] [FORUM] application on the website for better SEO management. (Selin)
19. [ ] Client [MEETINGS & WEBINARS]. (Ege & Hüseyin)
20. [ ] Client [TRAININGS]. (Ege & Hüseyin)
21. [ ] [FAIRS & EXHIBITIONS] for the company. (Ege & Hüseyin)
22. [ ] [SPONSORSHIPS & ADVERTISEMENTS] for the company. (Ege & Hüseyin)
23. [ ] [PARTNERSHIPS & COLLABORATIONS] for the company. (Ege & Hüseyin)
24. [ ] [HEADHUNTING & RECRUITMENT] for the company. (Ege & Hüseyin)
25. [ ] [UNIVERSITY MEETUPS & SEMINARS] for the company. (Ege & Hüseyin)

---

### CUSTOM REMINDERS

**Active Tools for Testing:**

- Bitvault for Password Protection
  - **Host:** Bitvault Cloud
  - **Username:** admin@bimod.io
  - **PW:** MejA@ZV38E.%fqF

- Hosting Service (Hostinger)
  - Login Credentials:
    - **@Via Google Account** ->
      - **E-mail:** edogandursun@gmail.com
      - **PW:** ***

  - SSH Connection for VPS Server:
    - **Connection:** ssh -o "StrictHostKeyChecking=no" root@185.170.198.44
    - **Username:** root
    - **PW:** 7#Ao141j3$sI?k5#aDrR

  - SSH Connection to DB VPS Server:
    - **Connection:** ssh -o "StrictHostKeyChecking=no" root@92.113.31.31
    - **Username:** root
    - **PW:** b6VtNjUvpogj=C:UMsx?

  - Email Accounts:
    - **Provider:** mail.hostinger.com
      - **Username:** admin@bimod.io
      - **PW:** FXYP9tU5o^

- PostgreSQL DB:
  - **Host:** Hostinger VPS Server (SSH)
  - **Username:** N/A
  - **Password:** N/A
  - User Login Credentials:
    - bimod_dev
      - **Username:** admin_dev
      - **PW:** AVNS_3Ahz2MyWPkiAEdiSV53
    - bimod_prod
      - **Username:** admin_prod
      - **PW:** AVNS_-pRb8XSnQqRJOyyHxKM

- Weaviate Server:
- **Host:** Weaviate Cloud
  - **Username:** edogandursun@gmail.com
  - **PW:** ***

- Storage Buckets
  - **Host:** AWS S3
  - **Username:**: admin@bimod.io
  - **PW:** ,vVzEkn/PVn+8Gc

- Sentry Logging
  - **Host:** Sentry Cloud
  - **Username:** admin@bimod.io
  - **PW:** ***

- GitHub Account:
- **Username:** egedursun
- **Classic Token:** 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

- Website Analytics:
- **Host:** Google Analytics
  - **Username:** esa.ege@gmail.com
  - **PW:** ***

- Email Templates:
- **Host:** Stripo
  - **Username:** edogandursun@gmail.com
  - **PW:** ***

---

### ENTERTAINING FACTS

- Start Date: 2024-06-29
- Total Lines of Code by 2024-08-23: (Day: 56) **140,024,000**
- Total Code Files by 2024-08-23: (Day: 56) **50,100**

---

*To count the number of lines of code in total:*

```bash
find . -type f -name '*.*' -print0 | xargs -0 cat | wc -l
```

*To count the number of files in total for specific file types:*

```bash
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.css" -o -name "*.scss" -o -name "*.html" -o -name "*.txt" \) -o -type d | wc -l
```

---

**THINGS TO REMEMBER:**

---

-> Master Reasoner: GPT-o1 (reasoning agent)

---

**PRIMARY FEATURE:**

0. AI-Agnostic LLMs Analysis

1. [ ] Implement [PAYMENT GATEWAY] for the application.
  - [ ] Integrate the payment in the [TRANSACTIONS] page for adding balance.
  - [ ] Integrate the [AUTO-SUBSCRIPTION] type payment in the [TRANSACTIONS] page (for automatic balance top-ups)
  - [ ] Integrate [CREDIT CARD STORAGE] in the [PROFILE] page which is necessary for automated payments.
  - [ ] Integrate the [PAYMENT HISTORY & RECEIPTS] page for the application.
    - [ ] [PAYMENT HISTORY PAGE] for the application.
    - [ ] [PAYMENT HISTORY VIEW] for the application.
    - [ ] [PAYMENT RECEIPTS PAGE] for the application.
    - [ ] [PAYMENT RECEIPT VIEW] for the application.
    - [ ] [PAYMENT RECEIPT PRINT FUNCTIONALITY VIEW] for the application.
  - [ ] [TEST OVERALL] functionality.

---
RELEASE v0.2.0 [RELEASE: BETA] version of the application.
---

*After first deployment:*

1. [ ] [DRIVE FILES] integration for the application.
    - [ ] Implement the [SERVICES] for file retrieval, listing, downloading, and adding to Bimod system.
    - [ ] Update the [PAGES] for adding the drive files to the media storages.
    - [ ] Update the [VIEWS] for the drive files addition feature.
    - [ ] [TEST OVERALL] functionality.

2. [ ] [META GUIDE] assistant for manipulating the application as a helper.
    - [ ] Implement an [META-ASSISTANT] that can automatically create data models (e.g. organizations, models, asisstants, etc.)
    - [ ] Implement an [PAGES] for the assistant to be able to manipulate the application.
    - [ ] Implement an [VIEWS] for the assistant to be able to manipulate the application.
    - [ ] Implement an [SERVICES] for the assistant to be able to manipulate the application.
    - [ ] Implement an [MODELS] for the assistant to be able to manipulate the application.
    - [ ] Implement an [URLS] for the assistant to be able to manipulate the application.
    - [ ] [TEST OVERALL] functionality.

3. [ ] [USER DOCUMENTATION] page development.
    - [ ] Implement the [READABLE DOCUMENTATION] pages for better user experience.

4. [ ] [TERMS & CONDITIONS] development with the law firms.
    - [ ] Needs to be [LEGALLY DESIGNED] by legal experts.
    - [ ] Implement the [TERMS & CONDITIONS] page for the application.

5. [ ] [PRIVACY POLICY] development with the law firms.
    - [ ] Needs to be [LEGALLY DESIGNED] by legal experts.
    - [ ] Implement the [PRIVACY POLICY] page for the application.

---
RELEASE v0.3.0 [RELEASE: BETA] version of the application.
---

*Ongoing Improvements:*

1.  [ ] Store additions [FUNC + API + SCRIPT / STORE] must be added to the application.
2.  [ ] Boilerplate knowledge bases [BOILERPLATE KB] must be added to the application.

---
RELEASE v0.4.0 [RELEASE: BETA] version of the application.
---

1. [ ] [MOBILE APPLICATION] only for connecting endpoints, and being able to chat with them and receive answers. 
        -> For Maps and Location features. 
        -> Requires implementation with a PWA (Progressive Web Application, works on Mobile)
        -> Requires a [MOBILE APPLICATION REPOSITORY].
2. [ ] [DESKTOP COPILOT] development for the application. 
        -> Only for connecting endpoints and receiving answers. 
        -> Requires a [DESKTOP APPLICATION REPOSITORY].
3. [ ] [WORD PLUGIN] development for the application. 
        -> For manipulating inside Microsoft Office applications.
        -> Requires [MS OFFICE PLUGIN REPOSITORIES].
4. [ ] [PHYSICAL DEVICE] for local integrations without Internet Usage.
        -> Definite [SOLUTION FOR PRIVACY] concerns.
        -> Requires a physical device / server node.
        -> Possible to be patentable (IP value).

---
RELEASE v0.5.0 [RELEASE: BETA] version of the application.
---

1. [ ] Integration (Boilerplate assistant) Systems.
       -> [INTEGRATION SYSTEMS]
2. [ ] Meta-Integration (Boilerplate group of assistants) Systems.
       -> [META-INTEGRATION SYSTEMS]

---
RELEASE v0.6.0 [RELEASE: BETA] version of the application.
---

*TO BE DISCUSSED:*

1. [ ] Integrate [PICONAUT] with GPT-4o. (MONDAY 30/07)
       -> A higher level programming language by using GPT-4o-mini. 
       -> Currently does not worth the development effort.
2. [ ] [BLOCKCHAIN] integration for the application.
       -> Blockchain multi-modality integration to the application.
       -> Not very clear what it can be helpful for.
       -> For building smart contracts [?]
3. [ ] [OPENCV FACE-RECOGNITION] technologies integration
       -> Facial recognition integration for security & other application areas.
       -> Currently does not worth the development effort.
4. [ ] [RECENTLY & FREQUENTLY USED] for the application.
       -> Recommendation systems for the general use patterns in the application.
       -> For the user to be able to see the recently and frequently used items.
       -> Currently does not worth the development effort.
5. [ ] [EXPERIENCE NETWORK] for the application.
       -> For the application users who are freelancers or independent workers.
       -> They can collaborate and form networks within the application to work together.
       -> They can share media storages, data sources, and other tools to create synergy.
       -> Currently does not worth the development effort.

---

*Standalone Applications:*

- **Django Mainframe (Server + Web Application)**
  - For the main application and the frontend of the web application.
  - The flagship application for the Bimod project.
- **Electron Copilot (Desktop Application)**
  - For image and text-based management and manipulation within the OS and overall system usage.
  - Can also understand the context of the browsers while the user is actively using the browser and OS.
- **Progressive Web App (PWA) (Android & iOS Application)**
  - Connecting an exported assistant and chatting with the assistant.
  - Communicating with STT and TTS services.
  - Sending and receiving messages from the assistant.
  - Sending and receiving files from the assistant.
  - Sending and receiving images from the assistant.
  - For the assistant to track location & other data.
  - For the assistant to be able to send notifications & reminders.

---

**MAINTENANCE COST ANALYSIS:**

- *One-Off:*
  - Company Formation Costs: $?
  - Legal Documentation Costs
    - Privacy Policy: $?
    - Terms of Service: $?
    - User Agreements: $?
    - Company Agreements: $?

- *Monthly:*
  - Company Expenses
    - Regular Taxations: $?
      * Paid: [monthly/yearly]
    - Accountant Service: $?
      * Paid: [monthly/yearly]
    - Virtual Office Service: $?
      * Paid: [monthly/yearly]
    - Trade Room Registry and Membership: $?
      * Paid: [monthly/yearly]
  - Hosting Service: $20
    * Paid: yearly / $20 x 12 = $240
  - Domain Service: $5
    * Paid: yearly / $5 x 12 = $60
  - SSL Certification: -- within the Hosting Service
    * Paid: yearly
  - Organization Emails: $10
    * Paid: yearly / $12 x 10 = $120
      1. admin@bimod.io / internal operations
      2. info@bimod.io / general inquiries
      3. support@bimod.io / support inquiries
      4. careers@bimod.io / job applications
      5. colab@bimod.io / collaborations and partnerships
      6. ege.dursun@bimod.io / Ege Dursun
      7. huseyin.ersay@bimod.io / Huseyin Ersay
      8. selin.canbulut@bimod.io / Selin Ceren Canbulut
      9. emre.oge@bimod.io / Emre Oge
      10. mert.tekin@bimod.io / Mert Tekin
  - Aiven Cloud PostgreSQL Database (Dev): $200
    * Paid: monthly
  - Aiven Cloud PostgreSQL Database (Prod): $200
  - AWS S3 Storage Service: $20 / 100GB
    * Paid: monthly
  - SMTP Cloud Service: ???
    * Paid: monthly
  - Weaviate Cloud Server: $75 / [for ~10,000 chats]
    * Paid: monthly / $75 x 12 = $900
  - Sentry Logging Tool: $30
    * Paid: monthly / $30 x 12 = $360
  - GitHub Entreprise: $4 per user / mo x 5 users = $20
    * Paid: monthly / $20 x 12 = $240

---

MAJOR COSTS:

1. HOSTING: $240 (will be higher / $500 OR $1000)
2. DOMAIN: $60
3. EMAILS: $150
4. DATABASE (DEV): $2400
5. DATABASE (PROD): $2400
6. WEAVIATE: $900
7. SENTRY LOGGING: $360
8. GITHUB ENTREPRISE: $240
9. AWS S3 STORAGE: $240
   => $7000 (~$600 / month) ($300 per month per co-founder)

COMPANY COSTS:

1. TAXATION: $1200
2. ACCOUNTANT: $1800
3. VIRTUAL OFFICE: $300
4. TRADE ROOM: $300
5. SECONDARY EXPENSES: $2400
   => $6000

TOTAL COSTS: $13,000 / year (~$1,100 / month) ($550 per month per co-founder)

---

- Common extensions, common browsing URLs are saved and offered to the user.
- Experience network / user collaboration for the application.


------------------------------------------------------------------------------------------------------------------------

**Headhunting & Recruitment:**

[-] Huseyin - Operations Project Management (net: $2,000)
[-] Ege - Artificial Intelligence Engineer & Tech Project Management (net: $2,000)
[-] Selin - Social Media Management & Digital Marketing & Legal Consultancy (net: $2,000)
[-] Emre - Marketing & Sales, Business Development (net: $2,000)
[-] Mert - Front-End Engineer & UI/UX Design (net: $2,000)

[1] UI/UX Designer & Brand Identity Designer (net: $2,000)
[2] Django Back-End Engineer (net: $2,500)
[3] Artificial Intelligence Engineer (net: $3,000)
[4] Front-End Engineer (net: $2,500)
[5] Data Engineer (net: $2,500)
[6] Python Engineer (net: $2,000)

**Technical Equipment:**

[1] Work Computers (x6) = $17,000
[2] Workstation (Local AI ) Prototype = $30,000

**Company Expenses:**

[1] Cloud Services = $15,000
[2] Base Company Expenses = $10,000
[3] Legal Expenses = $10,000
[4] Personal Accounts = $12,000

**Office Costs:**

[1] One-Time Setup: $5,000
[2] Rent: $1,500 (x12 months) = $18,000
[3] Utilities: $500 (x12 months) = $6,000
[4] Office Supplies: $500 (x12 months) = $6,000
[5] Cleaning and Maintenance: $500 (x12 months) = $6,000
[6] Kitchen & Need Supplies: $500 (x12 months) = $6,000
[7] Food & Beverage: $10 per person (x11 person x 22 work days x 12 months) = $30,000
[8] Transportation: $3 per person (x11 person x 22 work days x 12 months) = $10,000

**Sales, Advertising, Marketing:**

[1] Marketing & Advertising = $50,000 (x12 months) = $600,000


- Salaries (x12 months) = $300,000 + (tax: $200,000) = $500,000
- Equipment = $47,000
- Company Expenses = $42,000
- Office Costs = $87,000
-- Total costs before marketing: $676,000
-- Safety Padding: (%20) = $135,000
-- Total costs with padding: $800,000


----

begin:40% / s:34% / a:26% / b:20% / c:17% / d:14% / e:12% / ipo:9%
begin:$0 / s:$510,000 / a:$13,000,000 / b:$30,000,000 / c:$90,500,000 / d:$140,000,000 / e:$200,000,000 / ipo:$225,000,000

Expected Growth: 
- $500,000 volume in the first year (start: $1,500,000 investment with [20%]) seed
- $2,000,000 volume in the second year (start: $10,000,000 investment [20%]) series-a
- $10,000,000 volume in the third year (start: $30,000,000 investment [20%]) series-b
- $40,000,000 volume in the fourth year (start: $80,000,000 investment [15%]) series-c
- $80,000,000 volume in the fifth year (start: $150,000,000 investment [15%]) series-d
- $150,000,000 volume in the sixth year (start: $250,000,000 investment [15%]) series-e
- $250,000,000 volume in the seventh year (start: IPO: $500,000,000 [20%]) IPO


UVICORN RUN COMMAND (migrate this to a proper place later on):
```bash
uvicorn config.asgi:application --host 127.0.0.1 --port 8000 --reload
```


```
git ls-remote https://github.com/Bimod-HQ/bimod-app.git | awk '{print $1}' | xargs -n 1 git cat-file -s
```
