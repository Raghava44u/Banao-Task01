import os
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import enrich_tickets
from src.analysis import run_full_analysis

print("Loading raw data...")
raw = load_raw_data()
enriched = enrich_tickets(
    raw['tickets'],
    raw['agents'],
    raw['products'],
    raw['customers'],
    raw['orders']
)

print("Running full analysis and generating artifacts...")
categorized = run_full_analysis(enriched)
print("Analysis complete!")
print("Total categorized tickets:", len(categorized))
print("Category value counts:")
print(categorized['category'].value_counts())
print("\nResolving team value counts:")
print(categorized['resolving_team'].value_counts())
print("\nAssigned team value counts:")
print(categorized['assigned_team'].value_counts())
