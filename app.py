import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px

from database import (
    create_table,
    add_donation,
    get_donations,
    reserve_donation,
    request_food,
    total_donations,
    total_meals_saved,
    reserved_donations
)
create_table()

st.set_page_config(
    page_title="FoodLink",
    page_icon="🍲"
)

st.title("🍲 FoodLink")
st.subheader("Connecting Surplus Food with NGOs")

page = st.sidebar.selectbox(
    "Choose Portal",
    [
        "Restaurant Dashboard",
        "NGO Dashboard",
        "Analytics Dashboard"
    ]
)

st.markdown("""
### 🌍 Reducing Food Waste, One Meal at a Time

Helping restaurants, caterers, and individuals donate surplus food to NGOs before it goes to waste.
""")

# =====================================
# RESTAURANT DASHBOARD
# =====================================

if page == "Restaurant Dashboard":

    st.header("🍲 Donate Surplus Food")

    food_name = st.text_input("Food Name")

    quantity = st.number_input(
        "Quantity (Meals)",
        min_value=1,
        step=1
    )

    donor_name = st.text_input(
        "Restaurant / Donor Name"
    )

    location = st.text_input("Location")

    pickup_deadline = st.date_input(
        "Pickup Deadline"
    )

    if st.button("Submit Donation"):

        add_donation(
            food_name,
            quantity,
            donor_name,
            location,
            pickup_deadline
        )

        st.success(
            "Donation Saved Successfully!"
        )

# =====================================
# ANALYTICS DASHBOARD
# =====================================

if page == "Analytics Dashboard":

    st.header("📊 Impact Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📦 Total Donations",
            total_donations()
        )

    with col2:
        st.metric(
            "🍽️ Meals Saved",
            total_meals_saved()
        )

    with col3:
        st.metric(
            "🤝 Reserved Donations",
            reserved_donations()
        )

    co2_saved = total_meals_saved() * 0.5

    st.info(
        f"🌱 Estimated CO₂ Prevented: {co2_saved:.1f} kg"
    )

    st.success(
        f"🍽️ Estimated People Fed: {total_meals_saved()}"
    )

    donations = get_donations()

    if donations:

        status_data = pd.DataFrame(
            donations,
            columns=[
                "ID",
                "Food",
                "Total Quantity",
                "Remaining Quantity",
                "Donor",
                "Location",
                "Deadline",
                "Status"
            ]
        )

        status_counts = (
            status_data["Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            status_counts,
            values="Count",
            names="Status",
            title="Donation Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================
# NGO DASHBOARD
# =====================================

if page == "NGO Dashboard":

    st.header("NGO Dashboard")

    ngo_name = st.text_input(
        "NGO Name"
    )

    ngo_contact = st.text_input(
        "Contact Number"
    )

    search_food = st.text_input(
        "🔍 Search Food Item"
    )

    donations = get_donations()

    for donation in donations:

        if (
            search_food
            and search_food.lower()
            not in donation[1].lower()
        ):
            continue

        st.markdown("---")

        st.markdown(f"""
### 🍲 {donation[1]}

📦 **Total Meals:** {donation[2]}

🍽️ **Remaining Meals:** {donation[3]}

🏢 **Donor:** {donation[4]}

📍 **Location:** {donation[5]}
""")

        st.write(
            "Deadline:",
            donation[6]
        )

        st.write(
            "Status:",
            donation[7]
        )

        deadline = date.fromisoformat(
            donation[6]
        )

        days_left = (
            deadline - date.today()
        ).days

        if days_left <= 1:
            st.error("🔴 HIGH PRIORITY")
        elif days_left <= 3:
            st.warning("🟡 MEDIUM PRIORITY")
        else:
            st.success("🟢 LOW PRIORITY")

        if donation[7] == "Available":

            requested_qty = st.number_input(
                f"Meals Needed for Donation #{donation[0]}",
                min_value=1,
                max_value=int(donation[3]),
                key=f"qty_{donation[0]}"
            )

            if st.button(
                f"Request Meals #{donation[0]}",
                key=f"request_{donation[0]}"
            ):

                if ngo_name == "" or ngo_contact == "":

                    st.error(
                        "Please enter NGO details first."
                    )

                else:

                    success = request_food(
                        donation[0],
                        requested_qty
                    )

                    if success:

                        st.success(
                            f"✅ {requested_qty} meals requested successfully!"
                        )

                        st.info(
                            f"""
NGO: {ngo_name}

Contact: {ngo_contact}

Requested Meals: {requested_qty}
"""
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Not enough meals available."
                        )


st.markdown("""
### 🌍 FoodLink

Connecting surplus food with NGOs to reduce hunger and food waste.

Built using Python, Streamlit and SQLite.
""")