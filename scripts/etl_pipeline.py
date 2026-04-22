import pandas as pd
import numpy as np
import os
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AmazonDataCleaner:
    def __init__(self, raw_data_path: str, output_data_path: str):
        self.raw_data_path = raw_data_path
        self.output_data_path = output_data_path
        self.df = None

    def load_data(self):
        """Loads the raw dataset."""
        logging.info(f"Loading raw data from {self.raw_data_path}...")
        try:
            self.df = pd.read_csv(self.raw_data_path)
            logging.info(f"Loaded {self.df.shape[0]} rows and {self.df.shape[1]} columns.")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            raise

    def remove_duplicates(self):
        """Removes exact duplicate rows."""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        dropped_count = initial_count - len(self.df)
        logging.info(f"Removed {dropped_count} duplicate rows.")

    def clean_rating(self):
        """Extracts numerical rating from strings like '4.6 out of 5 stars'."""
        logging.info("Cleaning 'rating' column...")
        self.df['rating'] = self.df['rating'].astype(str).str.extract(r'^(\d+\.\d+)').astype(float)
        # Impute missing ratings with the median
        median_rating = self.df['rating'].median()
        self.df['rating'] = self.df['rating'].fillna(median_rating)

    def clean_reviews(self):
        """Removes commas and converts to integer. Imputes missing with 0."""
        logging.info("Cleaning 'number_of_reviews' column...")
        self.df['number_of_reviews'] = self.df['number_of_reviews'].astype(str).str.replace(',', '', regex=False)
        self.df['number_of_reviews'] = pd.to_numeric(self.df['number_of_reviews'], errors='coerce').fillna(0).astype(int)

    def clean_bought_last_month(self):
        """Parses '6K+ bought in past month' to integer 6000. Fills missing with 0."""
        logging.info("Cleaning 'bought_in_last_month' column...")
        
        def parse_bought(val):
            if pd.isna(val) or 'bought' not in str(val):
                return 0
            val_str = str(val).split('+')[0].strip()
            if 'K' in val_str:
                return int(float(val_str.replace('K', '')) * 1000)
            try:
                return int(val_str)
            except ValueError:
                return 0
                
        self.df['bought_in_last_month'] = self.df['bought_in_last_month'].apply(parse_bought)

    def clean_prices(self):
        """Cleans listed and current prices, handling '$' and 'No Discount' strings."""
        logging.info("Cleaning price columns...")
        
        # Clean listed_price
        self.df['listed_price'] = self.df['listed_price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
        self.df['listed_price'] = pd.to_numeric(self.df['listed_price'], errors='coerce')
        
        # Clean current/discounted_price
        self.df['current_price'] = self.df['current/discounted_price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
        self.df['current_price'] = pd.to_numeric(self.df['current_price'], errors='coerce')
        
        # Handle logic where listed price is missing but current price exists
        self.df['listed_price'] = self.df['listed_price'].fillna(self.df['current_price'])
        
        # Handle logic where current price is missing
        self.df['current_price'] = self.df['current_price'].fillna(self.df['listed_price'])
        
        # Drop the original awkwardly named column
        self.df = self.df.drop(columns=['current/discounted_price', 'price_on_variant'])

    def engineer_features(self):
        """Creates boolean flags and standardizes categoricals."""
        logging.info("Engineering boolean flags and standardizing formats...")
        
        # Boolean Flags
        self.df['is_best_seller'] = self.df['is_best_seller'].apply(lambda x: 1 if 'Best Seller' in str(x) else 0)
        self.df['is_sponsored'] = self.df['is_sponsored'].apply(lambda x: 1 if str(x).strip().lower() == 'sponsored' else 0)
        self.df['has_coupon'] = self.df['is_couponed'].apply(lambda x: 0 if 'No Coupon' in str(x) else 1)
        self.df['is_sustainable'] = self.df['sustainability_badges'].notna().astype(int)
        
        # Drop redundant columns
        self.df = self.df.drop(columns=['is_couponed', 'sustainability_badges'])
        
        # Datetime conversion
        self.df['collected_at'] = pd.to_datetime(self.df['collected_at'], errors='coerce')

    def run_pipeline(self):
        """Executes the full ETL cleaning pipeline."""
        logging.info("--- Starting ETL Pipeline ---")
        self.load_data()
        self.remove_duplicates()
        self.clean_rating()
        self.clean_reviews()
        self.clean_bought_last_month()
        self.clean_prices()
        self.engineer_features()
        
        # Outlier handling: dropping rows with price < 0 or abnormally high
        self.df = self.df[(self.df['current_price'] > 0) & (self.df['current_price'] < 50000)]
        
        self.save_data()
        logging.info("--- ETL Pipeline Completed Successfully ---")

    def save_data(self):
        """Saves the cleaned dataset."""
        os.makedirs(os.path.dirname(self.output_data_path), exist_ok=True)
        self.df.to_csv(self.output_data_path, index=False)
        logging.info(f"Cleaned data saved to {self.output_data_path}. Final shape: {self.df.shape}")


if __name__ == "__main__":
    # Define file paths
    RAW_DATA = "data/raw/amazon_products_sales_data_uncleaned.csv"
    CLEANED_DATA = "data/processed/cleaned_data.csv"
    
    # Run Pipeline
    cleaner = AmazonDataCleaner(RAW_DATA, CLEANED_DATA)
    cleaner.run_pipeline()
