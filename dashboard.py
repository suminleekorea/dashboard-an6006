# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

# ------------------------------------------------
# 1. Function to generate simulated truck data
# ------------------------------------------------

def generate_truck_data(n_trucks: int = 30, seed: int = None) -> pd.DataFrame:
    """
    This function generates random truck data for demonstration.
    In a real system, you would replace this with:
    - Kafka consumer
    - API call
    - Database query
    """
    if seed is not None:
        np.random.seed(seed)

    # Base location (Midwest USA region for demo)
    base_lat = 41.0
    base_lon = -93.0

    truck_ids = [f"T{str(i).zfill(3)}" for i in range(1, n_trucks + 1)]
    now = dt.datetime.utcnow()

    # Random GPS coordinates
    current_lat = base_lat + np.random.randn(n_trucks) * 1.0
    current_lon = base_lon + np.random.randn(n_trucks) * 1.0

    # Random speed
    speed_kmh = np.random.uniform(30, 90, size=n_trucks)

    # Random remaining distance
    remaining_km = np.random.uniform(5, 150, size=n_trucks)

    # ETA = distance / speed
    remaining_hours = remaining_km / speed_kmh
    eta_times = [now + dt.timedelta(hours=float(h)) for h in remaining_hours]

    # SLA deadlines (0.5–3 hours range)
    sla_hours = np.random.uniform(0.5, 3.0, size=n_trucks)
    sla_deadlines = [now + dt.timedelta(hours=float(h)) for h in sla_hours]

    # Delay calculation
    delay_minutes = [
        (eta_times[i] - sla_deadlines[i]).total_seconds() / 60.0
        for i in range(n_trucks)
    ]

    delay_status = []
    risk_score = []
    risk_label = []

    for d in delay_minutes:
        if d <= -15:
            delay_status.append("On Time")
            risk_score.append(0.2)
            risk_label.append("Low")
        elif -15 < d <= 0:
            delay_status.append("Near SLA")
            risk_score.append(0.5)
            risk_label.append("Medium")
        else:
            delay_status.append("Delayed")
            score = min(1.0, 0.5 + d / 60.0)
            risk_score.append(score)
            risk_label.append("High")

    # Empty truck indicator
    is_empty = np.random.rand(n_trucks) < 0.25
    potential_pickups = np.where(is_empty, np.random.randint(0, 6, size=n_trucks), 0)

    df = pd.DataFrame(
        {
            "truck_id": truck_ids,
            "lat": current_lat,
            "lon": current_lon,
            "speed_kmh": speed_kmh.round(1),
            "remaining_km": remaining_km.round(1),
            "eta_utc": eta_times,
            "sla_deadline_utc": sla_deadlines,
            "delay_minutes_vs_sla": np.round(delay_minutes, 1),
            "delay_status": delay_status,
            "risk_score": np.round(risk_score, 2),
            "risk_label": risk_label,
            "is_empty": is_empty,
            "potential_pickups_nearby": potential_pickups,
        }
    )

    return df


# ------------------------------------------------
# 2. Main Streamlit App
# ------------------------------------------------

def main():

    st.set_page_config(
        page_title="StreamLine Logistics Dashboard",
        layout="wide"
    )

    st.title("🚚 StreamLine Real-Time Operations Dashboard")
    st.write("Created by: **Sumin Lee**")
    st.write("Simulated data only")
    st.markdown("---")

    # Generate simulated truck data
    df = generate_truck_data(n_trucks=30)

    # KPI boxes
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trucks", len(df))
    col2.metric("Delayed Trucks", (df["delay_status"]=="Delayed").sum())
    col3.metric("Near SLA", (df["delay_status"]=="Near SLA").sum())
    col4.metric("Empty Trucks", df["is_empty"].sum())

    st.markdown("---")

    # 1. Live Map
    st.subheader("1. Live Map of All Trucks")
    st.map(df[["lat", "lon"]])

    # 2. ETA and Delay Alerts
    st.subheader("2. Real-Time ETA and Delay Alerts")
    alerts = df[df["delay_status"].isin(["Delayed", "Near SLA"])]

    if alerts.empty:
        st.success("All trucks are currently on time.")
    else:
        st.warning("Some trucks are delayed or close to SLA.")
        st.dataframe(alerts)

    # 3. SLA Risk Monitoring
    st.subheader("3. SLA Risk Monitoring")
    risk_table = df["risk_label"].value_counts()
    st.table(risk_table)

    st.dataframe(
        df[["truck_id","risk_label","risk_score","delay_status","eta_utc","sla_deadline_utc"]]
        .sort_values("risk_score", ascending=False)
    )

    # 4. Pickup Opportunities
    st.subheader("4. Pickup Opportunities for Empty Trucks")
    empty_df = df[df["is_empty"]]

    if empty_df.empty:
        st.info("No empty trucks right now.")
    else:
        st.dataframe(empty_df)
        st.map(empty_df[["lat","lon"]])


if __name__ == "__main__":
    main()
