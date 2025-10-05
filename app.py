import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load dataset ---
df = pd.read_csv("your_dataset.csv")

# --- Define ethnicity columns ---
ethnic_columns = [
    'American Indian / Alaskan Native',
    'Asian',
    'Black or African American',
    'Hispanic',
    'Native Hawaiian or other Pacific Islander(not hispanic)',
    'Multi-Racial',
    'White'
]

st.title("🎓 School District Demographics Dashboard")
st.markdown("""
Explore the demographic breakdowns of gender and nationality across different school districts.
You can also see a focused view of students identified as **Gifted/Talented**.
""")

# --- Sidebar dropdown for district selection ---
districts = ["All"] + sorted(df['DISTRICT_NAME'].unique().tolist())
district = st.selectbox("Select a School District", districts)


# --- Filter data based on selection ---
if district == "All":
    district_data = df.copy()
else:
    district_data = df[df['DISTRICT_NAME'] == district]

# --- Shared gender colors for bar charts ---
gender_colors = {
    "Male": "#1f77b4",   # blue
    "Female": "#e377c2"  # pink
}

# --- 1️⃣ Bar Chart — All Students ---
gender_all = district_data.groupby("GIFTED_TALENTED")[["Male", "Female"]].sum().reset_index()
bar_all_data = gender_all.melt(
    id_vars=["GIFTED_TALENTED"],
    value_vars=["Male", "Female"],
    var_name="Gender",
    value_name="Count"
)
bar_all_fig = px.bar(
    bar_all_data,
    x="GIFTED_TALENTED",
    y="Count",
    color="Gender",
    color_discrete_map=gender_colors,
    barmode="group",
    title=f"Gifted Talented Distribution by Gender — All Students ({district})"
)

# --- 2️⃣ Bar Chart — Gifted Only (exclude 'N') ---
gifted_only = district_data[district_data["GIFTED_TALENTED"] != "N"]
if not gifted_only.empty:
    gender_gifted = gifted_only.groupby("GIFTED_TALENTED")[["Male", "Female"]].sum().reset_index()
    bar_gifted_data = gender_gifted.melt(
        id_vars=["GIFTED_TALENTED"],
        value_vars=["Male", "Female"],
        var_name="Gender",
        value_name="Count"
    )
    bar_gifted_fig = px.bar(
        bar_gifted_data,
        x="GIFTED_TALENTED",
        y="Count",
        color="Gender",
        color_discrete_map=gender_colors,
        barmode="group",
        title=f"Gifted Talented Distribution by Gender — Gifted Students Only ({district})"
    )
else:
    bar_gifted_fig = None

# --- Shared ethnicity colors for pie charts ---
ethnicity_colors = px.colors.qualitative.Set3

# --- 3️⃣ Pie Chart — All Students ---
ethnic_all = district_data[ethnic_columns].sum().reset_index()
ethnic_all.columns = ["Ethnicity", "Count"]
pie_all_fig = px.pie(
    ethnic_all,
    names="Ethnicity",
    values="Count",
    color="Ethnicity",
    color_discrete_sequence=ethnicity_colors,
    title=f"Ethnicity Breakdown — All Students ({district})"
)

# --- 4️⃣ Pie Chart — Gifted Only (exclude 'N') ---
ethnic_gifted = gifted_only[ethnic_columns].sum().reset_index()
ethnic_gifted.columns = ["Ethnicity", "Count"]
pie_gifted_fig = px.pie(
    ethnic_gifted,
    names="Ethnicity",
    values="Count",
    color="Ethnicity",
    color_discrete_sequence=ethnicity_colors,
    title=f"Ethnicity Breakdown — Gifted Students Only ({district})"
)

# --- Display all charts vertically ---
st.plotly_chart(bar_all_fig, use_container_width=True)

if bar_gifted_fig:
    st.plotly_chart(bar_gifted_fig, use_container_width=True)
else:
    st.warning("No gifted student data available for this district.")

st.plotly_chart(pie_all_fig, use_container_width=True)
st.plotly_chart(pie_gifted_fig, use_container_width=True)
