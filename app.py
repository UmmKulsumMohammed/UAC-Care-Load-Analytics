import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="UAC Care Load Analytics",
    layout="wide"
)

# -------------------
# LOAD DATA
# -------------------

df = pd.read_csv("processed_uac_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -------------------
# SIDEBAR
# -------------------

st.sidebar.title("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date))
    &
    (df["Date"] <= pd.to_datetime(end_date))
]

# -------------------
# TITLE
# -------------------

st.title(
    "System Capacity & Care Load Analytics for Unaccompanied Children"
)

st.markdown(
"""
Monitoring CBP and HHS care system load,
capacity stress, intake pressure and backlog trends.
"""
)

# -------------------
# KPI CARDS
# -------------------

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Avg System Load",
        round(
            filtered_df["Total_System_Load"].mean(),
            2
        )
    )

with col2:
    st.metric(
        "Avg Net Intake",
        round(
            filtered_df["Net_Intake_Pressure"].mean(),
            2
        )
    )

with col3:
    st.metric(
        "Growth Rate %",
        round(
            filtered_df["Care_Load_Growth_Rate"].mean(),
            2
        )
    )

with col4:
    st.metric(
        "Discharge Offset Ratio",
        round(
            filtered_df["Discharge_Offset_Ratio"].mean(),
            2
        )
    )

# -------------------
# TOTAL SYSTEM LOAD
# -------------------

st.subheader(
    "Total System Load Over Time"
)

fig = px.line(
    filtered_df,
    x="Date",
    y="Total_System_Load"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# CBP VS HHS
# -------------------

st.subheader(
    "CBP vs HHS Care Load"
)

fig = px.line(
    filtered_df,
    x="Date",
    y=[
        "Children in CBP custody",
        "Children in HHS Care"
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# NET INTAKE PRESSURE
# -------------------

st.subheader(
    "Net Intake Pressure"
)

fig = px.line(
    filtered_df,
    x="Date",
    y="Net_Intake_Pressure"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# BACKLOG
# -------------------

st.subheader(
    "Backlog Accumulation"
)

fig = px.line(
    filtered_df,
    x="Date",
    y="Backlog_Accumulation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# DATA TABLE
# -------------------

st.subheader(
    "Dataset Preview"
)

st.dataframe(filtered_df)
