import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")
st.title("🚗 Uber-Style Live Vehicle Tracking")

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["vehicle_db"]
collection = db["vehicle_data"]

# Fetch data
data = list(collection.find().sort("timestamp", -1).limit(1000))

if not data:
    st.warning("No data found")
    st.stop()

df = pd.DataFrame(data)

# Clean
df = df.dropna(subset=["lat", "lon"])

# 🔥 Keep latest per vehicle
df = df.sort_values("timestamp").groupby("car_id").tail(1)

# 🔥 Reduce overlap
df["lat"] += np.random.uniform(-0.0003, 0.0003, len(df))
df["lon"] += np.random.uniform(-0.0003, 0.0003, len(df))

# 🔴 Speed category
def get_color(speed):
    if speed < 60:
        return "LOW"
    elif speed < 90:
        return "MEDIUM"
    else:
        return "HIGH"

df["speed_category"] = df["speed"].apply(get_color)

# Layout
col1, col2 = st.columns([2, 1])

# 📍 MAP
with col1:
    st.subheader("📍 Live Vehicles (Uber Style)")

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="speed_category",
        size_max=8,
        hover_data=["car_id", "speed"],
        zoom=11,
        height=650,
        opacity=0.7
    )

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# 📊 STATS
with col2:
    st.subheader("📊 Stats")

    st.metric("🚗 Vehicles", len(df))
    st.metric("⚡ Avg Speed", round(df["speed"].mean(), 2))

    moving = df[df["speed"] > 10].shape[0]
    stopped = df[df["speed"] <= 10].shape[0]

    st.metric("🟢 Moving", moving)
    st.metric("🔴 Stopped", stopped)

    st.subheader("📈 Speed Distribution")
    fig2 = px.histogram(df, x="speed", nbins=15)
    st.plotly_chart(fig2, use_container_width=True)

# 🔄 Auto refresh (IMPORTANT)
st.experimental_autorefresh(interval=2000, key="refresh")