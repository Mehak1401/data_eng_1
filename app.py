import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Data Warehouse Dashboard", layout="wide")

st.title("📊 Data Engineering Warehouse Dashboard")

# Function to load data
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect('warehouse.db')
        df = pd.read_sql("SELECT * FROM transactions", conn)
        conn.close()
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.warning("No data found. Please run the ETL pipeline first (python etl_pipeline.py).")
else:
    # Sidebar filters
    st.sidebar.header("Filters")
    categories = ['All'] + list(df['product_category'].unique())
    selected_category = st.sidebar.selectbox("Select Category", categories)
    
    if selected_category != 'All':
        df_filtered = df[df['product_category'] == selected_category]
    else:
        df_filtered = df

    # --- High Level Metrics ---
    col1, col2, col3 = st.columns(3)
    
    total_rows = len(df_filtered)
    total_revenue = df_filtered['total_with_tax'].sum()
    avg_order_value = df_filtered['total_with_tax'].mean()
    
    col1.metric("Total Transactions", f"{total_rows:,}")
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Avg Order Value", f"${avg_order_value:.2f}")
    
    st.markdown("---")
    
    # --- Visualizations ---
    c1, c2 = st.columns(2)
    
    # 1. Transaction Trends (Line Chart)
    # Group by Date
    df_filtered['date'] = df_filtered['timestamp'].dt.date
    daily_sales = df_filtered.groupby('date')['total_with_tax'].sum().reset_index()
    
    fig_line = px.line(daily_sales, x='date', y='total_with_tax', 
                       title='Daily Revenue Trend',
                       labels={'total_with_tax': 'Revenue ($)', 'date': 'Date'})
    c1.plotly_chart(fig_line, use_container_width=True)
    
    # 2. Sales by Product Category (Bar Chart)
    category_sales = df_filtered.groupby('product_category')['total_with_tax'].sum().reset_index()
    
    fig_bar = px.bar(category_sales, x='product_category', y='total_with_tax',
                     title='Revenue by Product Category',
                     labels={'total_with_tax': 'Revenue ($)', 'product_category': 'Category'},
                     color='product_category')
    c2.plotly_chart(fig_bar, use_container_width=True)
    
    # 3. Status Distribution (Pie Chart) - Optional Extra
    status_counts = df_filtered['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    fig_pie = px.pie(status_counts, values='count', names='status', title='Order Status Distribution')
    st.plotly_chart(fig_pie, use_container_width=True)

    # Raw Data View
    if st.checkbox("Show Raw Data"):
        st.dataframe(df_filtered.head(100))
