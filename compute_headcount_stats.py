"""
compute_headcount_stats.py - Deep dive calculations into team volumes, agent ratios,
shift mix, handle times, and SLA compliance.
"""
import pandas as pd
import numpy as np

tickets = pd.read_csv("outputs/categorized_tickets.csv")
agents = pd.read_csv("Given/agents.csv")

# 1. Team headcount from agents.csv
agent_counts = agents.groupby('team').size().rename("agent_headcount")

# 2. Volumes by Assigned Team vs Resolving Team
assigned_vol = tickets.groupby('assigned_team').size().rename("assigned_volume")
resolving_vol = tickets.groupby('resolving_team').size().rename("resolving_volume")

# 3. Handle time (hours) by resolving team
handle_time_med = tickets.groupby('resolving_team')['handle_time_hours'].median().rename("median_handle_time_hrs")
handle_time_mean = tickets.groupby('resolving_team')['handle_time_hours'].mean().rename("mean_handle_time_hrs")

# 4. SLA breaches by resolving team
sla_breaches = tickets.groupby('resolving_team')['sla_breached'].sum().rename("sla_breaches_count")
sla_breach_rate = (tickets.groupby('resolving_team')['sla_breached'].mean() * 100).round(2).rename("sla_breach_rate_pct")

# Combine into team master profile
team_profile = pd.concat([
    agent_counts,
    assigned_vol,
    resolving_vol,
    handle_time_med,
    handle_time_mean,
    sla_breaches,
    sla_breach_rate
], axis=1).fillna(0)

team_profile['tickets_per_agent_assigned'] = (team_profile['assigned_volume'] / team_profile['agent_headcount']).round(1)
team_profile['tickets_per_agent_resolved'] = (team_profile['resolving_volume'] / team_profile['agent_headcount']).round(1)
team_profile['pct_of_total_resolved'] = ((team_profile['resolving_volume'] / len(tickets)) * 100).round(2)
team_profile['pct_of_total_assigned'] = ((team_profile['assigned_volume'] / len(tickets)) * 100).round(2)

print("=== TEAM HEADCOUNT & WORKLOAD SUMMARY ===")
print(team_profile[[
    'agent_headcount',
    'assigned_volume',
    'pct_of_total_assigned',
    'resolving_volume',
    'pct_of_total_resolved',
    'tickets_per_agent_resolved',
    'median_handle_time_hrs',
    'sla_breach_rate_pct'
]].sort_values('resolving_volume', ascending=False).to_string())

# Save to CSV for dashboard and reports
team_profile.to_csv("outputs/team_workload_summary.csv")
print("\nSaved outputs/team_workload_summary.csv")
