import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
#df = pd.read_csv("C:/Users/simmi/OneDrive/Desktop/5122-Streamlit/Superstore_Sales_utf8.csv", parse_dates=True)
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)     
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## My additions - Sima Dutta (sdutta7)")

# Main category selection
categories = df['Category'].unique()
st.write("TASK 1")
main_category = st.selectbox(
    "Please select your category",
    categories,
    index=None,
    placeholder="Select..",
)

# function to get the sub-category for a selected category
def get_subcategories(df, category):
    return df[df['Category'] == category]['Sub_Category'].unique()

# Subcategory multi-selection
st.write("TASK 2")
subcategories = get_subcategories(df, main_category)
selected_subcategories = st.multiselect(
    "Select subcategories:",
    options=subcategories,
    default=[]
)

st.write("You selected:", main_category)
st.write(f"Selected Subcategories: {', '.join(selected_subcategories)}")

#function to calculate metrics
def calculate_metrics(df):
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    return total_sales, total_profit, overall_profit_margin

# Filter data based on selections
filtered_df = df[(df['Category'] == main_category) & (df['Sub_Category'].isin(selected_subcategories))]

# Calculate overall average profit margin
overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100

# Group by Order_Date and Sub_Category, and sum the Sales
st.write("TASK 3")
if selected_subcategories:
    chart_data = filtered_df.pivot_table(index='Order_Date', columns='Sub_Category', values='Sales', aggfunc='sum')
    # Create line chart
    st.subheader("Monthly Sales Chart")
    st.line_chart(chart_data)
st.write("TASK 4&5")
if selected_subcategories:
    # Calculate and display metrics
        total_sales, total_profit, overall_profit_margin = calculate_metrics(filtered_df)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${total_sales:,.2f}")
        col2.metric("Total Profit", f"${total_profit:,.2f}")
        col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", 
                    f"{overall_profit_margin - overall_avg_profit_margin:.2f}%",
                     delta_color="normal")
