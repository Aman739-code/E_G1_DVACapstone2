# Data Dictionary Template
Use this file to document every important field in your dataset. A strong data dictionary makes your cleaning decisions, KPI logic, and dashboard filters much easier to review.

## How To Use This File
1. Add one row for each column used in analysis or dashboarding.
2. Explain what the field means in plain language.
3. Mention any cleaning or standardization applied.
4. Flag nullable columns, derived fields, and known quality issues.

## Dataset Summary
| Item | Details |
|---|---|
| Dataset name | amazon_products_sales_data_uncleaned |
| Source | https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025?select=amazon_products_sales_data_uncleaned.csv |
| Raw file name | amazon_products_sales_data_uncleaned.csv |
| Last updated | _Fill in_ |
| Granularity | _e.g. one row per order / customer / transaction / day_ |

## Column Definitions
| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| product_id | string | Unique identifier for each Amazon product listing | B08N5WRWNW | EDA / KPI / Tableau | Check for duplicates; treat nulls as invalid rows |
| product_name | string | Full name/title of the product as listed on Amazon | "Apple AirPods Pro (2nd Gen)" | EDA / Tableau | Strip leading/trailing whitespace; handle special characters |
| category | string | Top-level product category on Amazon | Electronics | EDA / KPI / Tableau | Standardize casing; consolidate inconsistent labels (e.g. "electronic" vs "Electronics") |
| sub_category | string | More specific product classification within the main category | Headphones & Earbuds | EDA / Tableau | Nulls present for some listings; fill or flag as "Unknown" |
| discounted_price | float | Selling price of the product after any discount applied (in INR) | 18999.00 | EDA / KPI | Remove currency symbols (₹, $); cast to float; nulls → drop or impute |
| actual_price | float | Original listed price before discount (in INR) | 24900.00 | EDA / KPI | Same cleaning as discounted_price; must be >= discounted_price |
| discount_percentage | float | Percentage discount offered on the product | 23.7 | EDA / KPI / Tableau | Remove % symbol; cast to float; values outside 0–100 are outliers |
| rating | float | Average customer rating on a scale of 1.0 to 5.0 | 4.3 | EDA / KPI / Tableau | Some entries contain "|" or text — drop or flag; cast to float |
| rating_count | int | Total number of customer ratings received | 12450 | EDA / KPI | Remove commas (e.g. "12,450"); cast to int; nulls → 0 or drop |
| about_product | string | Bullet-point description of product features from the listing | "Active Noise Cancellation..." | EDA | May be very long or null; truncate for display; not used in KPIs |
| user_id | string | Anonymized identifier of the reviewer/user | AE4JNKIZMNZQP | EDA | May have multiple rows per user; check for nulls |
| user_name | string | Display name of the reviewer on Amazon | Ravi Kumar | EDA | Not used in KPIs; strip whitespace |
| review_id | string | Unique identifier for each customer review | R1BQRGFZOU9LYP | EDA | Check for duplicates at review level |
| review_title | string | Short headline summary of the customer review | "Worth every penny!" | EDA | May be null if no review title was submitted |
| review_content | string | Full text body of the customer review | "Battery life is excellent..." | EDA | Often contains HTML entities; decode before use; frequently null |
| img_link | string | URL to the product image on Amazon | https://m.media-amazon.com/... | Tableau | Validate URL format; nulls acceptable for dashboard |
| product_link | string | Direct URL to the Amazon product listing page | https://www.amazon.in/dp/... | Tableau | Validate URL format; nulls acceptable |

## Derived Columns
| Derived Column | Logic | Business Meaning |
|---|---|---|
| discount_amount | actual_price - discounted_price | Absolute savings in INR; useful for flagging high-value deals |
| discount_bucket | Binned discount_percentage: 0–10%, 11–30%, 31–50%, 50%+ | Groups products by deal depth for segmentation and filtering |
| is_highly_rated | rating >= 4.0 AND rating_count >= 100 | Flags products with statistically meaningful positive ratings |
| price_tier | Binned discounted_price: Budget / Mid-range / Premium / Luxury | Enables price-segment analysis across categories |
| reviews_per_rating | rating_count / number of reviews (if review data joined) | Proxy for review engagement rate |

## Data Quality Notes
- **Duplicate records:** The dataset may contain multiple rows per product if the same product has multiple reviews — confirm granularity before aggregating.
- **Mixed currency symbols:** Price columns (discounted_price, actual_price) contain ₹ or $ symbols and commas that must be stripped before numeric casting.
- **Inconsistent category labels:** Category and sub_category values have mixed casing and spelling variants (e.g., "Computers&Accessories" vs "Computers & Accessories") — standardization required.
- **Rating anomalies:** The rating column contains non-numeric entries (e.g., pipe characters "|") in some rows — these should be coerced to null and excluded from aggregations.
- **Sparse review content:** review_content and review_title are frequently null or contain placeholder text — do not use for completeness metrics.
- **Outlier prices:** Some rows have discounted_price > actual_price, which is logically invalid — flag and exclude from discount-related KPIs.
- **No explicit date column:** The dataset does not appear to contain a transaction or review date, limiting time-series analysis unless inferred from external metadata.
- **~42,000 rows total:** Dataset is moderately sized; no sampling required for EDA, but check for class imbalance across categories.