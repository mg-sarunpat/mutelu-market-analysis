import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_hype_analysis():
    # 1. Load Trends (The Thai Wide-Format CSV)
    # Ensure this file path matches your project structure
    trends_raw = pd.read_csv('data/raw/mutelu_master_trends.csv')
    
    # 2. Define the Bridge (Thai Trends -> English Lazada Categories)
    mapping = {
        'ท้าวเวสสุวรรณ': 'wessuwan',
        'พระแม่ลักษมี': 'lakshmi',
        'พระพิฆเนศ': 'ganesha',
        'พญานาค': 'naga',
        'สีเสื้อมงคล 2569': 'shirts',
        'เบอร์มงคล': 'numbers',
        'กำไลสายมู': 'bracelets'
    }

    # Rename and calculate average interest
    trends_renamed = trends_raw.rename(columns=mapping)
    mapped_cols = [col for col in mapping.values() if col in trends_renamed.columns]
    hype_scores = trends_renamed[mapped_cols].mean().reset_index()
    hype_scores.columns = ['category', 'search_interest']

    # 3. Load Lazada Clean Data & Aggregate
    lazada_df = pd.read_csv('data/processed/mutelu_market_clean.csv')
    sales_summary = lazada_df.groupby('category')['sold_count'].sum().reset_index()

    # 4. Merge Hype and Reality
    merged = pd.merge(sales_summary, hype_scores, on='category')

    # 5. Opportunity Score Calculation
    merged['opportunity_score'] = merged['search_interest'] / (merged['sold_count'] + 1)
    merged = merged.sort_values('opportunity_score', ascending=False)

    # 6. Optimized Visualization
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.set_context("notebook")
    
    # Tamed bubble sizes and added transparency (alpha)
    scatter = sns.scatterplot(
        data=merged, 
        x='search_interest', 
        y='sold_count', 
        size='opportunity_score', 
        hue='category', 
        sizes=(50, 800), 
        alpha=0.7
    )
    
    # Fix the Y-Axis to start at zero and give some headroom
    plt.ylim(0, merged['sold_count'].max() * 1.2)
    plt.xlim(0, 100)

    # Annotate points with a small offset for readability
    for i, row in merged.iterrows():
        plt.text(
            row.search_interest + 1.5, 
            row.sold_count, 
            row.category.upper(), 
            fontsize=9, 
            weight='bold', 
            va='center'
        )

    plt.title('2026 Mutelu Market Intelligence: Hype vs. Sales Reality', fontsize=14, weight='bold', pad=20)
    plt.xlabel('Google Search Interest (Thai Keywords)', fontsize=11)
    plt.ylabel('Total Units Sold (Lazada)', fontsize=11)
    
    # Move legend outside to the right
    plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    borderaxespad=0.,
    markerscale=0.6  # shrink legend bubbles only
)
    
    plt.tight_layout()
    
    # Save and Show
    plt.savefig('visuals/hype_vs_reality_optimized.png', dpi=300)
    print("\n✅ Optimized Chart saved to visuals/hype_vs_reality_optimized.png")
    print(merged[['category', 'opportunity_score']].to_string(index=False))
    plt.show()

if __name__ == "__main__":
    run_hype_analysis()