import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("/Users/celinaradwan2004/Desktop/MSBA/Célina-Radwan_Data-Visualization/8080fb0ab00e5cf690059cfbbdd239a4_20241009_172125_updated.csv")

st.header("Drill down your preferences!", divider = "rainbow")

st.markdown("##### Compare Immigrants Distribution by Nationality Within and Across Lebanese Governorates")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Select Governorates**")
    all_governorates = sorted(df["Governorate"].unique())
    selected_governorates = []
    remaining_govs = all_governorates.copy()

    for i in range(len(all_governorates)):
        if not remaining_govs:
            break
        gov_choice = st.selectbox(
            f"Governorate {i+1}",
            options=["--"] + remaining_govs,
            key=f"gov_{i}"
        )
        if gov_choice != "--":
            selected_governorates.append(gov_choice)
            remaining_govs = [g for g in remaining_govs if g != gov_choice]
        else:
            break

with col2:
    st.markdown("**Select Nationalities**")
    all_nationalities = sorted(df["Nationality"].unique())
    selected_nationalities = []
    remaining_nats = all_nationalities.copy()

    for i in range(len(all_nationalities)):
        if not remaining_nats:
            break
        nat_choice = st.selectbox(
            f"Nationality {i+1}",
            options=["--"] + remaining_nats,
            key=f"nat_{i}"
        )
        if nat_choice != "--":
            selected_nationalities.append(nat_choice)
            remaining_nats = [n for n in remaining_nats if n != nat_choice]
        else:
            break

immigrants_range = st.slider(
    "Filter by Number of Immigrants:",
    0, int(df["Number of Immigrants"].max()),
    (0, int(df["Number of Immigrants"].max()))
)

bar_mode = st.radio(
    "Choose Bar Mode:",
    options=["stack", "group"],
    index=0,
    horizontal=True
)

if selected_governorates and selected_nationalities:
    filtered_df = df[
        (df["Governorate"].isin(selected_governorates)) &
        (df["Nationality"].isin(selected_nationalities)) &
        (df["Number of Immigrants"].between(immigrants_range[0], immigrants_range[1]))
    ]

    if not filtered_df.empty:
        fig3 = px.bar(
            filtered_df,
            x="Governorate",
            y="Number of Immigrants",
            color="Nationality",
            title=f"Immigrants in {', '.join(selected_governorates)} "
                  f"for {', '.join(selected_nationalities)}",
            barmode=bar_mode
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("⚠️ No data available with the current filters. Try adjusting the selections or slider.")
else:
    st.info("Please select at least one governorate **and** one nationality for a bar chart to appear below 👇")

st.markdown(
    """
    <div style="border:1px solid #ddd; padding:15px; border-radius:5px; background-color:#f9f9f9;">
    Beirut is the main hub for immigrants across all nationalities, followed by Mount Lebanon. 
    Some governorates, such as Akkar, have very few immigrants, making their bars almost invisible. 
    Baalbek has low numbers for most nationalities, except for Ethiopians, who are significantly represented there.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("##### Explore Immigrants Distribution by Governorate, District, and Nationality in Lebanon")

col1, col2 = st.columns(2)

with col1:
    selected_governorates = st.multiselect(
        "Select Governorate(s) (leave empty to show all):",
        options=df["Governorate"].unique(),
        default=df["Governorate"].unique()
    )

    available_districts = df[df["Governorate"].isin(selected_governorates)]["District"].unique()
    selected_districts = st.multiselect(
        "Select District(s) (leave empty to show all):",
        options=available_districts,
        default=available_districts
    )

    selected_nationalities = st.multiselect(
        "Select Nationality(s) (leave empty to show all):",
        options=df["Nationality"].unique(),
        default=df["Nationality"].unique()
    )

    filtered_df = df[
        df["Governorate"].isin(selected_governorates) &
        df["District"].isin(selected_districts) &
        df["Nationality"].isin(selected_nationalities)
    ]

with col2:
    fig5 = px.sunburst(
        filtered_df,
        path=['Governorate', 'District', 'Nationality'],
        values='Number of Immigrants'
    )
    st.plotly_chart(fig5)

st.markdown(
    """
    <div style="border:1px solid #ddd; padding:15px; border-radius:5px; background-color:#f9f9f9;">
    In the North Governorate, Bsharri has the fewest immigrants, while Zgharta has the most. 
    This district-level view highlights variations within districts that are not visible in the aggregated bar chart, 
    which provides a high-level overview of immigrant nationality distributions within and across governorates.
    </div>
    """,
    unsafe_allow_html=True
)