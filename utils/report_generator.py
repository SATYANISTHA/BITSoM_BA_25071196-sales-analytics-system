import os
from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report.
    
    Args:
        transactions: List of valid transaction dictionaries.
        enriched_transactions: List of transactions with API data.
        output_file: Path where the report will be saved.
    """
    print("Generating comprehensive sales report...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # --- 1. PREPARE CALCULATIONS ---
    
    # Basic Stats
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    total_txns = len(transactions)
    avg_order_value = total_revenue / total_txns if total_txns > 0 else 0
    
    # Date Range
    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
    
    # Region Stats
    regions = set(t['Region'] for t in transactions)
    region_data = []
    for r in regions:
        r_txns = [t for t in transactions if t['Region'] == r]
        r_sales = sum(t['Quantity'] * t['UnitPrice'] for t in r_txns)
        r_count = len(r_txns)
        r_pct = (r_sales / total_revenue * 100) if total_revenue > 0 else 0
        r_avg = r_sales / r_count if r_count > 0 else 0
        region_data.append((r, r_sales, r_pct, r_count, r_avg))
    
    # Sort regions by sales descending
    region_data.sort(key=lambda x: x[1], reverse=True)
    
    # Top 5 Products
    product_sales = {}
    for t in transactions:
        p = t['ProductName']
        s = t['Quantity'] * t['UnitPrice']
        product_sales[p] = product_sales.get(p, 0) + s
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Top 5 Customers
    customer_spent = {}
    for t in transactions:
        cid = t['CustomerID']
        customer_spent[cid] = customer_spent.get(cid, 0) + t['Quantity']*t['UnitPrice']
    top_customers = sorted(customer_spent.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Enrichment Stats
    total_enriched_input = len(enriched_transactions)
    successful_enrichment = sum(1 for t in enriched_transactions if t.get('API_Match', False))
    failed_products = set(t['ProductID'] for t in enriched_transactions if not t.get('API_Match', False))
    success_rate = (successful_enrichment / total_enriched_input * 100) if total_enriched_input > 0 else 0

    # Best Selling Day
    daily_sales = {}
    daily_txn_count = {}
    for t in transactions:
        d = t['Date']
        daily_sales[d] = daily_sales.get(d, 0) + (t['Quantity'] * t['UnitPrice'])
        daily_txn_count[d] = daily_txn_count.get(d, 0) + 1
    best_day = max(daily_sales.items(), key=lambda x: x[1]) if daily_sales else ("N/A", 0)

    # --- 2. WRITE TO FILE ---
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # SECTION 1: HEADER
        f.write("="*50 + "\n")
        f.write("              SALES ANALYTICS REPORT              \n")
        f.write("="*50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_txns}\n")
        f.write("\n")
        
        # SECTION 2: OVERALL SUMMARY
        f.write("-" * 50 + "\n")
        f.write("2. OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue       : ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions  : {total_txns}\n")
        f.write(f"Average Order Value : ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range          : {date_range}\n")
        f.write("\n")
        
        # SECTION 3: REGION-WISE PERFORMANCE
        f.write("-" * 65 + "\n")
        f.write("3. REGION-WISE PERFORMANCE\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Region':<15} | {'Sales (₹)':<15} | {'% Total':<10} | {'Txns':<5} | {'Avg Order':<10}\n")
        f.write("-" * 65 + "\n")
        for r, sales, pct, count, avg in region_data:
            f.write(f"{r:<15} | {sales:,.2f}      | {pct:5.2f}%    | {count:<5} | {avg:,.2f}\n")
        f.write("\n")

        # --- SECTION 4: TOP 5 PRODUCTS ---
        # Calculate quantity per product
        product_quantity = {}
        for t in transactions:
            p = t['ProductName']
            product_quantity[p] = product_quantity.get(p, 0) + t['Quantity']

        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]

        f.write("-" * 50 + "\n")
        f.write("4. TOP 5 BEST SELLING PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5} {'Product Name':<30} {'Quantity':<10} {'Revenue':<15}\n")
        f.write("-" * 50 + "\n")
        for idx, (prod, sales) in enumerate(top_products, 1):
            qty = product_quantity.get(prod, 0)
            f.write(f"{idx:<5} {prod:<30} {qty:<10} ₹{sales:,.2f}\n")
        f.write("\n")

        # --- SECTION 5: TOP 5 CUSTOMERS ---
        # Calculate total spent and order count per customer
        customer_orders = {}
        for t in transactions:
            cid = t['CustomerID']
            if cid not in customer_orders:
                customer_orders[cid] = {'total_spent': 0, 'order_count': 0}
            customer_orders[cid]['total_spent'] += t['Quantity']*t['UnitPrice']
            customer_orders[cid]['order_count'] += 1

        top_customers = sorted(customer_orders.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]

        f.write("-" * 50 + "\n")
        f.write("5. TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<15} {'Orders':<10}\n")
        f.write("-" * 50 + "\n")
        for idx, (cid, data) in enumerate(top_customers, 1):
            f.write(f"{idx:<5} {cid:<15} ₹{data['total_spent']:,.2f} {data['order_count']:<10}\n")
        f.write("\n")

        # --- SECTION 6: DAILY SALES TREND ---
        # Calculate unique customers per day
        daily_customers = {}
        for t in transactions:
            d = t['Date']
            cid = t['CustomerID']
            if d not in daily_customers:
                daily_customers[d] = set()
            daily_customers[d].add(cid)

        f.write("-"*50 + "\n")
        f.write("6. DAILY SALES TREND\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Date':<12} | {'Revenue':<12} | {'Transactions':<12} | {'Unique Customers':<15}\n")
        f.write("-"*50 + "\n")
        for d in sorted(daily_sales):
            f.write(f"{d:<12} | ₹{daily_sales[d]:<11,.2f} | {daily_txn_count[d]:<12} | {len(daily_customers[d]):<15}\n")
        f.write("\n")

        # --- SECTION 7: PRODUCT & SALES ANALYSIS INSIGHTS ---
        # Calculate average transaction value per region
        region_avg_txn_value = {}
        for r, sales, pct, count, avg in region_data:
            region_avg_txn_value[r] = avg

        f.write("-" * 50 + "\n")
        f.write("7. PRODUCT & SALES ANALYSIS INSIGHTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} (Revenue: ₹{best_day[1]:,.2f})\n")
        low_performers = [p for p, s in product_sales.items() if s < 5000]
        if low_performers:
            f.write(f"Low Performing Products (Revenue < ₹5k): {', '.join(low_performers)}\n")
        else:
            f.write("Low Performing Products: None found below threshold.\n")
        f.write("\n")
        f.write("Average Transaction Value per Region:\n")
        for r, avg_val in region_avg_txn_value.items():
            f.write(f"  {r:<10}: ₹{avg_val:,.2f}\n")
        f.write("\n")

        # SECTION 8: API ENRICHMENT SUMMARY
        f.write("-" * 50 + "\n")
        f.write("8. API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Products Processed : {total_enriched_input}\n")
        f.write(f"Successfully Enriched    : {successful_enrichment}\n")
        f.write(f"Enrichment Success Rate  : {success_rate:.2f}%\n")
        if failed_products:
            missing_list = list(failed_products)[:5]
            f.write(f"Products Not Found in API: {missing_list} ...\n")
        else:
            f.write("Products Not Found in API: None (All matched!)\n")
            
        f.write("="*50 + "\n")
        f.write("END OF REPORT\n")

    print(f"Report generated successfully at: {output_file}")
