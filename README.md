                                         #🎓 Bridging the Gap
                         University Curricula vs. MENA Job Market Skills
![cover](images/cover.png)

> A graduation project analyzing the skills gap between Jordanian university programs and real employer demands across the MENA region.

---

## 📌 Project Overview

This project investigates whether the skills taught in Jordanian university curricula align with what employers actually require in the MENA job market. Using a combination of web scraping, LLM-powered skill extraction, machine learning models, and interactive dashboards, we quantify the gap and provide actionable, evidence-based recommendations for curriculum reform.

**Main Research Question:**
> *To what extent do the skills taught in Jordanian university programs match the skills demanded by employers in the MENA job market?*

---

## 👥 Our Team

| Name | Role |
|------|-------|
| Sara alzwiri | Job market data — scraping, cleaning, analysis, models |
| Yusra almuhtaseb | University curriculum data — PDF extraction, LLM skill mapping, cleaning , power BI|

---
## 🔍 ???

After studying skills extracted from official course descriptones from three chosen Jordanian universities:
[The University of Petra]
[Princess Sumaya University for Technology]
[Al-Zaytoonah University of Jordan]
across eight high-demand majors:
(Business Intelligence, Computer Science, Software Engineering, Data Science & AI, Cybersecurity, Accounting, Business Administration, and E-Marketing & Digital Marketing)
then comapring them to 2k job listings scraped from [bayt.com] across 4 MENA countries:
UAE
KSA
EGYPT
JORDAN
we found that:
**no university covers more than 22% of the skills employers actually ask for** — meaning at least **78% of job-required skills go untaught** across every program we examined.

Each university has relative strengths, but none comes close to full market alignment:

- **PSUT** leads in Computer Science (19% match) and Data Science (10% match)
- **ZUJ** leads in Accounting (21% match), Cybersecurity (15% match), and Business Intelligence (12% match)
- **UOP** leads in Software Engineering (22% match) and Business Administration (16% match)

The most critically absent skills across all programs were: **AI/ML, Cloud Computing, ERP systems (SAP/Oracle), Agile/Scrum, DevOps,** and BI tools like **Power BI and Tableau**.

> *Note: Coverage figures are based solely on skills explicitly stated in course syllabi and do not necessarily reflect the full scope of what is taught in practice.*

---

## 🗃️ Datasets we used

### University Curriculum Dataset
- **Source:** Official course syllabi and study-plan PDFs from UOP, PSUT, ZUJ
- **Extraction method:** Manual extraction then LLM-powered skill extraction with a structured prompt
- **Size:** 3,692 skill rows | 551 unique course codes across 3 universities
- **Fields:** University, Major, Course Code, Course Name, Skill

### Job Market Dataset
- **Source:** Bayt.com (scraped using Selenium)
- **Coverage:** 4 MENA countries — UAE, Saudi Arabia, Egypt, Jordan
- **Size:** 2,000 job postings across 8 sectors
- **Fields:** Job Title, Company, Location, Country, Sector, Skills, Experience Level, URL

### Skill Synonym Dictionary
- 54 job market skills mapped to 209 curriculum equivalents
- Bridges terminology differences between industry and academia (e.g., "Collaboration" → "Teamwork, Group Work, Team Projects")

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| Data Collection | Python, Selenium, BeautifulSoup |
| Data Processing | Pandas, OpenPyXL |
| Machine Learning | Scikit-learn (K-Means, Random Forest), MLxtend (Apriori) |
| Visualization | Matplotlib, Seaborn |
| BI Dashboard | Power BI |
| LLM Skill Extraction | Claude (Anthropic) |
| Documentation | Markdown |
| Version Control | GitHub |

---

## 🤖 Models Built

| # | Model Type | Purpose |
|---|-----------|---------|
| 1 | K-Means Clustering | Group skills into patterns across sectors |
| 2 | Association Rule Mining (Apriori) | Discover co-occurring job skill bundles |
| 3 | TF-IDF + Cosine Similarity | Measure overlap between university and market skills |
| 4 | Random Forest Classifier | Predict job sector from required skills |

---

## 📊 Power BI Dashboard

The dashboard has 4 pages:

1. **Executive Overview** — KPI cards, skill status donut, top market gaps treemap
2. **Market Alignment Analysis** — University vs. market bar chart, MENA jobs map
3. **Job Evidence** — Full table of job postings supporting market skill data
4. **Course Evidence** — Full table of university courses supporting curriculum data

---

## 📋 Requirements

```
pandas
openpyxl
selenium
beautifulsoup4
scikit-learn
mlxtend
matplotlib
seaborn
requests
```

---

## ⚠️ Limitations

- Job market data was collected as a sample; Egypt and KSA counts show low variance across sectors, likely due to scraping caps on the source website.

-Job postings from Jordan were inherently limited in volume, as Bayt.com contains significantly fewer Jordanian listings compared to other MENA countries such as the UAE and Saudi Arabia, this reflects the platform's regional usage patterns rather than a data collection issue.

- Curriculum skill coverage is based on explicit mentions in course descriptions only — actual classroom content may be broader.

- The Skill DNA Match percentage compares extracted skill names after synonym normalization; exact matching may undercount partial overlaps.

---

## 📄 License

This project was developed for academic purposes as a graduation project at the University of Petra. Data collected from Bayt.com was used solely for non-commercial research.
