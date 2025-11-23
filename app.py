import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Sales Analysis — Live Demo", layout="wide")

@st.cache_data
def load_data():
    csv_path = "Sales_data(EDA Exported).csv"
    excel_path = "Regional Sales Dataset.xlsx"
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        try:
            sheets = pd.read_excel(excel_path, sheet_name=None)
            if isinstance(sheets, dict):
                if 'Sales Orders' in sheets:
                    df = sheets['Sales Orders']
                else:
                    df = list(sheets.values())[0]
        except Exception:
            st.error("Could not find data file. Ensure `Sales_data(EDA Exported).csv` or `Regional Sales Dataset.xlsx` is in the repo.")
            return pd.DataFrame()
    df.columns = df.columns.str.strip().str.lower()
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    return df

df = load_data()
if df.empty:
    st.stop()

st.title("Sales Data Analytics — Live Demo")

with st.sidebar:
    st.header("Filters")
    min_date = df['order_date'].min() if 'order_date' in df.columns else None
    max_date = df['order_date'].max() if 'order_date' in df.columns else None
    if min_date is not None and max_date is not None:
        date_range = st.date_input("Order date range", value=(min_date, max_date))
    else:
        date_range = None

    region_options = list(df['us_region'].dropna().unique()) if 'us_region' in df.columns else []
    regions = st.multiselect("US Region", options=region_options, default=region_options)

    product_options = list(df['product_name'].dropna().unique())[:200] if 'product_name' in df.columns else []
    product = st.multiselect("Product (top 200 listed)", options=product_options)

    channel_options = list(df['channel'].dropna().unique()) if 'channel' in df.columns else []
    channels = st.multiselect("Sales Channel", options=channel_options, default=channel_options)

    st.markdown("---")
    st.markdown("Built with Python, Streamlit, pandas, Plotly, Seaborn, MySQL (for pipelines), and Power BI for dashboards.")

df_f = df.copy()
if date_range and len(date_range) == 2 and 'order_date' in df_f.columns:
    start, end = date_range
    df_f = df_f[(df_f['order_date'] >= pd.to_datetime(start)) & (df_f['order_date'] <= pd.to_datetime(end))]
if regions:
    if 'us_region' in df_f.columns:
        df_f = df_f[df_f['us_region'].isin(regions)]
if product:
    if 'product_name' in df_f.columns:
        df_f = df_f[df_f['product_name'].isin(product)]
if channels:
    if 'channel' in df_f.columns:
        df_f = df_f[df_f['channel'].isin(channels)]

col1, col2, col3, col4 = st.columns(4)
total_revenue = df_f['revenue'].sum() if 'revenue' in df_f.columns else 0
total_profit = df_f['profit'].sum() if 'profit' in df_f.columns else 0
avg_margin = (df_f['profit_margin_pct'].mean() if 'profit_margin_pct' in df_f.columns else np.nan)
orders = df_f['order_number'].nunique() if 'order_number' in df_f.columns else len(df_f)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Profit Margin", f"{avg_margin:.2f}%" if not np.isnan(avg_margin) else "N/A")
col4.metric("# Orders", f"{orders:,}")

st.markdown("---")

st.subheader("Monthly Revenue Trend")
if 'order_date' in df_f.columns and 'revenue' in df_f.columns:
    df_f['order_month'] = df_f['order_date'].dt.to_period('M')
    monthly = df_f.groupby('order_month')['revenue'].sum().reset_index()
    monthly['order_month'] = monthly['order_month'].dt.to_timestamp()
    fig = px.line(monthly, x='order_month', y='revenue', markers=True, title='Revenue over Time')
    fig.update_layout(yaxis_title='Revenue (USD)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Order date or revenue column not available for monthly trend.")

st.subheader("Top Products by Revenue")
if 'product_name' in df_f.columns and 'revenue' in df_f.columns:
    top_prod = df_f.groupby('product_name')['revenue'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_prod, x='revenue', y='product_name', orientation='h', title='Top 10 Products by Revenue')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

st.subheader('Sales by State (Choropleth)')
if 'state' in df_f.columns and 'revenue' in df_f.columns:
    state_sales = df_f.groupby('state')['revenue'].sum().reset_index()
    state_sales['revenue_m'] = state_sales['revenue'] / 1e6
    try:
        fig3 = px.choropleth(state_sales, locations='state', locationmode='USA-states', color='revenue_m', scope='usa',
                             color_continuous_scale='Blues', labels={'revenue_m':'Sales (M USD)'} )
        fig3.update_layout(margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig3, use_container_width=True)
    except Exception:
        st.info('Choropleth failed (missing state codes or Plotly data).')
else:
    st.info('State or revenue columns not available for map.')

st.markdown('---')

st.subheader('Filtered Data Sample')
st.dataframe(df_f.head(100))

@st.cache_data
def convert_df_to_csv(dframe):
    return dframe.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(df_f)
st.download_button(label='Download filtered data as CSV', data=csv, file_name='sales_filtered.csv', mime='text/csv')

st.markdown('---')
st.caption('Repo: https://github.com/Abhirajgautam28/Sales-Analysis')
