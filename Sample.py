import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel file
file_path = "Book2_test.xlsx"
df = pd.read_excel(file_path)

# Reshape from wide to long format
df.columns = df.columns.astype(str)  # ensure column names are strings
df_long = df.melt(id_vars='Ethinicity', var_name='year', value_name='value')
df_long.columns = ['ethnicity', 'year', 'value']
df_long['year'] = df_long['year'].astype(str)

# Title
st.title("📊 Interactive Ethnicity Data by Year")

# Slicers
years = sorted(df_long['year'].unique())
ethnicities = sorted(df_long['ethnicity'].unique())

selected_years = st.multiselect("📅 Select Year(s)", years, default=years)
selected_ethnicities = st.multiselect("🧬 Select Ethnicity(s)", ethnicities, default=ethnicities)

# Filter data
filtered = df_long[(df_long['year'].isin(selected_years)) & (df_long['ethnicity'].isin(selected_ethnicities))]

# Interactive plot
if not filtered.empty:
    fig = px.bar(
        filtered,
        x="ethnicity",
        y="value",
        color="year",
        barmode="group",
        title="Ethnicity-wise Breakdown by Year",
        labels={"value": "Value", "ethnicity": "Ethnicity", "year": "Year"}
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

# Show data table
with st.expander("📄 Show Filtered Data"):
    st.dataframe(filtered)
