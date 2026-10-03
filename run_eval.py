import os
import pandas as pd
from src.data_loader import load_raw_data
from src.preprocessing import enrich_tickets
from src.evaluation import run_evaluation

print("Loading raw data...")
raw_data = load_raw_data()
enriched_tickets = enrich_tickets(
    raw_data['tickets'],
    raw_data['agents'],
    raw_data['products'],
    raw_data['customers'],
    raw_data['orders']
)

print("Starting evaluation...")
categorizer, metrics = run_evaluation(enriched_tickets, sample_size=400, random_state=42)
print("Evaluation complete!")
print("AI Accuracy:", metrics['ai_model']['accuracy'])
print("Baseline Accuracy:", metrics['baseline_intake_bot']['accuracy'])
print("Macro F1:", metrics['ai_model']['macro_f1'])
