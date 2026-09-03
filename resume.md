---
layout: page
title: Resume
permalink: /resume/
download_pdf: resume.pdf
toc: true
---

# 👋🏻 Kiem Pham

---

**Data Engineer - VNG Corporation**
---


📧 phamkiem.ns@gmail.com

☎️ 0941840068

🏠 Ho Chi Minh City 

🔗 [dataspi.github.io/DataSpi](https://dataspi.github.io/DataSpi/)

---
<br />

> Data/Analytics Engineer with 3+ years of experience turning raw operational data into trusted, well-modeled datasets for analytics. Strong in `Python`, `SQL`, `PostgreSQL`, `BigQuery`, `dbt`, and `AWS Glue`, with hands-on delivery of dimensional data models, tested ELT pipelines, and a self-service semantic layer (`Malloy`). Proven ability to bridge engineering and business stakeholders — having worked as both a BI/HR analyst and a data engineer — to deliver data products people actually trust and use, and to mentor non-technical teammates into full ownership of the systems I build.

<a id="projects-section"></a>

# 🏗️ Highlighted Projects

> More details on my project, visit [Projects](https://dataspi.github.io/DataSpi/projects/)

### 1. Real Estate Analytics Platform

*Sep 2025 – Present*

Built and now operate an end-to-end analytics engineering pipeline for Vietnam's real estate market (~200K+ for-sale & rental listings across HCMC & Hanoi), following a medallion architecture on `BigQuery`: async scrapers land raw listings, `dbt` staging models deduplicate and clean into a silver layer, and `dbt` mart models build a gold layer surfaced through a `Malloy` semantic layer for self-service metrics. Data quality is enforced with `dbt` schema tests plus custom singular tests (e.g. negative price/area, price-per-m² outliers). The pipeline runs on a scheduled, fail-fast orchestrator with logging, and results are published via an interactive `Looker Studio` dashboard and detailed analysis reports.

**Tech stack:** `Python`, `BigQuery`, `dbt`, `Malloy`, `curl_cffi`, `BeautifulSoup`, `Google Looker Studio`
[GitHub](https://github.com/DataSpi/scrape-batdongsan-data), [Publication](https://spyno.substack.com/p/i-xem-chung-cu-cung-tho-so-p2)

### 2. CI/CD-Orchestrated Logistics Reporting Pipeline

*Nov 2025 – Present*

Built an event-driven ELT pipeline on `GitHub Actions` for two freight-forwarding clients (retail & food logistics), replacing manual daily reporting. Scheduled workflows scrape order/booking data into `BigQuery` bronze tables, then automatically trigger a chained workflow (`workflow_run`) that runs `dbt build` for silver/mart models, followed by a report workflow that pushes milestone and TEU reports to stakeholders — a full scrape-to-report pipeline with zero manual intervention. Engineered a reusable composite action for secrets/env provisioning across pipelines, plus failure-artifact capture (`upload-artifact`) and manual `workflow_dispatch` triggers for on-demand reruns and debugging.

**Tech stack:** `Python`, `GitHub Actions` (CI/CD, cron & event-driven orchestration), `dbt`, `BigQuery`, `Google Sheets API`
[GitHub](https://github.com/DataSpi/silky_project)

### 3. Building an Internal AI Assistant *(Sep 2023 - Present)*

Internal assistant for policy and knowledge lookup, letting employees retrieve company information in natural language. `OpenAI API`, `Langchain`, `Pinecone` - [GitHub](https://github.com/DataSpi/itl-inno-award-2023)

### 4. Labor Market Analysis from Job Listing Sites *(Aug 2023 - Present)*

Automated job posting collection and analysis to track hiring trends in Vietnam's data job market. `Python`, `Selenium`, `BeautifulSoup` - [GitHub](https://github.com/DataSpi/scraping-jobs),  [Publication](https://spyno.substack.com/p/thi-truong-tuyen-dung-cac-jobs-ve)

### 5. Employee Mental Health & Stress Survey Analytics *(Aug 2023 - Sep 2023)*

Analyzed employee and manager survey data to compare stress and mental health perceptions across cohorts. `Pandas`, `Google Forms` — [Project Link](https://www.notion.so/Survey-about-Mental-Health-Stress-status-of-ITL-Employees-Aug2023-a4e3286b13f34e5a933361d19f796e76?pvs=21)

---

# 💻 Work experience

## VNG Corporation - Data Engineer

*Sep 2025- Now (1yr)*

**Technical Core:** `Python`, `PostgreSQL`, `dbt`, `MetricFlow`, `AWS Glue`, `Hasura`, `Lightdash`.

**Key Projects & Impact:**

- Engineering Productivity Data Platform (TPMF): Designed a Kimball star-schema warehouse (a shared KPI-snapshot fact plus atomic-grain detail facts for drill-down) covering 45 engineering KPIs across three orgs (software delivery, QA/testing, People/HR), implemented as a `dbt` project on `PostgreSQL` with staging → intermediate → gold (mart) layers and KPI logic centralized in a `dbt` Semantic Layer (`MetricFlow`, incl. ratio/derived metrics). Built `Python` ETL for both file-based sources (Excel/CSV loaders into a raw landing schema) and live API sources (`GitLab`, `GitHub`, `SonarCloud`, an internal OAuth2 Service Desk API), with `dbt` schema and custom singular data-quality tests, running as cron pipelines on dedicated internal servers.
- Surfaced the modeled metrics through a read-only `MCP` server for natural-language querying in Claude, a `Lightdash` BI layer reading the marts directly, and an automated monthly executive report (self-contained offline HTML + `PPTX`).
- Data Platform & Migration: Designed and operated an `Odoo-to-ATS` data migration pipeline with reconciliation controls to maintain data integrity and prevent data loss at go-live.
- ETL/ELT Automation: Developed `Python` + `Boto3` automation for `AWS Glue` jobs, reducing manual operations and improving pipeline stability and run-time consistency.
- Managed `PostgreSQL`/`Hasura` workloads, including automated monthly partitioning, custom SQL functions, and scheduled maintenance (`pg_cron`) to keep query latency stable as data volume grew.
- Data Modeling & Consumption: Integrated `Malloy` semantic modeling into the `IPay` environment to improve self-service analytics and natural language querying accuracy.
- Monitoring & Documentation: Established technical documentation standards and implemented monitoring/alerting flows with operations teams to improve reliability and incident response.

## LEGO Manufacturing Vietnam - Data Analyst

 *Sep 2024 - Aug 2025 (1yr)*

- Reverse-engineered `UKG` timesheet data to resolve a high-stakes overtime calculation conflict (legal 300h/year cap vs. LEGO's actual pay policy vs. shift-based break rules); presented the logic to C&B leadership and cross-functional DA teams (Packing, Moulding), and it was adopted as the standard OT calculation used factory-wide — ahead of a global system fix that remained pending over a year later.
- Mentored a non-technical successor to full ownership of the PPC HR `Power BI` reporting system through a 3-week hands-on training program and detailed documentation; the system ran uninterrupted for 6+ months post-handover, and I remained the trusted technical advisor for two successive report owners after leaving LEGO.
- Designed and delivered 3 targeted reporting solutions for the PPC department, covering: headcount & workforce planning, turnover, D&I, L&D, overtime, absenteeism, retention policy analysis to support strategic decision-making.
- Produced monthly executive summaries from `Power BI` dashboards for senior leadership.
- Partnered with BI Manufacturing on Factory Huddle and Visual Factory reports used in daily operations and leadership meetings.
- Delivered an end-to-end data flow for LEGO Vietnam's 3-month Active Summer program using `Google Forms API` + `Python` + `Power BI`.
- Supported development of a `Power App` solution for gym consent and reservations, enhancing process efficiency and user experience.


## ITL Corporation 

### Data Analyst

*Aug 2023 - Sep 2024 (1yr 1m)*

- Conducted comprehensive analyses and generated detailed reports using data from the HRMS database.
- Developed a comprehensive data pipeline spanning database, data warehouse, and reporting phases using `MSSQL` and `PostgreSQL`.
- Streamlined data using `SQL` and `Python`.
- Visualized and created reports using `Power BI`.
- Collected and analyzed job listings from job-listing sites using `BeautifulSoup`, `Selenium`, and `Pandas` to generate comprehensive reports on the recruiting market.
- Led comprehensive internal surveys to assess key HR metrics, including stress levels, employee satisfaction, and employee engagement.
- Collaborated with IT to develop an internal AI assistant leveraging the `OpenAI API` and `Langchain`.

### Human Resources Management Trainee

*Feb 2022 - Aug 2023 (1yr 7m)*

- Calculated monthly salary add-ons for the container fleet to ensure accurate and timely compensation adjustments.
- Provide support by answering questions related to company policies.
- Processed employee paperwork related to union matters and resignations.
- Planned employee costs for 2024.

---

# 🛠 Skills

## 🔭 Technical Skills

### Analytics Engineering

* Dimensional Modeling (Star Schema), Medallion Architecture (Bronze/Silver/Gold), Data Warehouse & Data Marts
* ETL/ELT Pipelines, `dbt` (models, schema & custom data quality tests), Semantic Modeling (`Malloy`)

### Data & Programming

* Advanced `SQL` (`PostgreSQL`, `BigQuery`, `MSSQL`)
* `Python` (`pandas`, `BeautifulSoup`, `Selenium`, `matplotlib`, `plotly`)

### Data Platform & CI/CD

* `PostgreSQL`, `BigQuery`, `dbt`, `AWS Glue`, `Airflow`, `pg_cron`, `Git`, `Hasura`
* `GitHub Actions` (scheduled & event-driven workflow orchestration, dbt-in-CI, secrets management, reusable composite actions)

### Business Analytics

* `Power BI`, `DAX`, KPI Development, Executive Reporting, Self-service Analytics

### Collaboration

* Cross-functional stakeholder collaboration, technical documentation, mentoring & knowledge transfer, AI-assisted development (`Cursor`, `VS Code`)
* Public writing on data careers & self-taught learning — [Threads](https://www.threads.com/@spyno_kiem/post/C8CqeQmS3kM) post reached 4K+ views, 347 likes, 54 reposts; longer-form companion piece on [Substack](https://spyno.substack.com/p/kinh-nghiem-tu-hoc-python-cho-phan)


---

## 💭 Soft Skills

### Languages

- Vietnamese: Native or bilingual proficiency
- English: Full professional proficiency (IELTS 7.0)

---

## 🎓 Education

### Bachelor Degree

- Human Resources Management - University of Economics HCMC - *(Sep 2018 - Dec 2021)*

---
