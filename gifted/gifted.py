import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("your_dataset.csv")

# Define columns
ethnic_columns = [
    'American Indian / Alaskan Native', 
    'Asian', 
    'Black or African American', 
    'Hispanic', 
    'Native Hawaiian or other Pacific Islander(not hispanic)', 
    'Multi-Racial', 
    'White'
]

# App title and description
st.title("🎓 School District Gifted Student Dashboard")
st.markdown("""
Explore gender and ethnicity breakdowns across school districts.
Use the dropdowns below to switch between districts and compare *all students* versus *gifted students only*.
""")

# Dropdowns
districts = sorted(df['DISTRICT_NAME'].unique())
districts.insert(0, "All")  # add 'All' at the top
district_choice = st.selectbox("Select a School District:", districts)

view_choice = st.radio(
    "Select Data View:",
    ("All Students", "Gifted Students Only")
)

# Filter data based on user selection
if district_choice == "All":
    data = df.copy()
else:
    data = df[df['DISTRICT_NAME'] == district_choice]

# Apply view filter
if view_choice == "Gifted Students Only":
    data = data[data['GIFTED_TALENTED'] != 'N']

# ----- BAR CHART -----
bar_data = data.groupby('GIFTED_TALENTED')[['Male', 'Female']].sum().reset_index()

bar_fig = px.bar(
    bar_data,
    x='GIFTED_TALENTED',
    y=['Male', 'Female'],
    barmode='group',
    title=f"Gender Distribution - {view_choice} ({district_choice})",
    labels={'value': 'Count', 'variable': 'Gender', 'GIFTED_TALENTED': 'Gifted Category'},
    color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'}
)
bar_fig.update_traces(hovertemplate='%{x}<br>%{legendgroup}: %{y}')

st.plotly_chart(bar_fig, use_container_width=True)

# ----- PIE CHART -----
pie_data = data[ethnic_columns].sum().reset_index()
pie_data.columns = ['Ethnicity', 'Count']

pie_fig = px.pie(
    pie_data,
    names='Ethnicity',
    values='Count',
    title=f"Ethnicity Distribution - {view_choice} ({district_choice})",
    color_discrete_sequence=px.colors.qualitative.Plotly
)
pie_fig.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(pie_fig, use_container_width=True)
