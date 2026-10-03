"""
analysis.py - Generates full dataset categorization, monthly breakdowns,
team-category matrices, charts, and headcount analytics.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.taxonomy import CATEGORIES, CATEGORY_TO_TEAM
from src.pipeline import get_model

def run_full_analysis(enriched_tickets_df, categorizer=None):
    """
    Run full dataset classification, generate CSV deliverables and visualizations.
    """
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("outputs/charts", exist_ok=True)
    
    df = enriched_tickets_df.copy()
    
    # 1. Load production model if not passed
    if categorizer is None:
        print("Loading production model from models/vireo_classifier.joblib...")
        categorizer = get_model()
        
    print(f"Categorizing full dataset of {len(df)} tickets...")
    preds_df = categorizer.predict_dataset(df)
    
    # Merge predictions into full dataset
    df['ai_category'] = preds_df['category']
    df['ai_subcategory'] = preds_df['subcategory']
    df['confidence'] = preds_df['confidence']
    df['second_best_category'] = preds_df['second_best_category']
    df['second_best_confidence'] = preds_df['second_best_confidence']
    df['margin'] = preds_df['margin']
    df['review_required'] = preds_df['review_required']
    df['classification_reason'] = preds_df['reason']
    df['classification_evidence'] = preds_df['evidence']
    df['date'] = df['created_dt'].dt.date.astype(str)
    df['month'] = df['created_dt'].dt.to_period('M').astype(str)
    
    # Standardize column naming for required deliverables
    categorized_export = df[[
        'ticket_id',
        'date',
        'month',
        'assigned_team',
        'resolving_team',
        'agent_id',
        'resolving_agent_name',
        'channel',
        'product_sku',
        'product_name',
        'category', # baseline bot tag
        'ai_category',
        'ai_subcategory',
        'confidence',
        'second_best_category',
        'second_best_confidence',
        'margin',
        'review_required',
        'classification_reason',
        'classification_evidence',
        'transfers_count',
        'first_response_time_min',
        'handle_time_hours',
        'sla_breached',
        'refund_amount_inr',
        'replacement_issued'
    ]].rename(columns={'category': 'baseline_category', 'ai_category': 'category'})
    
    categorized_export.to_csv("outputs/categorized_tickets.csv", index=False)
    print("Saved outputs/categorized_tickets.csv")
    
    # 2. Monthly Category Breakdown (outputs/monthly_category.csv)
    monthly_cat = categorized_export.groupby(['month', 'category']).size().reset_index(name='ticket_count')
    month_totals = categorized_export.groupby('month').size().reset_index(name='month_total')
    monthly_cat = monthly_cat.merge(month_totals, on='month')
    monthly_cat['percentage'] = round((monthly_cat['ticket_count'] / monthly_cat['month_total']) * 100, 2)
    monthly_cat = monthly_cat.sort_values(['month', 'ticket_count'], ascending=[True, False])
    monthly_cat[['month', 'category', 'ticket_count', 'percentage']].to_csv("outputs/monthly_category.csv", index=False)
    print("Saved outputs/monthly_category.csv")
    
    # 3. Monthly Team Breakdown (outputs/monthly_team.csv)
    # Using resolving_team as the primary operational measure of work done, and including assigned_team view
    monthly_team = categorized_export.groupby(['month', 'resolving_team']).size().reset_index(name='ticket_count')
    monthly_team = monthly_team.merge(month_totals, on='month')
    monthly_team['percentage'] = round((monthly_team['ticket_count'] / monthly_team['month_total']) * 100, 2)
    monthly_team = monthly_team.rename(columns={'resolving_team': 'team'})
    monthly_team = monthly_team.sort_values(['month', 'ticket_count'], ascending=[True, False])
    monthly_team[['month', 'team', 'ticket_count', 'percentage']].to_csv("outputs/monthly_team.csv", index=False)
    print("Saved outputs/monthly_team.csv")
    
    # 4. Team x Category Analysis (outputs/team_category_matrix.csv)
    team_cat_matrix = pd.crosstab(
        categorized_export['resolving_team'],
        categorized_export['category'],
        margins=True,
        margins_name="Total"
    )
    team_cat_matrix.to_csv("outputs/team_category_matrix.csv")
    print("Saved outputs/team_category_matrix.csv")
    
    # 5. Chart 1: Monthly Category Volume (outputs/charts/monthly_category_volume.png)
    plt.figure(figsize=(14, 8))
    # Filter to main reporting window 2025-01 onwards for clear visualization
    main_window = monthly_cat[monthly_cat['month'] >= '2025-01']
    pivot_cat = main_window.pivot(index='month', columns='category', values='ticket_count').fillna(0)
    
    # Plot top 6 categories and bundle rest as 'Other categories' for clarity
    top_categories = categorized_export['category'].value_counts().head(6).index.tolist()
    pivot_plot = pivot_cat[[c for c in top_categories if c in pivot_cat.columns]]
    
    palette = sns.color_palette("tab10", len(pivot_plot.columns))
    for i, col in enumerate(pivot_plot.columns):
        plt.plot(pivot_plot.index, pivot_plot[col], marker='o', linewidth=2.5, label=col, color=palette[i])
        
    plt.title("Vireo Audio: Monthly Support Ticket Volume by AI Category (2025 - 2026)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Month", fontsize=11, labelpad=10)
    plt.ylabel("Number of Tickets", fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title="Primary Category", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig("outputs/charts/monthly_category_volume.png", dpi=300)
    plt.close()
    print("Saved outputs/charts/monthly_category_volume.png")
    
    # 6. Chart 2: Monthly Team Volume (outputs/charts/monthly_team_volume.png)
    plt.figure(figsize=(14, 8))
    main_window_team = monthly_team[monthly_team['month'] >= '2025-01']
    pivot_team = main_window_team.pivot(index='month', columns='team', values='ticket_count').fillna(0)
    
    team_palette = sns.color_palette("Set2", len(pivot_team.columns))
    for i, col in enumerate(pivot_team.columns):
        plt.plot(pivot_team.index, pivot_team[col], marker='s', linewidth=2.5, label=col, color=team_palette[i])
        
    plt.title("Vireo Audio: Monthly Ticket Resolution Volume by Support Team (2025 - 2026)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Month", fontsize=11, labelpad=10)
    plt.ylabel("Tickets Resolved", fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title="Resolving Support Team", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig("outputs/charts/monthly_team_volume.png", dpi=300)
    plt.close()
    print("Saved outputs/charts/monthly_team_volume.png")
    
    # 7. Chart 3: Team x Category Heatmap (outputs/charts/team_category_heatmap.png)
    plt.figure(figsize=(12, 8))
    heatmap_data = pd.crosstab(
        categorized_export['resolving_team'],
        categorized_export['category']
    )
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', cbar=True)
    plt.title("Team × Category Workload Matrix (Actual Tickets Resolved)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("True AI Category", fontsize=11, labelpad=10)
    plt.ylabel("Resolving Support Team", fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("outputs/charts/team_category_heatmap.png", dpi=300)
    plt.close()
    print("Saved outputs/charts/team_category_heatmap.png")
    
    return categorized_export
