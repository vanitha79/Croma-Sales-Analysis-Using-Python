import pandas as pd


import matplotlib.pyplot as plt

import streamlit as st


st.set_page_config(page_title="Croma Electronics Sales Dashboard", layout="wide")
st.title("Croma Electronics Sales Analysis Dashboard")



df = pd.read_csv(r"E:\Dowloads\Croma_sales_analysis - Croma_analysis.csv")
Products = pd.read_csv(r"E:\Dowloads\Croma_Data - Product.csv")
Customers = pd.read_csv(r"E:\Dowloads\Croma_Data - Customer.csv")
Payments = pd.read_csv(r"E:\Dowloads\Croma_Data - Payment.csv")
df = df.drop(columns=["Column"])
df["Date"]=pd.to_datetime(df["Date"])

df = df.merge(Products, on="ProductID")
df = df.merge(Customers, on="CustomerID")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    category_filter = st.selectbox(
        "Select Category",
        ["All"] + sorted(df["Category"].unique().tolist())
    )

with filter_col2:
    state_filter = st.selectbox(
        "Select State",
        ["All"] + sorted(df["State"].unique().tolist())
    )

with filter_col3:
    brand_filter = st.selectbox(
        "Select Brand",
        ["All"] + sorted(df["Brand"].unique().tolist())
    )



filtered_df = df.copy()

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if state_filter != "All":
    filtered_df = filtered_df[filtered_df["State"] == state_filter]

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

total_sales = filtered_df["SalesAmount"].sum()
total_orders = filtered_df["OrderID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
average_order_value = total_sales / total_orders if total_orders > 0 else 0



col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Quantity", total_quantity)
col4.metric("Average Order Value", f"₹{average_order_value:,.0f}")




st.subheader("Sales Performance")

#<------Charts Layout------>

# Row 1
chart_col1, chart_col2 = st.columns(2)

#<------Bar Chart------->

with chart_col1:

    category_sales = filtered_df.groupby("Category")["SalesAmount"].sum()

    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.bar(category_sales.index, category_sales.values)

    ax.bar_label(bars, labels=[f"₹{value:,.0f}" for value in category_sales.values])
    ax.set_title("Sales by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Sales Amount")

    st.pyplot(fig, width=600)


#<------Line Chart------>

with chart_col2:

    date_sales = filtered_df.groupby("Date")["SalesAmount"].sum()

    x = date_sales.index.strftime("%d-%b")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.plot(x, date_sales.values, marker="o")

    ax.set_title("Sales over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sales Amount")

    for i, y in enumerate(date_sales.values):
        ax.text(i, y, f"₹{y:,.0f}", ha="center", va="bottom")

    ax.grid(True, alpha=0.3)

    st.pyplot(fig, width=600)


# Row 2
chart_col3, chart_col4 = st.columns(2)

#<------Pie Chart------>

with chart_col3:

    customer_sales = filtered_df.groupby("CustomerID")["SalesAmount"].sum()

    fig, ax = plt.subplots(figsize=(4, 3))

    ax.pie(
        customer_sales.values,
        labels=customer_sales.index,
        autopct="%1.1f%%",
        textprops={"fontsize": 6}
    )

    ax.set_title("Sales by Customer", fontsize=6)

    st.pyplot(fig, width=600)


#<------Scatter Chart------>

with chart_col4:

    quantity_sales = filtered_df[["Quantity", "SalesAmount"]]

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.scatter(
        quantity_sales["Quantity"],
        quantity_sales["SalesAmount"]
    )

    for x, y in zip(
        quantity_sales["Quantity"],
        quantity_sales["SalesAmount"]
    ):
        ax.text(
            x,
            y,
            f"₹{y:,.0f}",
            ha="left",
            va="bottom"
        )

    ax.grid(True, alpha=0.3)
    ax.set_title("Quantity vs Sales Amount")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Sales Amount")

    st.pyplot(fig, width=600)