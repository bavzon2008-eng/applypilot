# 🚀 ApplyPilot

### An Autonomous AI Agent That Turns Job Opportunities Into Application-Ready Missions

**ApplyPilot** is an AI-powered job discovery and application-preparation agent built for the **Anakin Forge Hackathon — Build AI Agents That Read, Reason, and Act**.

Instead of simply showing job links, ApplyPilot combines **live web discovery, AI reasoning, opportunity evaluation, personalized application preparation, and controlled browser inspection** into one workflow.

> **Discover → Reason → Prepare → Review → Human Approval → Act**

ApplyPilot is designed around an important principle:

> **The agent should automate the repetitive work — while the human remains in control of the final application.**

---

## 🎯 The Problem

Finding internships and entry-level opportunities is surprisingly repetitive.

A student typically has to:

* Search multiple job websites
* Read dozens of job descriptions
* Check whether the role is still active
* Determine whether their skills match
* Check eligibility requirements
* Identify important application requirements
* Open the original job page
* Prepare a resume/cover letter
* Fill repetitive information
* Navigate different application systems
* Deal with expired listings, redirects, authentication, CAPTCHAs and bot protection

This process is time-consuming and difficult to scale manually.

### ApplyPilot changes that workflow.

Instead of asking the user to manually search and evaluate every opportunity, ApplyPilot acts as an **AI job-application copilot**.

---

# 🧠 What ApplyPilot Does

ApplyPilot transforms a user's profile and job-search goal into an application workflow.

### Example

**User profile**

```text
Name: Bavana Saravanan
Education: 3rd-year B.Tech CSE
Skills: Python, Java, React, SQL
Location: India / Remote
Goal: AI & Software Engineering Internships
```

ApplyPilot can then:

```text
1. Understand the user's goal
          ↓
2. Generate targeted search intents
          ↓
3. Search live web opportunities
          ↓
4. Collect opportunity information
          ↓
5. Remove/penalize weak or expired opportunities
          ↓
6. Analyze candidate ↔ opportunity fit
          ↓
7. Rank opportunities
          ↓
8. Generate an application mission
          ↓
9. Prepare a personalized cover letter
          ↓
10. Open and inspect the official opportunity
          ↓
11. Detect whether an application workflow is actually reachable
          ↓
12. Stop for human approval before final submission
```

---

# ✨ Key Features

## 1. 🎯 Goal-Driven Job Discovery

The user does not have to search using a fixed query.

ApplyPilot uses the user's actual goal to generate search intents.

For example:

```text
AI internships
```

produces a different discovery strategy from:

```text
Frontend React internships
```

or:

```text
Data Science internships in India
```

The user's:

* Goal
* Skills
* Education
* Location
* Preferred opportunities

are used to construct targeted searches.

---

# 2. 🌐 Live Web Search with Anakin

ApplyPilot uses **Anakin's Search API** to retrieve current web opportunities instead of relying on a static job database.

Anakin's Search API is designed for AI agents and provides web search with extracted page information.

ApplyPilot performs multiple targeted searches instead of depending on a single generic query.

### Search strategy

The agent considers signals such as:

* User's exact goal
* Relevant skills
* Education level
* Geographic preference
* Internship/job terminology
* Company/source quality
* Official or ATS-hosted listings

This allows the search process to adapt to different users.

---

# 3. 🏢 Opportunity Quality Filtering

Not every result returned by a web search is a good opportunity.

ApplyPilot evaluates source quality and prioritizes opportunities from:

* Official company career pages
* Recognized applicant-tracking systems
* Established recruitment platforms
* Reputable job sources

Weak aggregator sources can be penalized.

Expired opportunities are also detected using job-status signals and language indicating that a listing is no longer active.

---

# 4. 🤖 AI-Powered Opportunity Reasoning

After discovering opportunities, ApplyPilot uses an LLM reasoning layer to evaluate them.

The agent considers:

### Candidate information

* Skills
* Education
* Location
* Career goal
* Experience/profile information

### Opportunity information

* Job title
* Company
* Requirements
* Responsibilities
* Location
* Internship/full-time status
* Eligibility
* Opportunity status

The result is a structured evaluation rather than simply a list of URLs.

---

# 5. 📊 Match Scoring

