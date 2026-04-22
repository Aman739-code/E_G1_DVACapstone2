# Data Dictionary: Amazon Products Sales Data

This document provides a comprehensive overview of the attributes in the cleaned dataset (`data/processed/cleaned_data.csv`). It details the schema, describes the business meaning of each field, and outlines the ETL transformations applied to the raw data.

## Schema Definition

| Column Name | Data Type | Description | Cleaning & Transformation Rules |
| :--- | :--- | :--- | :--- |
| `title` | `string` | The full name/title of the product. | Kept as is. |
| `rating` | `float` | Average customer rating (e.g., out of 5 stars). | Extracted numerical value from strings; imputed missing with the median rating. |
| `number_of_reviews` | `int` | Total number of customer reviews. | Stripped commas; cast to integer; imputed missing values with `0`. |
| `bought_in_last_month` | `int` | Estimated number of purchases in the last 30 days. | Parsed `K+` formatting (e.g., "6K+" to `6000`); imputed missing values with `0`. |
| `listed_price` | `float` | The original listed price or MSRP. | Stripped `$` and commas; converted to float; imputed missing with `current_price`. |
| `current_price` | `float` | The actual checkout price after any discounts. | Stripped `$` and commas; imputed missing with `listed_price`; dropped outliers `< 0` and `> 50000`. |
| `is_best_seller` | `int (0/1)` | Binary flag indicating if the product is a "Best Seller". | Assigned `1` if textual label includes "Best Seller", else `0`. |
| `is_sponsored` | `int (0/1)` | Binary flag indicating if the listing is an advertisement. | Assigned `1` if textual label equals "Sponsored", else `0`. |
| `buy_box_availability` | `string` | Information on product availability (e.g., "Add to cart"). | Kept as is. |
| `delivery_details` | `string` | Textual details regarding delivery estimates. | Kept as is. |
| `image_url` | `string` | URL to the primary product image. | Kept as is. |
| `product_url` | `string` | URL to the Amazon product listing page. | Kept as is. |
| `collected_at` | `datetime` | The timestamp when the data was scraped. | Cast to proper `pd.to_datetime` format. |
| `has_coupon` | `int (0/1)` | Binary flag indicating if a coupon is available. | Derived from `is_couponed`: assigned `0` if "No Coupon", else `1`. |
| `is_sustainable` | `int (0/1)` | Binary flag for eco-friendly or sustainable badges. | Derived from `sustainability_badges`: `1` if present, else `0`. |

## Data Quality Notes

- **Price Imputation**: Missing `listed_price` values fallback to `current_price` and vice versa, assuming no discount if only one price is available.
- **Handling Outliers**: Rows with negative `current_price` or extreme values (>$50,000) are removed during the ETL process to ensure analytical integrity.
- **Categorical Flags**: Variables like `is_best_seller`, `is_sponsored`, `has_coupon`, and `is_sustainable` have been engineered into robust boolean (0/1) indicators for straightforward dashboarding and correlation analysis.
