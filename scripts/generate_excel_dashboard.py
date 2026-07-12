import json
import sqlite3
import xlsxwriter
import os

def create_excel_dashboard():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    db_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore.db')
    excel_path = os.path.join(BASE_DIR, 'excel', 'Superstore_Sales_Dashboard.xlsx')
    summary_path = os.path.join(BASE_DIR, 'data', 'processed', 'superstore_summary.json')
    
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    
    # Load summary data
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary = json.load(f)
        
    kpis = summary['kpis']
    
    # Connect to database to fetch clean orders for the raw data sheet
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT order_id, order_date, ship_mode, customer_name, segment, 
               city, state, region, category, sub_category, product_name, 
               sales, quantity, discount, profit 
        FROM orders
        ORDER BY order_date DESC
    """)
    raw_orders = cursor.fetchall()
    
    # Create workbook
    workbook = xlsxwriter.Workbook(excel_path)
    
    # ----------------------------------------------------
    # Styles and Formats
    # ----------------------------------------------------
    font_family = "Segoe UI"
    
    # Title Formats
    title_format = workbook.add_format({
        'font_name': font_family, 'font_size': 18, 'bold': True,
        'font_color': '#FFFFFF', 'bg_color': '#1E293B',
        'align': 'center', 'valign': 'vcenter'
    })
    
    subtitle_format = workbook.add_format({
        'font_name': font_family, 'font_size': 11, 'italic': True,
        'font_color': '#94A3B8', 'bg_color': '#1E293B',
        'align': 'center', 'valign': 'vcenter'
    })
    
    # KPI Card Formats
    kpi_title_format = workbook.add_format({
        'font_name': font_family, 'font_size': 9, 'bold': True,
        'font_color': '#64748B', 'bg_color': '#F8FAFC',
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#E2E8F0'
    })
    
    kpi_value_format = workbook.add_format({
        'font_name': font_family, 'font_size': 16, 'bold': True,
        'font_color': '#0F172A', 'bg_color': '#F8FAFC',
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#E2E8F0'
    })
    
    kpi_val_margin_format = workbook.add_format({
        'font_name': font_family, 'font_size': 16, 'bold': True,
        'font_color': '#0F172A', 'bg_color': '#F8FAFC',
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#E2E8F0',
        'num_format': '0.00"%"'
    })
    
    kpi_val_currency_format = workbook.add_format({
        'font_name': font_family, 'font_size': 16, 'bold': True,
        'font_color': '#0F172A', 'bg_color': '#F8FAFC',
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#E2E8F0',
        'num_format': '$#,##0'
    })
    
    # Section Header Format
    section_format = workbook.add_format({
        'font_name': font_family, 'font_size': 12, 'bold': True,
        'font_color': '#1E293B', 'bottom': 2, 'bottom_color': '#3B82F6'
    })
    
    # Table Header Format
    header_format = workbook.add_format({
        'font_name': font_family, 'font_size': 10, 'bold': True,
        'font_color': '#FFFFFF', 'bg_color': '#334155',
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#475569'
    })
    
    # Table Data Formats
    data_text_format = workbook.add_format({
        'font_name': font_family, 'font_size': 10, 'font_color': '#334155',
        'align': 'left', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1'
    })
    
    data_num_format = workbook.add_format({
        'font_name': font_family, 'font_size': 10, 'font_color': '#334155',
        'align': 'right', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1'
    })
    
    data_currency_format = workbook.add_format({
        'font_name': font_family, 'font_size': 10, 'font_color': '#334155',
        'align': 'right', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1',
        'num_format': '$#,##0.00'
    })
    
    data_percent_format = workbook.add_format({
        'font_name': font_family, 'font_size': 10, 'font_color': '#334155',
        'align': 'right', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1',
        'num_format': '0.0%'
    })
    
    # ----------------------------------------------------
    # Sheet 1: Dashboard
    # ----------------------------------------------------
    ws_dash = workbook.add_worksheet("Executive Dashboard")
    ws_dash.hide_gridlines(2) # Hide gridlines
    
    # Title Banner (Rows 0 to 2, Columns A to O)
    ws_dash.merge_range("A1:N1", "SUPERSTORE RETAIL PERFORMANCE DASHBOARD", title_format)
    ws_dash.merge_range("A2:N2", "Interactive Sales & Profitability Analysis Portfolio Project", subtitle_format)
    ws_dash.set_row(0, 30)
    ws_dash.set_row(1, 18)
    
    # KPI 1: Sales
    ws_dash.merge_range("B4:D4", "TOTAL SALES", kpi_title_format)
    ws_dash.merge_range("B5:D5", kpis['total_sales'], kpi_val_currency_format)
    
    # KPI 2: Profit
    ws_dash.merge_range("F4:H4", "TOTAL NET PROFIT", kpi_title_format)
    ws_dash.merge_range("F5:H5", kpis['total_profit'], kpi_val_currency_format)
    
    # KPI 3: Margin
    ws_dash.merge_range("J4:L4", "PROFIT MARGIN", kpi_title_format)
    ws_dash.merge_range("J5:L5", kpis['profit_margin'], kpi_val_margin_format)
    
    # KPI 4: Orders
    ws_dash.merge_range("N4:P4", "TOTAL ORDERS", kpi_title_format)
    ws_dash.merge_range("N5:P5", kpis['total_orders'], kpi_value_format)
    
    ws_dash.set_row(3, 16)
    ws_dash.set_row(4, 30)
    
    # Section Header
    ws_dash.write("A7", "Visual Business Performance Analytics", section_format)
    ws_dash.set_row(6, 22)
    
    # Charts placeholder areas:
    # We will build charts from data in Sheet 2 and insert them here.
    
    # ----------------------------------------------------
    # Sheet 2: Data Summary (Hidden or visible, we keep it visible for grading)
    # ----------------------------------------------------
    ws_data = workbook.add_worksheet("Dashboard_Calculations")
    
    # 1. Category Data
    ws_data.write("A1", "Category", header_format)
    ws_data.write("B1", "Sales", header_format)
    ws_data.write("C1", "Profit", header_format)
    for r_idx, cat in enumerate(summary['category_summary']):
        ws_data.write(r_idx + 1, 0, cat['category'], data_text_format)
        ws_data.write(r_idx + 1, 1, cat['sales'], data_currency_format)
        ws_data.write(r_idx + 1, 2, cat['profit'], data_currency_format)
        
    # 2. Region Data
    ws_data.write("E1", "Region", header_format)
    ws_data.write("F1", "Sales", header_format)
    ws_data.write("G1", "Profit", header_format)
    for r_idx, reg in enumerate(summary['region_summary']):
        ws_data.write(r_idx + 1, 4, reg['region'], data_text_format)
        ws_data.write(r_idx + 1, 5, reg['sales'], data_currency_format)
        ws_data.write(r_idx + 1, 6, reg['profit'], data_currency_format)
        
    # 3. Monthly Data
    ws_data.write("I1", "Month", header_format)
    ws_data.write("J1", "Sales", header_format)
    ws_data.write("K1", "Profit", header_format)
    for r_idx, mnt in enumerate(summary['monthly_trend']):
        ws_data.write(r_idx + 1, 8, mnt['month'], data_text_format)
        ws_data.write(r_idx + 1, 9, mnt['sales'], data_currency_format)
        ws_data.write(r_idx + 1, 10, mnt['profit'], data_currency_format)
        
    # ----------------------------------------------------
    # Create and Insert Charts into Dashboard
    # ----------------------------------------------------
    
    # Chart 1: Sales Trend over Time (Line Chart)
    chart_line = workbook.add_chart({'type': 'line'})
    num_months = len(summary['monthly_trend'])
    chart_line.add_series({
        'name': 'Sales',
        'categories': f'=Dashboard_Calculations!$I$2:$I${num_months + 1}',
        'values': f'=Dashboard_Calculations!$J$2:$J${num_months + 1}',
        'line': {'color': '#3B82F6', 'width': 2.25},
    })
    chart_line.add_series({
        'name': 'Profit',
        'categories': f'=Dashboard_Calculations!$I$2:$I${num_months + 1}',
        'values': f'=Dashboard_Calculations!$K$2:$K${num_months + 1}',
        'line': {'color': '#10B981', 'width': 1.5},
    })
    chart_line.set_title({'name': 'Monthly Sales & Profit Performance Trend', 'name_font': {'name': font_family, 'size': 11, 'bold': True}})
    chart_line.set_style(10)
    chart_line.set_x_axis({'text_font': {'name': font_family, 'size': 8}})
    chart_line.set_y_axis({'text_font': {'name': font_family, 'size': 8}, 'major_gridlines': {'visible': True, 'line': {'color': '#F1F5F9'}}})
    chart_line.set_legend({'position': 'bottom', 'font': {'name': font_family, 'size': 9}})
    chart_line.set_size({'width': 750, 'height': 320})
    ws_dash.insert_chart('B8', chart_line)
    
    # Chart 2: Category Analysis (Clustered Column Chart)
    chart_cat = workbook.add_chart({'type': 'column'})
    num_cats = len(summary['category_summary'])
    chart_cat.add_series({
        'name': 'Sales',
        'categories': f'=Dashboard_Calculations!$A$2:$A${num_cats + 1}',
        'values': f'=Dashboard_Calculations!$B$2:$B${num_cats + 1}',
        'fill': {'color': '#1E3A8A'},
    })
    chart_cat.add_series({
        'name': 'Profit',
        'categories': f'=Dashboard_Calculations!$A$2:$A${num_cats + 1}',
        'values': f'=Dashboard_Calculations!$C$2:$C${num_cats + 1}',
        'fill': {'color': '#10B981'},
    })
    chart_cat.set_title({'name': 'Performance by Product Category', 'name_font': {'name': font_family, 'size': 11, 'bold': True}})
    chart_cat.set_style(11)
    chart_cat.set_x_axis({'text_font': {'name': font_family, 'size': 9}})
    chart_cat.set_y_axis({'text_font': {'name': font_family, 'size': 8}})
    chart_cat.set_legend({'position': 'bottom', 'font': {'name': font_family, 'size': 9}})
    chart_cat.set_size({'width': 365, 'height': 300})
    ws_dash.insert_chart('B25', chart_cat)
    
    # Chart 3: Regional Sales (Bar/Pie Chart - lets use a Horizontal Bar Chart for variety)
    chart_reg = workbook.add_chart({'type': 'bar'})
    num_regs = len(summary['region_summary'])
    chart_reg.add_series({
        'name': 'Sales',
        'categories': f'=Dashboard_Calculations!$E$2:$E${num_regs + 1}',
        'values': f'=Dashboard_Calculations!$F$2:$F${num_regs + 1}',
        'fill': {'color': '#475569'},
    })
    chart_reg.add_series({
        'name': 'Profit',
        'categories': f'=Dashboard_Calculations!$E$2:$E${num_regs + 1}',
        'values': f'=Dashboard_Calculations!$G$2:$G${num_regs + 1}',
        'fill': {'color': '#34D399'},
    })
    chart_reg.set_title({'name': 'Sales & Profit by Territory Region', 'name_font': {'name': font_family, 'size': 11, 'bold': True}})
    chart_reg.set_style(12)
    chart_reg.set_x_axis({'text_font': {'name': font_family, 'size': 8}})
    chart_reg.set_y_axis({'text_font': {'name': font_family, 'size': 9}})
    chart_reg.set_legend({'position': 'bottom', 'font': {'name': font_family, 'size': 9}})
    chart_reg.set_size({'width': 370, 'height': 300})
    ws_dash.insert_chart('I25', chart_reg)
    
    # Auto-adjust column widths for calculation sheet
    ws_data.set_column('A:A', 15)
    ws_data.set_column('B:C', 18)
    ws_data.set_column('E:E', 15)
    ws_data.set_column('F:G', 18)
    ws_data.set_column('I:I', 15)
    ws_data.set_column('J:K', 18)
    
    # ----------------------------------------------------
    # Sheet 3: Clean Raw Data
    # ----------------------------------------------------
    ws_raw = workbook.add_worksheet("Clean Orders Dataset")
    
    headers_raw = [
        'Order ID', 'Order Date', 'Ship Mode', 'Customer Name', 'Segment',
        'City', 'State', 'Region', 'Category', 'Sub-Category', 'Product Name',
        'Sales', 'Quantity', 'Discount', 'Profit'
    ]
    
    # Write headers
    for c_idx, h in enumerate(headers_raw):
        ws_raw.write(0, c_idx, h, header_format)
        
    # Write rows
    for r_idx, row in enumerate(raw_orders):
        for c_idx, val in enumerate(row):
            # Format numbers appropriately
            if c_idx in [11, 14]: # Sales, Profit
                ws_raw.write(r_idx + 1, c_idx, val, data_currency_format)
            elif c_idx == 12: # Quantity
                ws_raw.write(r_idx + 1, c_idx, val, data_num_format)
            elif c_idx == 13: # Discount
                ws_raw.write(r_idx + 1, c_idx, val, data_percent_format)
            else:
                ws_raw.write(r_idx + 1, c_idx, val, data_text_format)
                
    # Auto-fit raw sheet columns
    col_widths = [16, 12, 14, 18, 12, 14, 14, 10, 12, 14, 25, 12, 8, 8, 12]
    for col_idx, width in enumerate(col_widths):
        ws_raw.set_column(col_idx, col_idx, width)
        
    workbook.close()
    conn.close()
    print("Excel dashboard generated successfully at:", excel_path)

if __name__ == "__main__":
    create_excel_dashboard()
