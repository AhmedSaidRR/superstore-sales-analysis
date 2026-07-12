import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

def generate_dashboard_images():
   import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    db_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore.db')
    images_dir = os.path.join(BASE_DIR, 'dashboard', 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Establish database connection
    conn = sqlite3.connect(db_path)
    
    # Set plotting style
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    
    # ----------------------------------------------------
    # Plot 1: Monthly Sales & Profit Trend
    # ----------------------------------------------------
    df_monthly = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) as Month, 
               SUM(sales) as Sales, 
               SUM(profit) as Profit
        FROM orders
        GROUP BY Month
        ORDER BY Month
    """, conn)
    
    # We will only plot the last 24 months to keep it clean and readable
    df_monthly_recent = df_monthly.tail(24)
    
    plt.figure(figsize=(12, 6))
    
    # Plot Sales (Line + Area)
    plt.plot(df_monthly_recent['Month'], df_monthly_recent['Sales'], 
             color='#3B82F6', label='Sales ($)', linewidth=3, marker='o')
    plt.fill_between(df_monthly_recent['Month'], df_monthly_recent['Sales'], 
                     color='#3B82F6', alpha=0.1)
    
    # Plot Profit
    plt.plot(df_monthly_recent['Month'], df_monthly_recent['Profit'], 
             color='#10B981', label='Net Profit ($)', linewidth=2.5, marker='s')
    plt.fill_between(df_monthly_recent['Month'], df_monthly_recent['Profit'], 
                     color='#10B981', alpha=0.08)
    
    plt.title('Monthly Sales & Profit Performance Trend (Last 24 Months)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=11, labelpad=10)
    plt.ylabel('Amount ($)', fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=9)
    
    # Formatting values on Y-axis
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'sales_trend.png'), dpi=150)
    plt.close()
    print("Generated sales_trend.png")
    
    # ----------------------------------------------------
    # Plot 2: Sales & Profit by Category
    # ----------------------------------------------------
    df_category = pd.read_sql_query("""
        SELECT category as Category, 
               SUM(sales) as Sales, 
               SUM(profit) as Profit
        FROM orders
        GROUP BY Category
        ORDER BY Sales DESC
    """, conn)
    
    # Melt dataframe for easy seaborn plotting
    df_cat_melted = pd.melt(df_category, id_vars=['Category'], value_vars=['Sales', 'Profit'], 
                            var_name='Metric', value_name='Amount')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_cat_melted, x='Category', y='Amount', hue='Metric', 
                palette={'Sales': '#1E3A8A', 'Profit': '#10B981'}, edgecolor='#FFFFFF')
    
    plt.title('Sales & Net Profit by Product Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Product Category', fontsize=11, labelpad=10)
    plt.ylabel('Amount ($)', fontsize=11, labelpad=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=9)
    
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'category_performance.png'), dpi=150)
    plt.close()
    print("Generated category_performance.png")
    
    # ----------------------------------------------------
    # Plot 3: Regional Sales & Profit
    # ----------------------------------------------------
    df_region = pd.read_sql_query("""
        SELECT region as Region, 
               SUM(sales) as Sales, 
               SUM(profit) as Profit
        FROM orders
        GROUP BY Region
        ORDER BY Sales DESC
    """, conn)
    
    df_reg_melted = pd.melt(df_region, id_vars=['Region'], value_vars=['Sales', 'Profit'], 
                            var_name='Metric', value_name='Amount')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_reg_melted, y='Region', x='Amount', hue='Metric', 
                palette={'Sales': '#475569', 'Profit': '#34D399'}, edgecolor='#FFFFFF')
    
    plt.title('Territory Analysis: Sales & Net Profit by Region', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Geographic Region', fontsize=11, labelpad=10)
    plt.xlabel('Amount ($)', fontsize=11, labelpad=10)
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=10)
    
    ax = plt.gca()
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'regional_performance.png'), dpi=150)
    plt.close()
    print("Generated regional_performance.png")
    
    conn.close()
    print("All plots generated successfully!")

if __name__ == "__main__":
    generate_dashboard_images()
