import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# TITLE
st.title("📊 Global Superstore Sales Dashboard")
st.markdown("Interactive Business Analytics Dashboard")

# LOAD DATA
df = pd.read_csv("Global_Superstore2.csv", encoding='latin1')

# DATE CONVERSION
df['Order Date'] = pd.to_datetime(df['Order Date'])

# SIDEBAR FILTER
st.sidebar.header("Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# FILTER DATA
filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category))
]

# KPI SECTION
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

# SALES BY REGION
sales_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()

fig1 = px.bar(
    sales_region,
    x='Region',
    y='Sales',
    title='Sales by Region',
    color='Sales'
)

st.plotly_chart(fig1, use_container_width=True)

# PROFIT BY CATEGORY
profit_category = filtered_df.groupby('Category')['Profit'].sum().reset_index()

fig2 = px.pie(
    profit_category,
    names='Category',
    values='Profit',
    title='Profit by Category'
)

st.plotly_chart(fig2, use_container_width=True)

# DISCOUNT VS PROFIT
fig3 = px.scatter(
    filtered_df,
    x='Discount',
    y='Profit',
    color='Category',
    title='Discount vs Profit'
)

st.plotly_chart(fig3, use_container_width=True)

# MONTHLY SALES TREND
filtered_df['Month'] = filtered_df['Order Date'].dt.to_period('M').astype(str)

monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()

fig4 = px.line(
    monthly_sales,
    x='Month',
    y='Sales',
    title='Monthly Sales Trend'
)

st.plotly_chart(fig4, use_container_width=True)

# TOP PRODUCTS
top_products = (
    filtered_df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x='Sales',
    y='Product Name',
    orientation='h',
    title='Top 10 Best Selling Products'
)

st.plotly_chart(fig5, use_container_width=True)

# FOOTER
st.markdown("---")
st.markdown("Created by Monami Banerjee")