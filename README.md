<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg" alt="Amazon Logo" width="300" />
</div>

<h1 align="center">Amazon Electronics Market Intelligence</h1>
<h2 align="left">DVA Capstone 2 — Group E_G1</h2>

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange?style=flat-square&logo=jupyter)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-blue?style=flat-square&logo=tableau)
![ETL](https://img.shields.io/badge/Pipeline-ETL-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

> **Identifying which Amazon Electronics product categories deliver the highest customer value**
> — through discount analysis, rating quality, and review engagement.

---

## 📌 Problem Statement

Which product categories on Amazon Electronics perform best in terms of:
- 🌟 **Customer satisfaction** (ratings)
- 💬 **Engagement** (review count)
- 🏷️ **Pricing strategy** (discount levels)

This project enables **data-driven decisions** for pricing optimization, product positioning, and category-level strategy.

---



## 📁 Repository Structure

```text
E_G1_DVACapstone2/
├──  DVA-focused-Portfolio
├── DVA-oriented-Resume
├── data/
│   ├── raw/                        # Raw scraped dataset (never edited)
│   └── processed/                  # Cleaned, analysis-ready dataset
├── docs/
│   └── data_dictionary.md          # Schema, rules & data quality notes
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
├── reports/
│   ├── presentation.pdf
│   └── project_report.pdf
├── scripts/
│   └── etl_pipeline.py
├── tableau/
     ├── dashboard_links.md
     └── screenshots/

```

---

## 🔄 Project Workflow

```mermaid
flowchart LR
    %% Nodes and Flow
    A[(📥 Raw Data\nuncleaned.csv)]:::raw -->|Ingest| B[🧹 Data Cleaning\n& Imputation]:::step
    B --> C[🔧 Feature Eng &\nCategorization]:::step
    C --> D[(✅ Processed Data\ncleaned.csv)]:::clean

    D -->|Feeds| E[📊 Exploratory\nData Analysis]:::analysis
    D -->|Feeds| F[📈 Statistical\nAnalysis]:::analysis

    E --> G[📉 Tableau\nDashboard]:::viz
    F --> G

    G --> H((🎯 Final Delivery\nReport & Dash)):::final

    %% Custom Colors for Visual Hierarchy
    classDef raw fill:#ffcccc,stroke:#cc4444,stroke-width:2px,color:#7a0000
    classDef step fill:#ede9fe,stroke:#7c3aed,stroke-width:1px,color:#3b0764
    classDef clean fill:#cce5ff,stroke:#185fa5,stroke-width:2px,color:#042c53
    classDef analysis fill:#fef08a,stroke:#ca8a04,stroke-width:1px,color:#713f12
    classDef viz fill:#ffedd5,stroke:#ea580c,stroke-width:2px,color:#7c2d12
    classDef final fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
```

## 🛠️ Full Data Cleaning Pipeline

```mermaid
flowchart TD
    subgraph Phase1 [1. Initial Cleaning]
        direction LR
        A([📥 Raw Data]):::input --> B[🔍 Quality Check]:::step --> C[🩹 Impute Nulls]:::step --> D[🗑️ Drop Duplicates]:::step
    end

    subgraph Phase2 [2. Transformations]
        direction LR
        E[🔢 Data Types]:::step --> F[💰 Prices]:::step --> G[🔤 Format Text]:::step
    end

    subgraph Phase3 [3. Enrichment & Export]
        direction LR
        H{{"⭐ Categories"}}:::critical --> I[🔧 New Features]:::step --> J([✅ Clean Data]):::output
    end

    %% Direct connections between phases to save space
    Phase1 --> Phase2 --> Phase3

    %% Custom Colors
    classDef input    fill:#ffcccc,stroke:#cc4444,stroke-width:2px,color:#7a0000
    classDef step     fill:#ede9fe,stroke:#7c3aed,stroke-width:1px,color:#3b0764
    classDef critical fill:#ccfdf0,stroke:#0f6e56,stroke-width:2px,color:#04342c
    classDef output   fill:#cce5ff,stroke:#185fa5,stroke-width:2px,color:#042c53
    
    %% Clean border style
    style Phase1 fill:none,stroke:#b0bec5,stroke-dasharray: 5 5
    style Phase2 fill:none,stroke:#b0bec5,stroke-dasharray: 5 5
    style Phase3 fill:none,stroke:#b0bec5,stroke-dasharray: 5 5
```

<br>

### 🎯 Why Each Step Matters

```mermaid
flowchart LR
    %% Phase 1
    subgraph P1 [1. Initial Cleaning]
        direction LR
        S1[🩹 Impute Nulls] ==> R1>Essential for accurate ratings & review counts]
        S2[🗑️ Drop Duplicates] ==> R2>Guarantees reliable & unique engagement metrics]
    end

    %% Phase 2
    subgraph P2 [2. Transformations]
        direction LR
        S3[🔢 Data Types] ==> R3>Enables correct numeric comparisons]
        S4[💰 Prices] ==> R4>Forms baseline for valid discount calculations]
        S5[🔤 Format Text] ==> R5>Ensures consistent category grouping]
    end

    %% Phase 3
    subgraph P3 [3. Enrichment & Export]
        direction LR
        S6{{"⭐ Categories (Critical)"}} ==> R6>Enables category-level analysis & strategy]
        S7[🔧 New Features] ==> R7>Facilitates best-seller & coupon segmentation]
        S8[✅ Clean Data] ==> R8>Ensures no gaps in Tableau reporting]
    end

    %% Invisible links to stack subgraphs neatly
    P1 ~~~ P2 ~~~ P3

    %% Custom Styling
    classDef step fill:#ede9fe,stroke:#7c3aed,stroke-width:1px,color:#3b0764
    classDef critical fill:#ccfdf0,stroke:#0f6e56,stroke-width:2px,color:#04342c
    classDef reason fill:#f0f8ff,stroke:#0369a1,stroke-width:1px,color:#000
    
    class S1,S2,S3,S4,S5,S7,S8 step
    class S6 critical
    class R1,R2,R3,R4,R5,R6,R7,R8 reason

    style P1 fill:none,stroke:#b0bec5,stroke-dasharray: 5 5
    style P2 fill:none,stroke:#b0bec5,stroke-dasharray: 5 5
    style P3 fill:none,stroke:#b0bec5,stroke-dasharray: 5 5
```

---

### Pipeline Steps Summary

| Step | What Happens |
|------|-------------|
| 🔍 **Extraction** | Ingest raw CSV without modification |
| 🧹 **Cleaning** | Remove duplicates, fix types, parse text numerics |
| 💰 **Price Processing** | Resolve & impute listed/current price, filter outliers |
| 🏷️ **Category Derivation** | Keyword-based engine → `product_category` column |
| 🔧 **Feature Engineering** | Binary flags: `is_best_seller`, `has_coupon`, `is_sponsored`, `is_sustainable` |
| 🔁 **Null Imputation** | Semantic fallbacks for string columns |

### Run Locally

```bash
git clone https://github.com/Aman739-code/E_G1_DVACapstone2
cd E_G1_DVACapstone2
pip install -r requirements.txt
python scripts/etl_pipeline.py
```

> Output: `data/processed/cleaned_data.csv`

---

## 📓 Notebooks

| # | Notebook | Purpose |
|---|----------|---------|
| 01 | `01_extraction.ipynb` | Initial data exploration |
| 02 | `02_cleaning.ipynb` | Cleaning prototype (automated in etl_pipeline.py) |
| 03 | `03_eda.ipynb` | Distributions, trends, correlations |
| 04 | `04_statistical_analysis.ipynb` | Statistical testing & significance |
| 05 | `05_final_load_prep.ipynb` | Final validation before Tableau load |

---

## 📊 Tableau Dashboard

🔗 **[Amazon Electronics Market Intelligence Dashboard](https://public.tableau.com/app/profile/aman.bhatnagar7387/viz/AmazonElectronicsMarketIntelligenceDashboard/Dashboard1)**

---

## 📚 Documentation

- [`docs/data_dictionary.md`](docs/data_dictionary.md) — Full schema & transformation rules
- [`reports/project_report.pdf`](reports/project_report.pdf) — Detailed findings

---


## 👥 Team Contribution Matrix

| Team Member | Primary Role | Deliverables |
| :--- | :--- | :--- |
| **Aman** | Project Lead, Visualisation Lead | Repo setup, timeline management, submission compliance, Gate 1, KPIs, Tableau dashboard |
| **Adnan Rizvi** | ETL Lead, Quality Lead | Engineered a production-grade ETL pipeline, restructured the repo |
| **Bhoomi Chhikara** | ETL Lead, Analysis Lead | Notebook 01 and 03 - Extraction and EDA |
| **Mouli Srivastava** | Analysis Lead, Report Lead | Notebook 04 - Statistical Analysis, Final Report PDF, contribution matrix |
| **Gauri Mishra** | Report Lead | Prepared the Report PDF |
| **Prashant Raj** | PPT Lead | Designed and structured the final presentation deck |
| **Swagato Bauri** | Documentation Lead | Documented the process in Readme.md, Notebook 05 - Final_load_prep |

<br>

<div align="center">

</div>

---

*DVA Capstone 2 — Group E_G1 | Data Visualization & Analytics*
