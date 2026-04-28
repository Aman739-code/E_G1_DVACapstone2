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
graph TD
    A[(Raw Data\namazon_products_sales_data_uncleaned.csv)] -->|Ingest| B(Data Cleaning & Imputation)
    B --> C[Feature Engineering & Categorization]
    C --> D[(Processed Data\ncleaned_data.csv)]
    D --> E(Exploratory Data Analysis)
    D --> F(Statistical Analysis)
    E --> G[Tableau Dashboard]
    F --> G
    G --> H((Final Delivery\nReport & Dashboard))

    style A fill:#ff9999,stroke:#333,stroke-width:2px
    style D fill:#99ccff,stroke:#333,stroke-width:2px
    style G fill:#ffcc99,stroke:#333,stroke-width:2px
    style H fill:#99ff99,stroke:#333,stroke-width:2px
```

---

## ⚙️ ETL Pipeline

All cleaning was performed via `scripts/etl_pipeline.py` (`AmazonDataCleaner` class).

### Full Cleaning Pipeline

```mermaid
flowchart TD
    A([📥 Raw Dataset\namazon_products_sales_data_uncleaned.csv]):::input --> B
    B[🔍 Data Quality Assessment\nNulls · Duplicates · Type mismatches · No category column]:::step --> C
    C[🩹 Missing Value Treatment\nNumeric: impute or drop · Categorical: semantic fallback]:::step --> D
    D[🗑️ Duplicate Removal\nUnique product entries retained only]:::step --> E
    E[🔢 Data Type Conversion\nPrice → float · Rating → float · Reviews → int]:::step --> F
    F[💰 Price Processing\nImpute listed & current price · Filter negatives & outliers above $50k]:::step --> G
    G[🔤 Text Standardisation\nTrim spaces · Unify casing · Remove special characters]:::step --> H
    H{{"⭐ Product Category Creation — CRITICAL STEP\nKeyword-based engine applied to raw data\n→ Adds standardised product_category column"}}:::critical --> I
    I[🔧 Feature Engineering\nis_best_seller · has_coupon · is_sponsored · is_sustainable]:::step --> J
    J[🔁 Null Imputation\nSemantic fallbacks for buy_box, delivery_details, product_url]:::step --> K
    K([✅ Cleaned Dataset Exported\ndata/processed/cleaned_data.csv]):::output

    classDef input    fill:#ffcccc,stroke:#cc4444,stroke-width:2px,color:#7a0000
    classDef step     fill:#ede9fe,stroke:#7c3aed,stroke-width:1px,color:#3b0764
    classDef critical fill:#ccfdf0,stroke:#0f6e56,stroke-width:2px,color:#04342c
    classDef output   fill:#cce5ff,stroke:#185fa5,stroke-width:2px,color:#042c53
```

### Why Each Step Matters

| Cleaning Step | Problem Statement Requirement |
|---|---|
| Missing value treatment | Accurate ratings & review counts |
| Duplicate removal | Reliable engagement metrics |
| Type conversion | Correct numeric comparisons |
| Price processing | Valid discount calculations |
| Text standardisation | Consistent category grouping |
| **Product category creation** | **Enables category-level analysis** |
| Feature engineering | Best seller & coupon segmentation |
| Null imputation | No gaps in downstream reporting |

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

## 👥 Team Contributors

| Role | Member(s) |
|------|-----------|
| 📊 Tableau Dashboard Design | Aman |
| 🔧 Data Cleaning & ETL Pipeline | Adnan |
| 📈 EDA, PPT & Project Report | Bhoomi, Gauri, Mouli, Swagato, Prashant |

---

*DVA Capstone 2 — Group E_G1 | Data Visualization & Analytics*
