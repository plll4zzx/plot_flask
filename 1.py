import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

# Adjust tasks to start from April 2025
tasks_updated = [
    ("Design dual-signal watermarking (RQ2)", "2025-04-01", "2025-06-30"),
    ("Implement & test RQ2 scheme", "2025-07-01", "2025-09-30"),
    ("Write & submit RQ2 paper", "2025-10-01", "2025-10-31"),
    ("Release RQ2 open-source code", "2025-11-01", "2025-11-30"),
    ("Design distortion-free watermarking (RQ3)", "2025-07-01", "2025-09-30"),
    ("Implement & evaluate RQ3 method", "2025-10-01", "2025-11-30"),
    ("Write & submit RQ3 paper", "2025-12-01", "2025-12-15"),
    ("Release RQ3 open-source code", "2025-12-16", "2025-12-31"),
]

# Convert to DataFrame
df_updated = pd.DataFrame(tasks_updated, columns=["Task", "Start", "End"])
df_updated["Start"] = pd.to_datetime(df_updated["Start"])
df_updated["End"] = pd.to_datetime(df_updated["End"])
df_updated["Duration"] = df_updated["End"] - df_updated["Start"]

# Create the updated Gantt chart
fig, ax = plt.subplots(figsize=(12, 6))
for i, task in df_updated.iterrows():
    ax.barh(i, task["Duration"].days, left=task["Start"], height=0.4, align='center')

# Set y-ticks and labels
ax.set_yticks(range(len(df_updated)))
ax.set_yticklabels(df_updated["Task"])

# Format x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)

ax.set_title("Gantt Chart: RQ2 & RQ3 Research Plan (Starting April 2025)")
ax.set_xlabel("Timeline")
ax.set_ylabel("Tasks")
plt.tight_layout()

plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.savefig("gantt_chart.pdf")