Each opportunity receives a candidate-fit evaluation.

The interface communicates:

* Match score
* Recommendation
* Eligibility
* Opportunity status
* Reasoning/signals
* Recommended next action

Example:

```text
MATCH: 91%

RECOMMENDATION: PREPARE

ELIGIBILITY: LIKELY ELIGIBLE

STATUS: ACTIVE

WHY:
Strong alignment with Python, React and software engineering
requirements.
```

---

# 6. 📋 Application Mission

Once the user chooses an opportunity, ApplyPilot can build an **Application Mission**.

The mission transforms a job listing into a structured preparation workflow.

It can include:

* Target company
* Role
* Opportunity URL
* Candidate fit
* Application checklist
* Important requirements
* Personalized cover letter
* Application preparation status
* Official opportunity link

The mission gives the user a clear path from:

**“I found a job”**

to:

**“I know exactly what I need to do to apply.”**

---

# 7. ✍️ Personalized Cover Letter

ApplyPilot generates a cover letter based on the selected opportunity and candidate profile.

The generated letter is personalized using information such as:

* Candidate name
* Skills
* Education
* Career goal
* Target role
* Company/opportunity context

The application mission is explicitly prepared for the candidate rather than producing a generic reusable letter.

Example sign-off:

```text
Best regards,

Bavana Saravanan
```

---

# 8. 🌍 Official Opportunity Inspection

ApplyPilot can open the selected opportunity and inspect the destination page.

The browser agent looks for signals indicating whether the page actually leads to an application workflow.

It can inspect:

* Page content
* Links
* Application-related controls
* Application forms
* Relevant input fields
* Application-page indicators
* Redirects
* Verification/security barriers

The goal is to determine:

> **Can ApplyPilot actually reach an application workflow for this opportunity?**

---

# 9. 🧭 Application Workflow Detection

ApplyPilot does not assume that a button named **Apply** means a usable application form exists.

It attempts to distinguish between:

### Real application workflow

```text
Job page
   ↓
Apply
   ↓
Application page
   ↓
Candidate fields
   ↓
Application workflow detected
```

and:

### Non-application destination

```text
Job page
   ↓
Apply
   ↓
Generic website / login / search page
```

and:

### Verification blocked

```text
Job page
   ↓
Apply
   ↓
Cloudflare / CAPTCHA / verification
   ↓
VERIFICATION_BLOCKED
```

This prevents the agent from falsely claiming that an application was completed.

---

# 10. 🛡️ Verification & Anti-Bot Detection

Real-world websites can introduce:

* CAPTCHA
* Cloudflare verification
* Human verification
* Security checks
* Identity verification
* Access denied pages
* Bot detection

ApplyPilot explicitly detects these conditions.

When encountered, the agent reports a state such as:

```text
VERIFICATION_BLOCKED
```

instead of pretending that it successfully reached the application.

---

# 11. 👤 Human-in-the-Loop Approval

ApplyPilot intentionally does **not** blindly submit applications.

The workflow stops before final submission and keeps the user in control.

### Why?

Job applications may contain:

* Personal information
* Education information
* Employment history
* Legal declarations
* Work authorization questions
* Demographic information
* Salary expectations
* Consent agreements
* Company-specific questions
* Resume uploads

These should not be blindly submitted by an autonomous system.

Therefore:

```text
AI prepares
      ↓
AI inspects
      ↓
AI recommends
      ↓
        HUMAN REVIEWS
              ↓
       HUMAN APPROVES
```

---

# 🔌 Anakin Integration

ApplyPilot is built around **Anakin.io** as its web-agent infrastructure.

Anakin provides APIs for web search, scraping, browser automation and pre-built website actions. Its current Wire platform exposes structured actions across a large catalog of websites.

ApplyPilot currently uses Anakin primarily for:

### Search

```text
Anakin Search API
        ↓
Live web opportunity discovery
```

### Wire

```text
Anakin Wire
        ↓
Discover supported website actions
        ↓
Execute configured/read/write actions when available
```

### Browser / Web Inspection

```text
Browser automation
        ↓
Open opportunity
        ↓
Inspect page
        ↓
Detect application workflow
```

Anakin's Wire architecture provides structured website actions rather than requiring an agent to manually reproduce every browser interaction.

---

