import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = os.path.join("data", "unipi_faculty_detailed.csv")
OUTPUT_IMG = os.path.join("images", "pisa_dashboard.png")

# Ensure images directory exists
os.makedirs("images", exist_ok=True)

def create_dashboard():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Please run the scraper first.")
        return

    # --- Data Cleaning ---
    if 'Category' in df.columns:
        df['Role'] = df['Category'].str.replace('Faculty - ', '').str.replace('Staff - ', '').str.replace(' - empty', '')
    else:
        df['Role'] = 'Unknown'

    # Extract Building Code from Room (e.g., "331 O" -> "O")
    df['Building'] = df['Room'].apply(lambda x: str(x).split()[-1] if len(str(x).split()) > 1 else 'Unknown')

    # --- Visualization ---
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    sns.set_style("whitegrid")
    
    fig.suptitle('University of Pisa - CS Dept Analysis', fontsize=20, weight='bold')

    # Chart 1: Gender Distribution
    if 'Gender' in df.columns:
        sns.countplot(x='Gender', data=df, palette='pastel', ax=axes[0, 0],
                      order=df['Gender'].value_counts().index)
        axes[0, 0].set_title('Gender Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('Count')

    # Chart 2: Role Comparison
    role_counts = df['Role'].value_counts()
    sns.barplot(x=role_counts.values, y=role_counts.index, palette='viridis', ax=axes[0, 1])
    axes[0, 1].set_title('Academic Role Distribution', fontsize=14, fontweight='bold')

    # Chart 3: Composition (Pie)
    axes[1, 0].pie(role_counts, labels=role_counts.index, autopct='%1.1f%%',
                   startangle=140, colors=sns.color_palette('pastel'))
    axes[1, 0].set_title('Faculty Composition Breakdown', fontsize=14, fontweight='bold')

    # Chart 4: Building Occupancy
    building_counts = df['Building'].value_counts()
    sns.barplot(x=building_counts.index, y=building_counts.values, palette='rocket', ax=axes[1, 1])
    axes[1, 1].set_title('Occupancy by Building', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Building Code')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(OUTPUT_IMG, dpi=300)
    print(f"Charts saved to '{OUTPUT_IMG}'")

if __name__ == "__main__":
    create_dashboard()