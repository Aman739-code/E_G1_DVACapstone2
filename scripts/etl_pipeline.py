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

    # ─────────────────────────────────────────────────────────────────────────
    # CATEGORY DERIVATION — added to support category-level analysis
    # (discount, rating, review engagement per category)
    # ─────────────────────────────────────────────────────────────────────────

    # Ordered keyword rules for category classification.
    # WHY ordered dict? Priority matters — more specific categories must be
    # matched before broader catch-alls. E.g., "microphone" before "audio".
    # WHY keyword-based? The raw dataset has no category column; the product
    # title is the only structured text signal available per row.
    CATEGORY_RULES = {
        # Protection/warranty listings — caught first to avoid mis-classification
        # (e.g., "ASURION 2 Year Auto Accessories Plan" would match 'auto' otherwise)
        'Protection Plans': [
            'protection plan', 'asurion', 'warranty plan',
        ],
        # Highly specific audio input devices — before generic "audio" bucket
        'Microphones': [
            'microphone', 'lavalier mic', 'condenser mic', 'usb mic',
            'lapel mic', 'recording mic',
        ],
        'Headphones & Earbuds': [
            'earbuds', 'earphones', 'headphones', 'headset', 'airpods',
            'earpods', 'in-ear', 'over-ear', 'on-ear', 'true wireless',
        ],
        'Audio & Speakers': [
            'speaker', 'soundbar', 'subwoofer', 'bluetooth speaker',
            'turntable', 'amplifier', 'stereo', 'floorstanding',
        ],
        'Streaming & TV Devices': [
            'roku', 'fire stick', 'fire tv stick', 'chromecast',
            'streaming stick', 'streaming device', 'apple tv',
        ],
        'Smart Home & Security': [
            'smart plug', 'smart bulb', 'security camera', 'doorbell camera',
            'garage door', 'arlo', 'ring ', 'wyze', 'nest ',
        ],
        'Wearables': [
            'smartwatch', 'apple watch', 'fitbit', 'garmin watch',
            'fitness tracker', 'sport band', 'wearable',
        ],
        'Smartphones': [
            'iphone', 'android phone', 'pixel phone', 'galaxy s ',
            'unlocked smartphone',
        ],
        'Tablets': [
            'ipad', 'tablet', 'galaxy tab', 'fire hd', 'fire tablet',
            'android tablet',
        ],
        'Laptops & Computers': [
            'laptop', 'macbook', 'chromebook', 'notebook computer',
            'desktop computer', 'mac mini', 'mac pro', 'imac',
        ],
        'Gaming': [
            'gaming', 'playstation', 'xbox', 'nintendo', 'game controller',
            'joystick', 'gaming headset', 'gaming mouse', 'gaming keyboard',
            'wii ', 'game console',
        ],
        'Monitors & Displays': [
            'monitor', 'display ', 'projector', ' tv,', ' tv ', '4k tv',
            'qled', 'oled tv',
        ],
        'Cameras & Photography': [
            'camera', 'camera lens', 'tripod', 'dslr', 'mirrorless',
            'gopro', 'action camera', 'webcam', 'digital photo frame',
            'picture frame', '35mm film', 'camera strap',
        ],
        'Networking': [
            'router', 'wi-fi extender', 'wifi extender', 'wifi range extender',
            'network switch', 'modem', 'mesh network', 'access point',
        ],
        'Storage & Memory': [
            'ssd', 'hard drive', 'hdd', 'flash drive', 'sd card',
            'memory card', 'thumb drive', 'usb drive', 'nas ', 'nvme',
        ],
        'Printers & Ink': [
            'printer', 'ink cartridge', 'inkjet', 'toner cartridge', 'scanner',
            'laminating', 'laminator', 'print head',
        ],
        'Cables & Chargers': [
            'cable', 'charger', 'charging cable', 'usb-c', 'usb c to',
            'lightning cable', 'power bank', 'wall charger', 'hdmi cable',
        ],
        'Batteries': [
            'battery', 'batteries', 'alkaline', 'lithium battery',
            'rechargeable battery', 'aa battery', 'aaa battery', '9v battery',
        ],
        'Computer Accessories': [
            'keyboard', 'mouse ', 'laptop stand', 'monitor arm', 'hub ',
            'usb hub', 'docking station', 'ram ', 'ddr4', 'ddr5',
            'cpu cooler', 'cooling fan',
        ],
        'Phone Accessories': [
            'phone case', 'iphone case', 'samsung case', 'screen protector',
            'tempered glass', 'phone holder', 'car mount', 'airtag', 'air tag',
        ],
        'Office Supplies': [
            'printer paper', 'copy paper', 'pencil', 'ballpoint pen',
            'file folder', 'packing tape', 'laminating pouches',
            'sticky notes', 'calculator', 'whiteboard',
        ],
    }

    @staticmethod
    def extract_category(title: str) -> str:
        """
        Classify a product title into a subcategory using ordered keyword rules.

        WHY static method: Pure function — depends only on the title string,
        not on any instance state. Can be unit-tested in isolation and reused
        outside the class if needed (e.g., in a Spark UDF).

        Parameters
        ----------
        title : str
            Raw product title string.

        Returns
        -------
        str
            Category label. Returns 'Other Electronics' when no rule matches
            (deterministic fallback — never returns NaN or None).
        """
        if not isinstance(title, str) or title.strip() == '':
            # Guard against non-string or empty values; assign safe fallback
            return 'Other Electronics'

        title_lower = title.lower()

        for category, keywords in AmazonDataCleaner.CATEGORY_RULES.items():
            for kw in keywords:
                if kw in title_lower:
                    return category

        # Deterministic fallback — ensures zero nulls in output
        return 'Other Electronics'

    @staticmethod
    def clean_category(series: pd.Series) -> pd.Series:
        """
        Standardize category labels: strip whitespace and apply Title Case.

        WHY needed: Even though our rules produce consistent labels, this step
        future-proofs the pipeline — if categories are ever loaded from an
        external source or user input, inconsistent casing (e.g., 'batteries',
        'BATTERIES') would break groupby aggregations and Tableau filters.

        Parameters
        ----------
        series : pd.Series
            Series of raw category strings.

        Returns
        -------
        pd.Series
            Cleaned, Title-Cased category strings.
        """
        return series.str.strip().str.title()

    def assign_category(self):
        """
        Orchestrates the full category derivation step:
          1. Applies extract_category() to each product title.
          2. Cleans/standardizes the result via clean_category().
          3. Validates: logs distribution and asserts zero nulls.

        WHY placed after engineer_features(): The title column is untouched
        during feature engineering, so we can safely read it here. Placing
        category derivation before the outlier price filter means we don't
        lose category context for rows that will be filtered — the filter
        step runs after this method and operates on price only.

        Raises
        ------
        AssertionError
            If any null values are found in the resulting category column
            (should be impossible given the 'Other Electronics' fallback).
        """
        logging.info("Deriving 'product_category' from product titles...")

        # Step 1: Extract raw category label from title using keyword rules
        raw_categories = self.df['title'].apply(self.extract_category)

        # Step 2: Standardize casing and whitespace
        self.df['product_category'] = self.clean_category(raw_categories)

        # Step 3: Validate — null guard
        null_count = self.df['product_category'].isna().sum()
        assert null_count == 0, (
            f"Data quality failure: {null_count} null values found in "
            f"'product_category'. Check extract_category() fallback logic."
        )

        # Step 4: Log the category distribution for audit trail
        distribution = self.df['product_category'].value_counts()
        logging.info(
            f"'product_category' assigned successfully. "
            f"{self.df['product_category'].nunique()} unique categories. "
            f"Null count: {null_count}.\n{distribution.to_string()}"
        )

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

        # Category derivation: runs after feature engineering (title is intact)
        # and before outlier filtering (so category is present on all rows).
        self.assign_category()

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
