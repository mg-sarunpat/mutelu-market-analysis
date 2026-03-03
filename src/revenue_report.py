import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_revenue_report():
    # 1. Load Data
    df = pd.read_csv('data/processed/mutelu_market_clean.csv')
    df['est_revenue'] = df['price'] * df['sold_count']
    
    # 2. Aggregate and Calculate % Market Share
    rev_stats = df.groupby('category')['est_revenue'].sum().sort_values(ascending=False).reset_index()
    total_market_rev = rev_stats['est_revenue'].sum()
    rev_stats['share_pct'] = (rev_stats['est_revenue'] / total_market_rev) * 100

    # 3. Calculate ARPL (Average Revenue Per Listing)
    arpl_stats = df.groupby('category').agg(
        total_rev=('est_revenue', 'sum'),
        item_count=('category', 'count')
    ).reset_index()
    
    arpl_stats['arpl'] = arpl_stats['total_rev'] / arpl_stats['item_count']
    arpl_stats = arpl_stats.sort_values('arpl', ascending=False)

    # 4. Console Output
    print("\n" + "="*60)
    print("💰 MUTELU MARKET REPORT 2026 💰")
    print("="*60)
    
    print("\n💎 MARKET EFFICIENCY (Average Revenue per Listing):")
    for _, row in arpl_stats.iterrows():
        print(f"{row['category'].upper():<12} | Avg Rev/Listing: ฿{row['arpl']:,.2f}")
    
    print(f"\n👑 Total Market Value Analyzed: ฿{total_market_rev:,.2f}")

    # 5. Visualization Setup (Subplots)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    sns.set_style("white")
    
    # --- Chart 1: Revenue Market Share ---
    colors_rev = sns.color_palette("RdYlGn_r", n_colors=len(rev_stats))
    sns.barplot(data=rev_stats, x='category', y='est_revenue', palette=colors_rev, ax=ax1)

    for i, p in enumerate(ax1.patches):
        # Fix: Using .iloc to match the sorted bar position
        rev_m = rev_stats['est_revenue'].iloc[i] / 1_000_000
        share = rev_stats['share_pct'].iloc[i]
        
        ax1.annotate(f"{rev_m:.1f}M\n({share:.1f}%)", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', 
                    xytext=(0, 8), 
                    textcoords='offset points',
                    fontsize=9, weight='bold', color='#333333')

    ax1.set_title('Total Revenue by Category', fontsize=14, pad=20, weight='bold')
    ax1.set_ylabel('Revenue (Thai Baht)', fontsize=11, labelpad=12)
    ax1.set_xlabel('Market Category', fontsize=11)
    ax1.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: f"{x/1e6:,.1f}M")
    )
    ax1.tick_params(axis='x', rotation=45)

    # --- Chart 2: ARPL Market Efficiency ---
    colors_arpl = sns.color_palette("YlOrRd", n_colors=len(arpl_stats))
    sns.barplot(data=arpl_stats, x='category', y='arpl', palette=colors_arpl, ax=ax2)

    for i, p in enumerate(ax2.patches):
        # Fix: Using .iloc ensures the value matches the bar position
        arpl_val = arpl_stats['arpl'].iloc[i]
        
        ax2.annotate(f"{arpl_val:,.0f}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', 
                    xytext=(0, 8), 
                    textcoords='offset points',
                    fontsize=9, weight='bold', color='#333333')

    ax2.set_title('Average Revenue per Listing (ARPL)', fontsize=14, pad=20, weight='bold')
    ax2.set_ylabel('Avg Revenue per Item (Thai Baht)', fontsize=11, labelpad=12)
    ax2.set_xlabel('Market Category', fontsize=11)
    ax2.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: f"{x:,.0f}")
    )
    ax2.tick_params(axis='x', rotation=45)

    # 6. Apply consistent styling
    sns.despine()
    
    plt.suptitle('2026 Mutelu Market Intelligence: Revenue vs. Efficiency', 
                 fontsize=16, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('visuals/revenue_executive_summary.png', dpi=300, bbox_inches='tight')
    print("\n✅ Chart saved to visuals/revenue_executive_summary.png")
    plt.show()

if __name__ == "__main__":
    run_revenue_report()