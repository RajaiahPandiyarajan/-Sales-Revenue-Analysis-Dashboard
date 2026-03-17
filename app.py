import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload Excel or CSV", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Convert Date
    df['Date'] = pd.to_datetime(df['Date'])

    # Create Revenue Column
    df['Revenue'] = df['Quantity'] * df['Price']

    # Sidebar Filters
    st.sidebar.header("Filters")

    min_date = df['Date'].min()
    max_date = df['Date'].max()

    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

    category = st.sidebar.multiselect(
        "Select Category",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    # Apply Filters
    df_filtered = df[
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1])) &
        (df['Category'].isin(category))
    ]

    # KPIs
    total_sales = df_filtered['Quantity'].sum()
    total_revenue = df_filtered['Revenue'].sum()
    avg_order_value = df_filtered['Revenue'].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", int(total_sales))
    col2.metric("Total Revenue", f"₹ {total_revenue:,.2f}")
    col3.metric("Avg Order Value", f"₹ {avg_order_value:,.2f}")

    st.markdown("---")

    # Revenue Trend
    st.subheader("📈 Revenue Trend")

    revenue_trend = df_filtered.groupby('Date')['Revenue'].sum().reset_index()

    fig1, ax1 = plt.subplots()
    sns.lineplot(data=revenue_trend, x='Date', y='Revenue', ax=ax1)
    plt.xticks(rotation=45)

    st.pyplot(fig1)

    # Top Products
    st.subheader("🏆 Top Products")

    top_products = df_filtered.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(10)

    fig2, ax2 = plt.subplots()
    top_products.plot(kind='bar', ax=ax2)
    plt.xticks(rotation=45)

    st.pyplot(fig2)

    # Category Sales
    st.subheader("📊 Category Sales Distribution")

    category_sales = df_filtered.groupby('Category')['Revenue'].sum()

    fig3, ax3 = plt.subplots()
    category_sales.plot(kind='pie', autopct='%1.1f%%', ax=ax3)

    st.pyplot(fig3)

else:
    st.warning("Please upload a file to continue.")