# 🌐 What Websites Can ApplyPilot Fetch Information From?

ApplyPilot's discovery layer is **not limited to one job board**.

Because Anakin Search operates over the live web, ApplyPilot can discover opportunities from different publicly accessible sources.

Depending on the search results, this can include:

* Official company career pages
* ATS-hosted career pages
* Job boards
* Recruitment platforms
* Other publicly accessible opportunity pages

The exact sources are dynamic because the agent searches the live web rather than using a fixed database.

---

# 🔎 What ApplyPilot Can Fetch

From a discovered opportunity, ApplyPilot can potentially retrieve and reason about information such as:

| Information                            | Supported |
| -------------------------------------- | --------: |
| Job title                              |         ✅ |
| Company                                |         ✅ |
| Job description                        |         ✅ |
| Skills/requirements                    |         ✅ |
| Responsibilities                       |         ✅ |
| Location                               |         ✅ |
| Internship/full-time classification    |         ✅ |
| Opportunity URL                        |         ✅ |
| Source/domain                          |         ✅ |
| Job status signals                     |         ✅ |
| Eligibility signals                    |         ✅ |
| Candidate-job matching                 |         ✅ |
| Application-related links              |         ✅ |
| Public application-page content        |         ✅ |
| Application form fields when reachable |         ✅ |
| CAPTCHAs / verification detection      |         ✅ |
| Login-protected personal information   |         ❌ |
| Private candidate information          |         ❌ |

---

# ⚡ What ApplyPilot Can Do on Websites

When the required website capability is available, the agent can:

### Read

* Search for opportunities
* Open opportunity pages
* Extract relevant information
* Inspect application-related pages
* Analyze requirements

### Reason

* Compare candidate profile with requirements
* Rank opportunities
* Determine likely eligibility
* Identify missing requirements
* Recommend whether to prepare an application

### Prepare

* Generate an application mission
* Generate a personalized cover letter
* Build an application checklist
* Identify required next steps

### Act / Inspect

Depending on available Anakin actions and the target website:

* Resolve available website actions
* Execute supported Wire actions
* Open opportunity pages
* Navigate to application destinations
* Inspect application forms
* Detect blockers

Anakin's Wire catalog supports both read and, for supported/authenticated actions, state-changing workflows; availability depends on the specific site's catalog and required authentication.

---

# 🚫 What ApplyPilot Does NOT Do

ApplyPilot is intentionally **not** an unrestricted autonomous job-submission bot.

## ❌ It does not guarantee application submission

An **Apply** button on a website does not guarantee that the agent can complete the application.

The destination may require:

* Login
* CAPTCHA
* Human verification
* Identity verification
* Unsupported application platform
* File upload
* Complex custom UI
* Multi-step authentication

---

## ❌ It does not bypass human verification

ApplyPilot detects verification barriers but does not pretend that they were successfully completed.

Examples:

```text
CAPTCHA
Cloudflare verification
"Verify you are human"
Security checks
Identity verification
```

These can result in:

```text
VERIFICATION_BLOCKED
```

---

## ❌ It does not submit an application without human approval

The final submission remains intentionally human-controlled.

This protects the user from accidentally submitting:

* Incorrect information
* Incorrect answers
* Wrong resume
* Wrong job
* Incorrect declarations
* Incorrect authorization information

---

## ❌ It does not access private accounts without authorization

ApplyPilot does not attempt to:

* Guess passwords
* Bypass authentication
* Access private accounts
* Steal session information
* Circumvent access controls

Account-connected website actions require the appropriate authenticated mechanism supported by the platform. Anakin's authenticated Wire flow supports account-connected actions through configured identities/credentials.

---

## ❌ It does not guarantee that every website is supported

Website behavior varies dramatically.

A site may have:

* Custom JavaScript
* Dynamic forms
* Authentication
* Bot protection
* Unsupported fields
* Unsupported workflow
* Application redirects

Therefore:

> **ApplyPilot reports what it actually accomplished rather than claiming success when a workflow was blocked.**

---

# 🧑‍💻 Human vs AI Responsibilities

