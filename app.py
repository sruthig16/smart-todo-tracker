import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

# 🔥 MUST BE HERE — FIRST Streamlit command
st.set_page_config(
    page_title="My Smart Tracker",
    page_icon="📊",
    layout="centered"
)

st.markdown("<h2 style='color: teal;'>🌅 Morning Routine</h2>", unsafe_allow_html=True)

# Set app title
st.title("📋 Smart To-Do & Weight Tracker")

# Initialize session state
if 'weights' not in st.session_state:
    st.session_state.weights = []

# --- Daily To-Do ---
st.header("✅ Daily Checklist")

st.subheader("📂 Office Work")
office_tasks = ["Check emails", "Team stand-up", "Work on tasks", "Attend meetings", "Log progress"]
for task in office_tasks:
    st.checkbox(task, key=f"office_{task}")

st.subheader("💪 Exercise")
exercise_tasks = ["Morning stretch (15 mins)", "Cardio/Gym (30 mins)", "Drink 8 glasses of water"]
for task in exercise_tasks:
    st.checkbox(task, key=f"exercise_{task}")

st.subheader("📚 Personal Development")
personal_tasks = ["Read 30 mins", "Practice Skill",]
for task in personal_tasks:
    st.checkbox(task, key=f"personal_{task}")

# --- Monthly Goal ---
st.header("📆 Monthly Goal")
st.write("🎯 Reduce 2kg this month")

# --- Weight Tracker ---
st.header("📊 Weight Progress Tracker")

today = date.today()
weight_input = st.number_input(f"Enter your weight for {today} (kg)", min_value=0.0, step=0.1)

if st.button("📥 Save Weight"):
    st.session_state.weights.append((str(today), weight_input))
    st.success(f"Saved weight for {today}: {weight_input} kg")

# Show weight log
if st.session_state.weights:
    df = pd.DataFrame(st.session_state.weights, columns=["Date", "Weight"])
    st.line_chart(df.set_index("Date"))

st.markdown("<h1 style='color:indigo;'>📋 My Daily Dashboard</h1>", unsafe_allow_html=True)
st.markdown("> _“Small steps every day lead to big results.”_")

# Footer
st.markdown("---")
st.caption("Built with ❤️ in Streamlit")

st.markdown("> _“Discipline is doing what needs to be done, even when you don’t feel like doing it.”_")
