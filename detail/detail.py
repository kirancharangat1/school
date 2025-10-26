import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="PA Special Education Dashboard",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------
# Assuming you've already uploaded the data or have it locally
# Example: detail = pd.read_csv("Detail.csv")
# Replace this with your actual dataset path
@st.cache_data
def load_data():
    detail = pd.read_csv("Data - Detail.csv")
    return detail

detail = load_data()

# -------------------------------
# DATA PREP
# -------------------------------
# Keep rows that have at least one non-null gifted count
gifted_students = detail[detail[['GS', 'GX', 'GY']].notna().any(axis=1)].copy()

# Replace NaNs with 0 for easier aggregation
gifted_students[['GS', 'GX', 'GY']] = gifted_students[['GS', 'GX', 'GY']].fillna(0)

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

gifted_category = st.sidebar.radio(
    "Select Gifted Category:",
    options=["GS", "GX", "GY"],
    index=0,
    help="GS, GX, and GY represent different special education categories."
)

# Optional filters (can be expanded later)
gender_filter = st.sidebar.multiselect(
    "Select Gender(s):",
    options=gifted_students['STUDENT_GENDER_CD'].dropna().unique(),
    default=gifted_students['STUDENT_GENDER_CD'].dropna().unique()
)

grade_filter = st.sidebar.multiselect(
    "Select Grade(s):",
    options=sorted(gifted_students['CURR_GRADE_LVL'].dropna().unique()),
    default=sorted(gifted_students['CURR_GRADE_LVL'].dropna().unique())
)

# Apply filters
filtered_data = gifted_students[
    (gifted_students['STUDENT_GENDER_CD'].isin(gender_filter)) &
    (gifted_students['CURR_GRADE_LVL'].isin(grade_filter))
]

# -------------------------------
# AGGREGATION
# -------------------------------
agg_data = (
    filtered_data.groupby("ETHNIC_DESC", as_index=False)[gifted_category]
    .sum()
    .sort_values(by=gifted_category, ascending=False)
)

# -------------------------------
# PLOTLY BAR CHART
# -------------------------------
fig = px.bar(
    agg_data,
    x="ETHNIC_DESC",
    y=gifted_category,
    text=gifted_category,
    title=f"Total {gifted_category} Students by Ethnicity",
    labels={
        "ETHNIC_DESC": "Ethnicity",
        gifted_category: f"Total {gifted_category} Students"
    },
    color="ETHNIC_DESC",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
    plot_bgcolor="white",
    title_x=0.5
)

# -------------------------------
# MAIN DASHBOARD DISPLAY
# -------------------------------
st.title("🎓 PA School District Special Education Dashboard")
st.markdown("""
Explore total counts of special education students across Pennsylvania by ethnicity.
Use the sidebar to filter by category, gender, or grade.
""")

st.plotly_chart(fig, use_container_width=True)

st.dataframe(agg_data.rename(columns={gifted_category: f"Total {gifted_category} Students"}))

