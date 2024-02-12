import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv('Financial Analytics data (1).csv')

st.title(':moneybag: Financial Analytics')
st.write('Financial analytics leverages advanced statistical models and data visualization tools to extract insights from financial data. This dashboard provides a concise and comprehensive overview of key financial metrics, empowering users to make informed decisions, manage risks, and optimize financial strategies for business success.')

# Sidebar 
st.sidebar.title("Filter")

# Size category filter
selected_size_categories = st.sidebar.multiselect("Select Size Categories", ["Small", "Medium", "Large"], default=["Small", "Medium", "Large"])

# Filter data based on user input
filtered_df = df.copy()

if "All" not in selected_size_categories:
    size_mapping = {"Small": 50000, "Medium": 100000, "Large": 600000}
    filtered_df = filtered_df[filtered_df["Mar Cap - Crore"].between(size_mapping[selected_size_categories[0]], size_mapping[selected_size_categories[-1]])]

# Correlation Analysis
st.header("Correlation Analysis")
correlation_matrix = filtered_df[["Mar Cap - Crore", "Sales Qtr - Crore"]].corr()
st.write('Measures the degree of association  between two or more variables.A positive value indicates variables move in the same direction, a negative value indicates variables move in opposite directions, and a value close to zero suggests a weak or no correlation.')
st.write(correlation_matrix)

# Data Visualization
st.header("Data Visualization")
fig_bar = px.bar(filtered_df, x="Name", y="Sales Qtr - Crore", title="Sales Quarter by Company")
st.plotly_chart(fig_bar)

# Descriptive Statistics
st.header("Descriptive Statistics")
st.write(filtered_df[["Mar Cap - Crore", "Sales Qtr - Crore"]].describe())

# Ranking Analysis
st.header("Ranking Analysis")
filtered_df["Mar Cap Rank"] = filtered_df["Mar Cap - Crore"].rank(ascending=False)
filtered_df["Sales Qtr Rank"] = filtered_df["Sales Qtr - Crore"].rank(ascending=False)
st.write(filtered_df[["Name", "Mar Cap Rank", "Sales Qtr Rank"]])

# Size Categories
size_df = pd.DataFrame()

for category in selected_size_categories:
    size_df[category] = filtered_df[filtered_df["Mar Cap - Crore"].between(size_mapping[selected_size_categories[0]], size_mapping[selected_size_categories[-1]])]["Sales Qtr - Crore"]

fig_size_categories = px.box(size_df, points="all", labels={"variable": "Size Category", "value": "Sales Qtr - Crore"},
                             title="Sales Distribution Across Size Categories")

# Regression Analysis
st.header("Regression")
fig_regression = px.scatter(filtered_df, x="Mar Cap - Crore", y="Sales Qtr - Crore", trendline="ols",
                            labels={"Mar Cap - Crore": "Market Cap (Crore)", "Sales Qtr - Crore": "Sales (Crore)"},
                            title="Regression Analysis")
st.write('Regression analysis is a statistical method that examines the relationship between a dependent variable and one or more independent variables. ')
st.plotly_chart(fig_regression)


