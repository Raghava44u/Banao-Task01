"""
utils.py - General helper functions for formatting, currency, and file paths.
"""
import os
import re

def format_inr(amount):
    """Format floating point numbers as Indian Rupee string."""
    if amount is None or pd.isna(amount):
        return "Rs 0"
    return f"Rs {amount:,.2f}"

def format_percentage(val, decimals=2):
    """Format float as percentage string."""
    if val is None or pd.isna(val):
        return "0.0%"
    return f"{val:.{decimals}f}%"

def clean_text_basic(text):
    """Basic whitespace and punctuation normalization."""
    if not text:
        return ""
    text = str(text)
    text = re.sub(r'[\r\n\t]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()
