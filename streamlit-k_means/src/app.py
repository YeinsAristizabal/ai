import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data
def load_data():
    df = pd.read_csv("..\\data\\dataset-with-clustering.csv")  # Update with correct path
    
    # Handle missing values
    df.fillna(df.median(numeric_only=True), inplace=True)
    
    # Assign ordinal values to 'Education'
    education_mapping = {1:'Basic', 2:'Graduation', 3:'Master', 4:'PhD', 5:'2n Cycle'}
    df['Education'] = df['Education'].map(education_mapping)
    
    # Normalize 'Marital_Status'
    df['Marital_Status'] = df['Marital_Status'].map(df['Marital_Status'].value_counts(normalize=True))
    
    # Create new variables
    df['Total_Spending'] = df[['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum(axis=1)
    df['Total_Purchases'] = df[['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']].sum(axis=1)
    df['Total_Campaign_Response'] = df[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']].sum(axis=1)
    
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
income_range = st.sidebar.slider("Income Range", int(df["Income"].min()), int(df["Income"].max()), (30000, 100000))

Kidhome = df["Kidhome"].dropna().unique().tolist()
kidhome_filter = st.sidebar.multiselect("Kids at Home", Kidhome, default=Kidhome)

Teenhome = df["Teenhome"].dropna().unique().tolist()
teenhome_filter = st.sidebar.multiselect("Teens at Home", Teenhome, default=Teenhome)

Education = df["Education"].unique().tolist()
education_filter = st.sidebar.multiselect("Education Level", Education, default=Education)

# Apply Filters
df_filtered = df[(df["Income"] >= income_range[0]) & (df["Income"] <= income_range[1]) &
                 (df["Kidhome"].isin(kidhome_filter)) & (df["Teenhome"].isin(teenhome_filter))]

# Header
st.title("📊 Customer Segmentation Dashboard")
st.markdown("### Explore customer insights and segment behavior using machine learning analysis.")
st.markdown("---")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Avg. Income", f"${df_filtered['Income'].mean():,.2f}")
col2.metric("🛒 Avg. Spending", f"${df_filtered['Total_Spending'].mean():,.2f}")
col3.metric("📈 Total Customers", f"{len(df_filtered):,}")

st.markdown("---")

# Categorical Variable Analysis
st.subheader("📊 Categorical Variables by Cluster")
categorical_columns = ['Education', 'Complain', 'Response']
selected_categorical = st.selectbox("Select Categorical Variable", categorical_columns)

# Group by Cluster
df_grouped = df_filtered.groupby([selected_categorical, "Cluster"]).size().reset_index(name="Count")

# Bar Chart
fig_bar = px.bar(
    df_grouped,
    x=selected_categorical,
    y="Count",
    color="Cluster",
    barmode="group",  # by Category
    color_discrete_map={0: "blue", 1: "red"}  # Custom colors
)

st.plotly_chart(fig_bar, use_container_width=True)

# Numerical Variable Analysis
st.subheader("📉 Numerical Variable Distribution")
numerical_columns = ['Income', 'Kidhome', 'Teenhome', 'Recency', 'Total_Spending', 'Total_Purchases']
selected_numerical = st.selectbox("Select Numerical Variable", numerical_columns)
fig_hist = px.histogram(df_filtered, x=selected_numerical, color='Cluster', marginal="rug", barmode='overlay')
st.plotly_chart(fig_hist, use_container_width=True)

# Clustering Visualization
st.subheader("🔍 Cluster Visualization")
x_axis = st.selectbox("Select X-axis", numerical_columns, index=3)
y_axis = st.selectbox("Select Y-axis", numerical_columns, index=0)
fig_cluster = px.scatter(df_filtered, x=x_axis, y=y_axis, color='Cluster', color_continuous_scale='viridis')
st.plotly_chart(fig_cluster, use_container_width=True)


# Footer
st.text("")
st.text("")
st.text("")
st.markdown("---")

st.page_link('https://www.linkedin.com/in/yeins-aristizabal/', label="LinkeIn")
st.page_link('https://github.com/YeinsAristizabal/ai/tree/main/streamlit-dashboard-customer-segmentation', label="GitHub")
st.markdown("**Developed by Yeins Aristizabal**")