| Task                          | ApplyPilot | Human |
| ----------------------------- | :--------: | :---: |
| Search opportunities          |      ✅     |       |
| Collect job information       |      ✅     |       |
| Analyze requirements          |      ✅     |       |
| Match candidate to role       |      ✅     |       |
| Rank opportunities            |      ✅     |       |
| Generate cover letter         |      ✅     |       |
| Build application checklist   |      ✅     |       |
| Inspect application page      |      ✅     |       |
| Detect verification barriers  |      ✅     |       |
| Review generated content      |            |   ✅   |
| Provide sensitive information |            |   ✅   |
| Resolve CAPTCHA               |            |   ✅   |
| Handle identity verification  |            |   ✅   |
| Final application approval    |            |   ✅   |
| Final submission              |            |   ✅   |

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │ Profile + Goal       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ApplyPilot UI      │
                    │     Streamlit        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Search Agent       │
                    │ Goal-driven queries  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Anakin Search     │
                    │    Live Web Data     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Opportunity Analysis │
                    │   LLM Reasoning      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Opportunity Ranking  │
                    │ Match + Eligibility  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Application Mission │
                    │ Cover Letter + Tasks │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Browser Inspection  │
                    │ Application Workflow│
                    └──────────┬───────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
              ┌──────────────┐   ┌────────────────┐
              │ Application  │   │ Verification / │
              │ Reachable    │   │ Unsupported    │
              └──────┬───────┘   └───────┬────────┘
                     │                   │
                     └─────────┬─────────┘
                               ▼
                    ┌──────────────────────┐
                    │   HUMAN APPROVAL     │
                    │ Final decision stays │
                    │ with the candidate   │
                    └──────────────────────┘
```

---

# 🧩 Technology Stack

### Frontend

* **Streamlit**
* Custom CSS
* Responsive dashboard UI

### AI / Reasoning

* OpenRouter
* LLM-based opportunity analysis
* Structured opportunity evaluation

### Web Agent Infrastructure

* **Anakin.io**
* Anakin Search API
* Anakin Wire
* Browser automation / web inspection

### Browser Automation

* Playwright

### Language

* Python

### Configuration

* `python-dotenv`
* Environment-based API credentials

---

# 📁 Project Structure

```text
applypilot/
│
├── app.py
│   └── Streamlit application and UI
│
├── agent.py
│   └── Opportunity discovery and ranking logic
│
├── ai_client.py
│   └── LLM / OpenRouter integration
│
├── anakin_client.py
│   └── Anakin API integration
│
├── browser_agent.py
│   └── Browser inspection and application workflow detection
│
├── mission.py
│   └── Application mission generation
│
├── database.py
│   └── Database module
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Secret and generated-file exclusions
│
└── README.md
    └── Project documentation
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/applypilot.git
cd applypilot
```

---

## 2. Create a virtual environment

### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Playwright browser

```bash
python -m playwright install chromium
```

---

# 🔐 Environment Variables

Create a `.env` file locally:

```env
OPENROUTER_API_KEY=your_openrouter_key
ANAKIN_API_KEY=your_anakin_key
```

### ⚠️ NEVER commit `.env`

The repository intentionally excludes:

```text
.env
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

API keys should never be placed directly inside source code or committed to GitHub.

For cloud deployment, use the deployment platform's secure secrets mechanism instead.

---

# ▶️ Run Locally

Start ApplyPilot with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ☁️ Deployment

ApplyPilot can be deployed using **Streamlit Community Cloud**.

Basic deployment flow:

```text
GitHub Repository
       ↓
Streamlit Community Cloud
       ↓
Select app.py
       ↓
Configure Secrets
       ↓
Deploy
```

For deployment, API credentials should be configured as secure secrets rather than committed to GitHub.

---

# 💳 API Usage & Credits

ApplyPilot uses Anakin for web-agent infrastructure, so live discovery and other Anakin operations consume credits according to the applicable Anakin pricing.

Current Anakin pricing lists:

* Search API: **3 credits/request**
* Browser API: **1 credit / 2 minutes**
* Wire: **varies by action**
* Agentic Search: **10 credits + 1 credit per URL**
* Basic scraping: **1 credit**

Exact costs can change, so users should check Anakin's current pricing/dashboard before running large-scale searches.

ApplyPilot therefore avoids unnecessary repeated discovery requests where possible.

---

# 🔒 Security & Privacy

ApplyPilot follows a **human-controlled automation model**.

The application:

