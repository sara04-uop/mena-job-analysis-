import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# ── style ──────────────────────────────────────────────────
COLORS  = ["#2196F3","#4CAF50","#FF5722","#9C27B0",
           "#FF9800","#00BCD4","#E91E63","#607D8B"]
BLUE    = "#2196F3"
RED     = "#FF5722"
GREEN   = "#4CAF50"

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 140, "figure.autolayout": True})

OUTPUT = "C:/Users/Toshiba/OneDrive/Desktop/graduation project files/"
FILE   = "C:/Users/Toshiba/OneDrive/Desktop/graduation project files/data for analysis.xlsx"

def save(fig, name):
    path = OUTPUT + name
    fig.savefig(path, bbox_inches="tight")
    print(f"  Saved → {path}")
    plt.close(fig)


# ============================================================
# LOAD DATA
# ============================================================
print("Loading data...")

df_uni = pd.read_excel(FILE, sheet_name="uni", header=1)
df_job = pd.read_excel(FILE, sheet_name="jobs", header=1)
df_uni.columns = df_uni.columns.str.strip()
df_job.columns = df_job.columns.str.strip()

# -- uni columns
uni_skill  = [c for c in df_uni.columns if "skill"       in c.lower()][0]
uni_major  = [c for c in df_uni.columns if "major"       in c.lower()][0]
uni_course = [c for c in df_uni.columns if "course name" in c.lower()][0]

df_uni = df_uni[[uni_major, uni_course, uni_skill]].dropna()
df_uni.columns = ["Major", "Course", "Skill"]
df_uni["Skill"] = df_uni["Skill"].str.strip()

# -- job columns
job_skill  = [c for c in df_job.columns if "skill"  in c.lower()][0]
job_sector = [c for c in df_job.columns if "sector" in c.lower()][0]

df_job = df_job[[job_sector, job_skill]].dropna(subset=[job_skill])
df_job.columns = ["Sector", "Skills_raw"]
df_job["Skills"] = df_job["Skills_raw"].apply(
    lambda x: [s.strip() for s in str(x).split(",") if s.strip()])
df_job = df_job[df_job["Skills"].apply(len) > 0].reset_index(drop=True)

all_job_skills = [s for lst in df_job["Skills"] for s in lst]

print(f"  University skills : {df_uni['Skill'].nunique()}")
print(f"  Job postings      : {len(df_job)}")
print(f"  Job skills (unique): {len(set(all_job_skills))}")


# ============================================================
# FIG 01 — Skill Frequency Side-by-Side
# ============================================================
print("\nFig01 — Skill Frequency...")

uni_freq = df_uni["Skill"].value_counts().head(25)
job_freq = pd.Series(Counter(all_job_skills)).sort_values(ascending=False).head(25)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

ax1.barh(uni_freq.index[::-1], uni_freq.values[::-1], color=BLUE)
ax1.set_title("Top 25 University Curriculum Skills", fontweight="bold", fontsize=13)
ax1.set_xlabel("Number of courses teaching this skill")

ax2.barh(job_freq.index[::-1], job_freq.values[::-1], color=RED)
ax2.set_title("Top 25 Job Market Required Skills (MENA)", fontweight="bold", fontsize=13)
ax2.set_xlabel("Number of job postings requiring this skill")

fig.suptitle("University vs. Job Market — Skill Frequency Comparison",
             fontsize=15, fontweight="bold")
save(fig, "fig01_skill_frequency.png")


# ============================================================
# FIG 02 — K-Means Clusters (PCA 2D scatter)
# ============================================================
print("Fig02 — K-Means Clusters...")

job_docs = df_job["Skills"].apply(lambda x: " ".join(x))
tfidf_km = TfidfVectorizer(max_features=200, min_df=2)
X_km     = tfidf_km.fit_transform(job_docs).toarray()

km = KMeans(n_clusters=4, random_state=42, n_init=10)
labels_km = km.fit_predict(X_km)
df_job["Cluster"] = labels_km

# Name the clusters based on their top skills
feature_names_km = tfidf_km.get_feature_names_out()
cluster_names = {}
for c in range(4):
    top = km.cluster_centers_[c].argsort()[-3:][::-1]
    top_words = [feature_names_km[i] for i in top]
    joined = " ".join(top_words).lower()
    if "accounting" in joined or "financial" in joined:
        cluster_names[c] = "Core Finance &\nAccounting"
    elif "python" in joined or "software" in joined or "development" in joined:
        cluster_names[c] = "Tech &\nEngineering"
    elif "sales" in joined or "crm" in joined or "operations" in joined:
        cluster_names[c] = "Sales &\nCommercial"
    else:
        cluster_names[c] = "Business &\nCompliance"

pca   = PCA(n_components=2, random_state=42)
X_2d  = pca.fit_transform(X_km)
var   = pca.explained_variance_ratio_.sum() * 100

fig, ax = plt.subplots(figsize=(10, 7))
for c in range(4):
    mask = labels_km == c
    ax.scatter(X_2d[mask, 0], X_2d[mask, 1],
               label=cluster_names[c], alpha=0.65, s=60, color=COLORS[c])

centers_2d = pca.transform(km.cluster_centers_)
ax.scatter(centers_2d[:, 0], centers_2d[:, 1],
           marker="X", s=280, c="black", zorder=5, label="Cluster centers")

ax.set_title(f"K-Means Clustering — Job Postings by Skill Profile (k=4)\n"
             f"Each dot = one job posting   |   Variance captured: {var:.1f}%",
             fontweight="bold", fontsize=13)
ax.set_xlabel("Skill similarity dimension 1\n"
              "( technical jobs)")
