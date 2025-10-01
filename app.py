import pandas as pd
import streamlit as st
import plotly.express as px

# --- Config ---
ethnic_columns = [
    'American Indian / Alaskan Native',
    'Asian',
    'Black or African American',
    'Hispanic',
    'Native Hawaiian or other Pacific Islander(not hispanic)',
    'Multi-Racial',
    'White'
]

@st.cache_data
def load_data():
    df = pd.read_csv("your_dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("School District Dashboard")

# Dropdown for district
districts = sorted(df["DISTRICT_NAME"].unique())
selected_district = st.selectbox("Select a District:", districts)

# Toggle for chart type
chart_type = st.radio("Choose Visualization:", ["Gifted/Talented by Gender", "Ethnicity Breakdown"])

if chart_type == "Gifted/Talented by Gender":
    df_long = df.melt(
        id_vars=["DISTRICT_NAME", "GIFTED_TALENTED"],
        value_vars=["Male", "Female"],
        var_name="Gender",
        value_name="Count"
    )
    filtered_df = df_long[df_long["DISTRICT_NAME"] == selected_district]

    fig = px.bar(
        filtered_df,
        x="GIFTED_TALENTED",
        y="Count",
        color="Gender",
        barmode="group",
        color_discrete_map={"Male": "blue", "Female": "red"}
    )
    fig.update_layout(
        title=f"Gifted/Talented by Gender - {selected_district}",
        xaxis_title="Gifted/Talented Status",
        yaxis_title="Student Count",
        legend_title="Gender"
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    filtered_df = df[df["DISTRICT_NAME"] == selected_district]
    ethnicity_counts = (
        filtered_df[ethnic_columns]
        .sum()
        .reset_index()
        .rename(columns={"index": "Ethnicity", 0: "Count"})
    )

    fig = px.pie(
        ethnicity_counts,
        names="Ethnicity",
        values="Count",
        hole=0.3
    )
    fig.update_traces(textinfo="percent+label", hovertemplate="%{label}: %{value} students")
    fig.update_layout(title=f"Ethnicity Breakdown - {selected_district}")
    st.plotly_chart(fig, use_container_width=True)
