import pandas as pd

def run_analysis():
    # 1. Load the clean data
    df = pd.read_csv('data/processed/mutelu_market_clean.csv')

    # 2. Calculate Estimated Revenue per item (Price * Sold Count)
    df['est_revenue'] = df['price'] * df['sold_count']

    print("\n" + "="*40)
    print("💰 MUTELU MARKET REPORT 2026 💰")
    print("="*40)

    # --- INSIGHT 1: The Top Categories ---
    print("\n🏆 Top Categories by Total Sales Volume (Items Sold):")
    sales_by_cat = df.groupby('category')['sold_count'].sum().sort_values(ascending=False)
    print(sales_by_cat.to_string())

    # --- INSIGHT 2: The "Premium" Factor ---
    print("\n💎 Average Price per Category (Premium vs Mass Market):")
    price_by_cat = df.groupby('category')['price'].mean().sort_values(ascending=False)
    # Format as Thai Baht
    print(price_by_cat.apply(lambda x: f"฿{x:,.2f}").to_string())

    # --- INSIGHT 3: The Money Makers ---
    print("\n👑 Top Categories by Estimated Revenue:")
    rev_by_cat = df.groupby('category')['est_revenue'].sum().sort_values(ascending=False)
    print(rev_by_cat.apply(lambda x: f"฿{x:,.2f}").to_string())

    # --- INSIGHT 4: The Real Efficiency Metric (ARPL) ---
    print("\n⚡ Market Efficiency: Average Revenue per Listing:")
    arpl = df.groupby('category').agg(
        total_revenue=('est_revenue', 'sum'),
        listing_count=('category', 'count')
    ).reset_index()
    arpl['avg_revenue_per_listing'] = arpl['total_revenue'] / arpl['listing_count']
    arpl = arpl.sort_values('avg_revenue_per_listing', ascending=False)
    # Format as Thai Baht
    arpl_display = arpl[['category', 'avg_revenue_per_listing']].copy()
    arpl_display['avg_revenue_per_listing'] = arpl_display['avg_revenue_per_listing'].apply(lambda x: f"฿{x:,.2f}")
    print(arpl_display.to_string(index=False))

    # --- INSIGHT 5: Where is the supply coming from? ---
    print("\n📍 Top 5 Seller Locations:")
    top_locations = df['location'].value_counts().head(5)
    print(top_locations.to_string())

if __name__ == "__main__":
    run_analysis()