ax.set_ylabel("Skill similarity dimension 2\n"
              "(Business jobs")
ax.legend(title="Cluster", loc="best", fontsize=10)
save(fig, "fig02_kmeans_clusters.png")


# ============================================================
# FIG 03 — Top 10 Association Rules by Lift
# ============================================================
print("Fig03 — Association Rules...")

te       = TransactionEncoder()
te_array = te.fit_transform(df_job["Skills"].tolist())
df_te    = pd.DataFrame(te_array, columns=te.columns_)

freq_items = apriori(df_te, min_support=0.05, use_colnames=True)
rules      = association_rules(freq_items, metric="lift", min_threshold=1.2)
rules      = rules.sort_values("lift", ascending=False).head(10)

rules["rule"] = (rules["antecedents"].apply(lambda x: ", ".join(list(x))) +
                 "  →  " +
                 rules["consequents"].apply(lambda x: ", ".join(list(x))))

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(rules["rule"][::-1], rules["lift"][::-1],
               color=COLORS[:10][::-1], edgecolor="white", linewidth=0.5)

for bar, val in zip(bars, rules["lift"][::-1]):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}", va="center", fontsize=10, fontweight="bold")

ax.set_title("Top 10 Skill Pairs That Always Appear Together in Job Postings\n"
             "(Lift score — higher means stronger co-occurrence)",
             fontweight="bold", fontsize=13)
ax.set_xlabel("Lift score  (1.0 = independent,  3.0+ = strongly linked)")
ax.set_xlim(0, rules["lift"].max() * 1.18)
save(fig, "fig03_top_association_rules.png")


# ============================================================
# FIG 04 — Top Distinctive Skills per Sector (fully automatic)
# ============================================================
print("Fig04 — Skills per Sector...")

from collections import Counter as _Counter

sector_counts = df_job["Sector"].value_counts()
valid_sectors = sector_counts[sector_counts >= 20].index
df_plot       = df_job[df_job["Sector"].isin(valid_sectors)].copy()
sectors       = sorted(df_plot["Sector"].unique())
n_sectors     = len(sectors)

# ── Step 1: auto-detect generic skills ──────────────────────
# A skill is generic if it appears at >10% rate in almost every sector
all_skills_set = set(s for lst in df_plot["Skills"] for s in lst)
skill_sector_presence = {}
for skill in all_skills_set:
    count = sum(
        1 for sector in sectors
        if sum(1 for lst in df_plot[df_plot["Sector"]==sector]["Skills"] if skill in lst)
           / len(df_plot[df_plot["Sector"]==sector]) > 0.10
    )
    skill_sector_presence[skill] = count

# Skills in (n_sectors - 1) or more sectors = automatically generic
AUTO_GENERIC = {s for s, c in skill_sector_presence.items() if c >= n_sectors - 1}

# ── Step 2: compute lift per sector ─────────────────────────
ncols = 2
nrows = (n_sectors + 1) // ncols
TOP_N    = 12
MIN_FREQ = 0.05

fig, axes = plt.subplots(nrows, ncols, figsize=(18, nrows * 5))
axes = axes.flatten()

for i, sector in enumerate(sectors):
    # Auto-exclude words that are part of the sector name (prevent circular results)
    sector_words = set(sector.lower().split())

    in_jobs  = df_plot[df_plot["Sector"] == sector]["Skills"]
    out_jobs = df_plot[df_plot["Sector"] != sector]["Skills"]
    n_in, n_out = len(in_jobs), len(out_jobs)

    in_counts, out_counts = _Counter(), _Counter()
    for lst in in_jobs:
        for s in lst: in_counts[s] += 1
    for lst in out_jobs:
        for s in lst: out_counts[s] += 1

    lift_scores = {}
    for skill, cnt in in_counts.items():
        skill_words = set(skill.lower().split())
        if skill in AUTO_GENERIC:            # auto-remove generic skills
            continue
        if skill_words & sector_words:       # auto-remove sector-name leakage
            continue
        rate_in  = cnt / n_in
        rate_out = out_counts.get(skill, 0) / n_out
        if rate_in < MIN_FREQ:
            continue
        lift_scores[skill] = (rate_in / (rate_out + 0.01), rate_in)

    top_skills   = sorted(lift_scores.items(), key=lambda x: -x[1][0])[:TOP_N]
    skill_names  = [s.title() for s, _ in top_skills][::-1]
    lift_values  = [v[0] for _, v in top_skills][::-1]
    freq_values  = [v[1] for _, v in top_skills][::-1]

    ax   = axes[i]
    bars = ax.barh(skill_names, lift_values,
                   color=COLORS[i % len(COLORS)],
                   edgecolor="white", linewidth=0.5)

    for bar, lift, freq in zip(bars, lift_values, freq_values):
        ax.text(bar.get_width() + 0.03,
                bar.get_y() + bar.get_height() / 2,
                f"×{lift:.1f}  ({freq:.0%})",
                va="center", fontsize=8.5, color="#333333")

    ax.set_title(f"{sector}  (n={n_in})", fontweight="bold", fontsize=13)
    ax.set_xlabel("Lift score  (how much MORE than other sectors)")
    ax.set_xlim(0, max(lift_values) * 1.35)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle(
    "Top Distinctive Skills per Job Sector\n"
    "(Lift score — fully automatic, no manual rules: "
    "generic skills and sector-name words excluded by algorithm)",
    fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
fig.savefig(OUTPUT + "fig04_skills_per_sector.png", bbox_inches="tight", dpi=140)
print("  Saved → " + OUTPUT + "fig04_skills_per_sector.png")
plt.close(fig)

print("\nAll 4 charts saved successfully.")
print("Files saved in:", OUTPUT)