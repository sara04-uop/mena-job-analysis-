#                                            🎓 Bridging the Gap
##                            University Curricula vs. MENA Job Market Skills
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
## 🔍 Our Project's Story

After studying skills extracted from official course descriptones from three chosen Jordanian universities:
<img width="50" height="50" alt="petra" src="https://github.com/user-attachments/assets/e7b21083-def2-4b88-8227-f8bccdb221b2" />[The University of Petra](www.uop.edu.jo)

<img width="50" height="50" alt="psut" src="https://github.com/user-attachments/assets/c78a3115-c0dc-4670-8526-ea0e5615e44b" />[Princess Sumaya University for Technology](psut.edu.jo)

<img width="50" height="50" alt="zuj" src="https://github.com/user-attachments/assets/58288d6d-df1b-4eca-a854-c346da959912" />[Al-Zaytoonah University of Jordan](www.zuj.edu.jo)

across eight high-demand majors:

(Business Intelligence, Computer Science, Software Engineering, Data Science & AI, Cybersecurity, Accounting, Business Administration, and E-Marketing & Digital Marketing)

then comapring them to 2k job listings scraped from [bayt.com](www.Bayt.com) across 4 MENA countries:

![uae](https://flagcdn.com/24x18/ae.png) UAE

![ksa](https://flagcdn.com/24x18/sa.png)KSA

![egy](https://flagcdn.com/24x18/eg.png)EGYPT

![jor](https://flagcdn.com/24x18/jo.png)JORDAN

### 🤖 **we found that:**

**1-no university covers more than 22% of the skills employers actually ask for** — meaning at least **78% of job-required skills go untaught** across every program we examined.

**2-The most critically absent skills across all programs were: *AI/ML, Cloud Computing, ERP systems (SAP/Oracle), Agile/Scrum, DevOps,* and BI tools like *Power BI and Tableau*.**

> *Note: Coverage figures are based solely on skills explicitly stated in course syllabi and do not necessarily reflect the full scope of what is taught in practice.*

### 🤖 How the Job Market Actually Groups Itself

To go beyond manual categorization, we used **K-Means Clustering (k=4)** to let the data speak for itself — grouping 2,000 job postings purely by their skill profiles, with no human labels.

The model discovered **4 distinct skill clusters** that naturally emerged from the market:

![K-Means Clustering — Job Postings by Skill Profile](images/fig02_kmeans_clusters.png)

 **The market itself drew this line. By clustering 2,000 job postings 
 purely by skill patterns, the algorithm confirmed what the gap analysis shows: 
 *technical and business roles demand fundamentally different skill sets*, 
 meaning universities cannot close the gap with a single shared curriculum fix.**

> Note:The clusters were **not predefined** — the algorithm found them on its own, which validates that these are real, distinct skill demands in the market.


---

## 🗃️ [Datasets we used]([Data File](../data/processed/Curriculum_vs_Job_Market_Skills_Gap_Analysis_Final.xlsx)

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
