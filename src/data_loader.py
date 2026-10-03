"""
data_loader.py - Loads and verifies raw data files for Vireo Audio.
"""
import os
import pandas as pd

REQUIRED_FILES = {
    'tickets': 'tickets.csv',
    'agents': 'agents.csv',
    'customers': 'customers.csv',
    'orders': 'orders.csv',
    'products': 'products.csv',
    'support_policy': 'support-policy.pdf',
    'email_thread': 'email-thread.txt',
    'readme': 'README.txt'
}

def get_data_dir():
    """Return the absolute path to the Given directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    given_dir = os.path.join(base_dir, 'Given')
    return given_dir

def load_raw_data(data_dir=None):
    """
    Load all CSV raw data files from the Given directory without modifying them.
    Returns a dictionary of DataFrames.
    """
    if data_dir is None:
        data_dir = get_data_dir()
    
    datasets = {}
    for name in ['tickets', 'agents', 'customers', 'orders', 'products']:
        file_path = os.path.join(data_dir, REQUIRED_FILES[name])
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing required file: {file_path}")
        datasets[name] = pd.read_csv(file_path)
    
    return datasets
