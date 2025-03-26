import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Smart To-Do & Weight Tracker", layout="centered")
st.title("📋 Smart To-Do & Weight Tracker (Morning & Evening)")

# Track daily mode
mode = st.radio("Select your session:", ["🌅 Morning", "🌇 Evening"])

# Initialize session state
if 'morning_weights' not in st.session_state:
    st.session_state.morning_weights = []
if 'evening_weights' not in st.session_state:
    st.session_state.evening_weights = []

# ------------------------
# 🧾 Daily Checklist
# ------------------------
st.header(f"✅ {mode} Checklist")

if mode == "🌅 Morning":
    st.subheader("📂 Office Prep")
    for task in ["Plan tasks", "Review emails", "Daily stand-up"]:
        st.checkbox(task, key=f"morning_office_{task}")

    st.subheader("💪 Morning Exercise")
    for task in ["Stretching", "Cardio / Walk", "Drink water"]:
        st.checkbox(task, key=f"morning_exercise_{task}")

    st.subheader("🧠 Mindset")
    for task in ["Read 10 mins", "Journal / Affirmations"]:
        st.checkbox(task, key=f"morning_mindset_{task}")

else:
    st.subheader("📂 Work Wrap-Up")
    for task in ["Check-off tasks", "Daily sync", "Log progress"]:
        st.checkbox(task, key=f"evening_office_{task}")

    st.subheader("💪 Evening Routine")
    for task in ["Light walk", "Stretch / Relax", "Drink water"]:
        st.checkbox(task, key=f"evening_exercise_{task}")

    st.subheader("🧠 Mind Reset")
    for task in ["Read", "Reflect / Gratitude"]:
        st.checkbox(task, key=f"evening_mindset_{task}")

# ------------------------
# 📆 Monthly Goal
# ------------------------
st.header("🎯 Monthly Goal")
st.markdown("- Reduce **2kg** this month")
st.markdown("- Stay consistent with both morning and evening routines")

# ------------------------
# 📈 Weight Tracker
# ------------------------
st.header(f"📈 {mode} Weight Entry")

today = str(date.today())
weight = st.number_input(f"Enter your {mode.lower()} weight for {today} (kg)", min_value=0.0, step=0.1)

if st.button(f"📥 Save {mode} Weight"):
    if mode == "🌅 Morning":
        st.session_state.morning_weights.append((today, weight))
        st.success(f"Saved morning weight: {weight} kg")
    else:
        st.session_state.evening_weights.append((today, weight))
        st.success(f"Saved evening weight: {weight} kg")

# ------------------------
# 📊 Chart Visualization
# ------------------------
if st.session_state.morning_weights or st.session_state.evening_weights:
    st.subheader("📊 Weight Trend")

    chart_data = pd.DataFrame()

    if st.session_state.morning_weights:
        morning_df = pd.DataFrame(st.session_state.morning_weights, columns=["Date", "Morning Weight"])
        chart_data = morning_df.set_index("Date")

    if st.session_state.evening_weights:
        evening_df = pd.DataFrame(st.session_state.evening_weights, columns=["Date", "Evening Weight"])
        evening_df = evening_df.set_index("Date")

        if not chart_data.empty:
            chart_data = chart_data.join(evening_df, how='outer')
        else:
            chart_data = evening_df

    st.line_chart(chart_data)

# ------------------------
# 🧠 AI Assistant Tab
# ------------------------
st.markdown("---")
tabs = st.tabs(["💬 Daily Tracker", "🧠 Ask AI"])

with tabs[1]:
    st.subheader("🧠 Ask AI Anything")
    prompt = st.text_input("Type your question (e.g., 'How to stay focused?')")

    if st.button("🎯 Get AI Tip"):
        if prompt:
            # Mock AI logic here
            prompt_lower = prompt.lower()
            if "productivity" in prompt_lower:
                ai_response = "Try using the Pomodoro technique: 25 mins focused work + 5 mins break."
            elif "fitness" in prompt_lower or "weight" in prompt_lower:
                ai_response = "Start with 15-minute walks after meals and increase weekly."
            else:
                ai_response = "Stay consistent. Small steps daily lead to big wins."

            st.success(ai_response)
        else:
            st.warning("Please enter a prompt first.")

# ------------------------
# Footer
# ------------------------
st.markdown("---")
st.caption("Built with ❤️ for your daily rhythm")