* Does not hard-code API keys
* Uses environment variables for credentials
* Does not commit `.env`
* Does not intentionally bypass authentication
* Does not attempt to access private accounts without authorization
* Does not automatically submit job applications without human approval
* Reports verification blockers instead of pretending they were bypassed

Users should still avoid entering sensitive credentials into untrusted environments.

---

# 🧠 Design Philosophy

ApplyPilot is built around three principles:

## 1. Read

The agent should understand the live web rather than depend entirely on static datasets.

## 2. Reason

The agent should interpret the information and determine which opportunities actually matter to the candidate.

## 3. Act

The agent should move beyond recommendations and prepare actionable application workflows.

But:

> **Autonomy should stop where human judgment is required.**

That is why final application submission remains under human control.

---

# 🏆 Why ApplyPilot Fits Anakin Forge

Anakin Forge challenges developers to build AI agents that:

> **Read, Reason, and Act.**

ApplyPilot maps directly to those three stages.

### READ

```text
Live job discovery
Job descriptions
Requirements
Application pages
Website state
```

### REASON

```text
Candidate ↔ Job matching
Eligibility analysis
Opportunity ranking
Application recommendations
```

### ACT

```text
Generate application mission
Generate personalized cover letter
Open official opportunity
Inspect application workflow
Execute supported website actions
```

### HUMAN CONTROL

```text
Review
Approval
Final submission
```

The result is not just a chatbot that recommends jobs.

It is an **agentic workflow that moves from opportunity discovery toward application completion while keeping the candidate in control.**

---

# 🚧 Current Limitations

ApplyPilot is a hackathon prototype and therefore has practical limitations.

### Website variability

Every website has different layouts, workflows and security mechanisms.

### Application platforms

Not every application platform can be automatically operated.

### Authentication

Private or account-protected workflows require appropriate authentication and supported integrations.

### CAPTCHA / verification

Human verification may stop the browser workflow.

### File uploads

Some applications require resume or document uploads through custom interfaces that may not be supported by the current workflow.

### Custom questions

Applications may contain questions requiring candidate-specific judgment.

### Final submission

Final submission is intentionally human-controlled.

### Search freshness

Search results depend on the current state of the web and the sources returned by Anakin.

### API availability

The availability and cost of Anakin actions depend on Anakin's current APIs, supported catalogs and account configuration.

---

# 🔮 Future Improvements

Potential future versions could add:

* Resume parsing and job-specific resume tailoring
* Structured application-form field mapping
* More ATS integrations
* Application history
* Application tracking dashboard
* Deadline tracking
* Duplicate application detection
* Interview preparation
* Job-status monitoring
* Personalized application analytics
* Multi-agent application workflows
* Secure account-connected actions
* User-approved form autofill
* Application outcome tracking

---

# ⚠️ Responsible Automation

ApplyPilot is designed to **assist candidates, not impersonate them**.

The agent should not:

* Fabricate qualifications
* Invent work experience
* Misrepresent education
* Provide false answers
* Bypass security controls
* Submit applications without user approval
* Circumvent authentication

AI-generated application material should be reviewed by the candidate before submission.

---

# 📜 Disclaimer

ApplyPilot is an experimental hackathon project.

It does not guarantee:

* Job availability
* Eligibility
* Application acceptance
* Interview selection
* Successful application submission
* Website compatibility
* Accuracy of AI-generated content

Users are responsible for reviewing information and approving applications before submission.

---

# 👩‍💻 Built For

**Anakin Forge Hackathon 2026**

**Challenge:**

### Build AI Agents That Read, Reason, and Act

**Project:**

### ApplyPilot — Autonomous Job Discovery & Application Preparation Agent

---

# ⭐ Project Vision

ApplyPilot's long-term goal is simple:

> **Turn job searching from a repetitive browsing task into an intelligent, personalized application workflow.**

Instead of:

```text
Search → Open → Read → Compare → Repeat
```

ApplyPilot aims for:

```text
Tell the agent your goal
        ↓
Discover
        ↓
Reason
        ↓
Prioritize
        ↓
Prepare
        ↓
Inspect
        ↓
Review
        ↓
Approve
        ↓
Apply
```

### ApplyPilot

**Find the opportunity.
Understand the fit.
Prepare the application.
Keep the human in control.**
