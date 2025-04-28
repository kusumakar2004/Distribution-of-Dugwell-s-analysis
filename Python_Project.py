import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
path = "C:/Users/kusum/Downloads/mi_census5_13-14_Table1.10.csv"
df = pd.read_csv(path)

# Convert numeric columns
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='ignore')

# Basic info
print("Shape:", df.shape)
print(df.info())
print(df.head())

# Select relevant columns
problem_types = [
    'Salinity - No.', 'Dried up - No.', 'Destroyed beyond repair - No.',
    'Sea water intrusion  - No.', 'Industrial effluents - No.', 'Other reasons - No.'
]

# 1. Top 10 Districts by Salinity Issues (Hue by State)
top_salinity = df.groupby(["District", "State"])["Salinity - No."].sum().reset_index()
top_salinity = top_salinity.sort_values("Salinity - No.", ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=top_salinity, x="Salinity - No.", y="District", hue="State", dodge=False, palette="Reds")
plt.title("Top 10 Districts by Salinity-Affected Sources")
plt.tight_layout()
plt.show()

# 2. Stacked Total Problems by Type (bar chart - no hue needed)
total_by_type = df[problem_types].sum().sort_values()
plt.figure(figsize=(10, 6))
total_by_type.plot(kind='barh', color='skyblue')
plt.title("Total Reported Water Source Issues by Type")
plt.xlabel("Total Number")
plt.tight_layout()
plt.show()

# 3. Heatmap of Problems by District (Top 15 Districts)
top_districts = df['District'].value_counts().head(15).index
heatmap_data = df[df['District'].isin(top_districts)].groupby('District')[problem_types].sum()
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrBr')
plt.title("Water Source Issues (Top 15 Districts)")
plt.tight_layout()
plt.show()

# 4. Proportion of All Problem Types (Pie Chart)
plt.figure(figsize=(6, 6))
plt.pie(total_by_type.values, labels=total_by_type.index.str.replace(" - No.", ""), autopct='%1.1f%%', startangle=140)
plt.title("Proportion of Problem Types in Water Sources")
plt.tight_layout()
plt.show()

# 5. Industrial Effluent-Affected Sources (Hue by State)
indust_df = df.groupby(['District', 'State'])["Industrial effluents - No."].sum().reset_index()
top10_indust = indust_df.sort_values("Industrial effluents - No.", ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=top10_indust, x='Industrial effluents - No.', y='District', hue='State', dodge=False, palette="Blues")
plt.title("Top 10 Districts by Industrial Effluents Issues")
plt.tight_layout()
plt.show()

# 6. Dried-Up Sources per Village (Histogram + KDE)
plt.figure(figsize=(10, 6))
sns.histplot(df["Dried up - No."], bins=30, kde=True, color='orange')
plt.title("Distribution of Dried-Up Water Sources per Village")
plt.xlabel("No. of Dried-Up Sources")
plt.tight_layout()
plt.show()

# 7. Boxplot: Destroyed Sources Across Districts (Hue by State)
top_blocks = df['District'].value_counts().head(10).index
box_df = df[df['District'].isin(top_blocks)]
plt.figure(figsize=(12, 6))
sns.boxplot(data=box_df, x='District', y='Destroyed beyond repair - No.', hue='State', palette="coolwarm")
plt.title("Distribution of Destroyed Water Sources (Top 10 Districts)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 8. Correlation Heatmap (No hue, numerical)
plt.figure(figsize=(10, 6))
corr = df[problem_types].corr()
sns.heatmap(corr, annot=True, cmap='rocket', fmt='.2f')
plt.title("Correlation Among Water Source Issues")
plt.tight_layout()
plt.show()

# 9. Sea Water Intrusion Distribution (Hue not needed)
plt.figure(figsize=(10, 6))
sns.violinplot(y=df["Sea water intrusion  - No."], color='lightblue')
plt.title("Distribution of Sea Water Intrusion-Affected Sources")
plt.tight_layout()
plt.show()

# 10. 'Other Reasons' by District (Hue by State)
other_df = df.groupby(['District', 'State'])['Other reasons - No.'].sum().reset_index()
top10_other = other_df.sort_values('Other reasons - No.', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=top10_other, x='Other reasons - No.', y='District', hue='State', dodge=False, palette="Greens")
plt.title("Top 10 Districts by 'Other Reasons'")
plt.tight_layout()
plt.show()

# 11. Irrigation Project Availability (Hue-like Pie)
labels = ['Available', 'Not Available']
values = [
    df['Availability of Major/Medium Irrigation Projects  - No.'].sum(),
    df['Availability of Major/Medium Irrigation Projects  - PL'].sum()
]
plt.figure(figsize=(6, 6))
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=120, colors=["#72c2d1", "#ffb347"])
plt.title("Availability of Major/Medium Irrigation Projects")
plt.tight_layout()
plt.show()

# 12. Parallel Coordinates (Comparing Districts Across Problem Types)
from pandas.plotting import parallel_coordinates
viz_df = df[["District", "State"] + problem_types].dropna()
top_districts_pc = viz_df.groupby(["District", "State"]).sum().reset_index().head(10)
top_districts_pc["label"] = top_districts_pc["District"] + " (" + top_districts_pc["State"] + ")"
plt.figure(figsize=(12, 6))
parallel_coordinates(top_districts_pc.drop(columns=["District", "State"]), "label", colormap=plt.get_cmap("Set2"))
plt.title("Comparison of Water Issues Across Top 10 Districts")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
