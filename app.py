import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Sales Analysis — Live Demo", layout="wide")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Sales Analysis — Live Demo", layout="wide")


@st.cache_data(ttl=3600)
def load_data():
    csv_path = "Sales_data(EDA Exported).csv"
    excel_path = "Regional Sales Dataset.xlsx"
    df = None
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
            return pd.DataFrame()

    df.columns = df.columns.str.strip().str.lower()
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    return df


def validate_columns(df):
    """Return dict stating which logical columns are present in dataframe."""
    cols = {c: c in df.columns for c in [
        'revenue', 'profit', 'profit_margin_pct', 'order_number', 'order_date',
        'product_name', 'us_region', 'state', 'channel', 'unit_price', 'quantity', 'customer_name'
    ]}
    return cols


@st.cache_data
def convert_df_to_csv(dframe):
    return dframe.to_csv(index=False).encode('utf-8')


with st.spinner("Loading data..."):
    df = load_data()

if df.empty:
    st.title("Warehouse Sales Analytics Dashboard")
    st.error("No data found. Place `Sales_data(EDA Exported).csv` or `Regional Sales Dataset.xlsx` in the repository root.")
    st.stop()

st.title("Sales Data Analytics — Live Demo")

cols_present = validate_columns(df)

with st.sidebar:
    st.header("Filters")
    if cols_present['order_date']:
        min_date = df['order_date'].min()
        max_date = df['order_date'].max()
        date_range = st.date_input("Order date range", value=(min_date, max_date))
    else:
        date_range = None

    region_options = list(df['us_region'].dropna().unique()) if cols_present['us_region'] else []
    regions = st.multiselect("US Region", options=region_options, default=region_options)

    product_options = list(df['product_name'].dropna().unique())[:200] if cols_present['product_name'] else []
    product = st.multiselect("Product (top 200)", options=product_options)

    channel_options = list(df['channel'].dropna().unique()) if cols_present['channel'] else []
    channels = st.multiselect("Sales Channel", options=channel_options, default=channel_options)

    st.markdown("---")
    st.markdown("Built with Python, Streamlit, pandas, Plotly, Seaborn; uses MySQL for ETL and Power BI for executive reports.")

df_f = df.copy()
try:
    if date_range and len(date_range) == 2 and cols_present['order_date']:
        start, end = date_range
        df_f = df_f[(df_f['order_date'] >= pd.to_datetime(start)) & (df_f['order_date'] <= pd.to_datetime(end))]
    if regions and cols_present['us_region']:
        df_f = df_f[df_f['us_region'].isin(regions)]
    if product and cols_present['product_name']:
        df_f = df_f[df_f['product_name'].isin(product)]
    if channels and cols_present['channel']:
        df_f = df_f[df_f['channel'].isin(channels)]
except Exception as e:
    st.error(f"Error applying filters: {e}")

def compute_metrics(d):
    total_revenue = d['revenue'].sum() if cols_present['revenue'] else 0
    total_profit = d['profit'].sum() if cols_present['profit'] else 0
    avg_margin = d['profit_margin_pct'].mean() if cols_present['profit_margin_pct'] else np.nan
    orders = d['order_number'].nunique() if cols_present['order_number'] else len(d)
    aov = (total_revenue / orders) if orders and cols_present['revenue'] else np.nan
    median_unit_price = d['unit_price'].median() if cols_present['unit_price'] else np.nan
    top_region = d.groupby('us_region')['revenue'].sum().idxmax() if cols_present['us_region'] and cols_present['revenue'] else None
    top_customer = d.groupby('customer_name')['revenue'].sum().idxmax() if cols_present['customer_name'] and cols_present['revenue'] else None
    orders_per_day = None
    if cols_present['order_date']:
        days = (d['order_date'].max() - d['order_date'].min()).days or 1
        orders_per_day = d['order_number'].nunique()/days if cols_present['order_number'] else len(d)/days
    return {
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'avg_margin': avg_margin,
        'orders': orders,
        'aov': aov,
        'median_unit_price': median_unit_price,
        'top_region': top_region,
        'top_customer': top_customer,
        'orders_per_day': orders_per_day,
    }

metrics = compute_metrics(df_f)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${metrics['total_revenue']:,.0f}")
k2.metric("Total Profit", f"${metrics['total_profit']:,.0f}")
k3.metric("Avg Profit Margin", f"{metrics['avg_margin']:.2f}%" if not np.isnan(metrics['avg_margin']) else "N/A")
k4.metric("# Orders", f"{metrics['orders']:,}")

with st.expander("More KPIs"):
    c1, c2, c3 = st.columns(3)
    c1.metric("AOV", f"${metrics['aov']:,.2f}" if not np.isnan(metrics['aov']) else "N/A")
    c2.metric("Median Unit Price", f"${metrics['median_unit_price']:,.2f}" if not np.isnan(metrics['median_unit_price']) else "N/A")
    c3.metric("Orders / day", f"{metrics['orders_per_day']:.1f}" if metrics['orders_per_day'] else "N/A")
    st.write(f"Top region: **{metrics['top_region']}** | Top customer: **{metrics['top_customer']}**")

st.markdown("---")

st.subheader("Monthly Revenue Trend")
if cols_present['order_date'] and cols_present['revenue']:
    try:
        df_f['order_month'] = df_f['order_date'].dt.to_period('M')
        monthly = df_f.groupby('order_month')['revenue'].sum().reset_index()
        monthly['order_month'] = monthly['order_month'].dt.to_timestamp()
        fig = px.line(monthly, x='order_month', y='revenue', markers=True, title='Revenue over Time')
        fig.update_layout(yaxis_title='Revenue (USD)')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not draw monthly revenue chart: {e}")
else:
    st.info("Order date or revenue column not available for monthly trend.")

st.subheader("Top Products by Revenue")
if cols_present['product_name'] and cols_present['revenue']:
    try:
        top_prod = df_f.groupby('product_name')['revenue'].sum().nlargest(10).reset_index()
        fig2 = px.bar(top_prod, x='revenue', y='product_name', orientation='h', title='Top 10 Products by Revenue')
        fig2.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not draw top products chart: {e}")

st.subheader('Sales by State (Choropleth)')
if cols_present['state'] and cols_present['revenue']:
    try:
        state_sales = df_f.groupby('state')['revenue'].sum().reset_index()
        state_sales['revenue_m'] = state_sales['revenue'] / 1e6
        fig3 = px.choropleth(state_sales, locations='state', locationmode='USA-states', color='revenue_m', scope='usa',
                             color_continuous_scale='Blues', labels={'revenue_m':'Sales (M USD)'} )
        fig3.update_layout(margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.info(f'Choropleth failed: {e}')
else:
    st.info('State or revenue columns not available for map.')

st.markdown('---')

st.subheader('Filtered Data Sample')
st.dataframe(df_f.head(100))

csv = convert_df_to_csv(df_f)
st.download_button(label='Download filtered data as CSV', data=csv, file_name='sales_filtered.csv', mime='text/csv')

st.markdown('---')
st.caption('Repo: https://github.com/Abhirajgautam28/Sales-Analysis')
