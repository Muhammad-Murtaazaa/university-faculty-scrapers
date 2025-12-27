import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = os.path.join("data", "aarhus_staff.csv")
OUTPUT_IMG = os.path.join("images", "aarhus_dashboard.png")

# Ensure images directory exists
os.makedirs("images", exist_ok=True)

def create_charts():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Please run the scraper first.")
        return

    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Aarhus University CS Dept - Staff Analysis', fontsize=20, weight='bold')

    # Chart 1: Gender
    gender_counts = df['Gender'].value_counts()
    axes[0, 0].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
    axes[0, 0].set_title('Gender Distribution')

    # Chart 2: Categories
    sns.countplot(x='Category', data=df, ax=axes[0, 1], palette='viridis')
    axes[0, 1].set_title('Staff Categories')
    axes[0, 1].tick_params(axis='x', rotation=15)

    # Chart 3: Jobs
    top_jobs = df['Job Title'].value_counts().nlargest(10).index
    sns.countplot(y='Job Title', data=df[df['Job Title'].isin(top_jobs)], ax=axes[1, 0], palette='magma', order=top_jobs)
    axes[1, 0].set_title('Top 10 Job Titles')

    # Chart 4: Buildings
    top_buildings = df['Building'].value_counts().nlargest(10).index
    sns.countplot(y='Building', data=df[df['Building'].isin(top_buildings)], ax=axes[1, 1], palette='coolwarm', order=top_buildings)
    axes[1, 1].set_title('Top 10 Buildings')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(OUTPUT_IMG)
    print(f"Charts saved to '{OUTPUT_IMG}'")

if __name__ == "__main__":
    create_charts()