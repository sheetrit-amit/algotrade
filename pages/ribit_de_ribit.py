import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# --- Set up English font and styling ---
rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# --- Page configuration ---
st.set_page_config(page_title="Compound Interest Simulator", layout="centered")
st.title("💸 Compound Interest: Invest Smart, Earn Big")

st.markdown("""
This is an interactive simulator that demonstrates the **power of compound interest**.
With visualizations, comparisons, and a quick quiz, you'll learn why starting early matters.
""")

# --- Scenarios ---
st.markdown("### 📊 Choose a scenario")
scenario = st.radio("Select a scenario to visualize:", (
    "Eyal starts investing at age 20", 
    "Bar starts at age 30", 
    "Gal starts at age 40",
    "Customize your own"
), index=3)

# All use the same interest rate (Index Fund)
annual_rate = 7.0
investment_option = "Index Fund"

if scenario == "Eyal starts investing at age 20":
    initial_amount = 5000
    monthly_contribution = 500
    years = 40
    info = "Eyal invested ₪5,000 initially and ₪500 per month for 40 years (Total invested: ₪245,000)."
elif scenario == "Bar starts at age 30":
    initial_amount = 5000
    monthly_contribution = 700
    years = 30
    info = "Bar invested ₪5,000 initially and ₪700 per month for 30 years (Total invested: ₪259,000)."
elif scenario == "Gal starts at age 40":
    initial_amount = 10000
    monthly_contribution = 1000
    years = 20
    info = "Gal invested ₪10,000 initially and ₪1,000 per month for 20 years (Total invested: ₪250,000)."
else:
    st.markdown("---")
    initial_amount = st.slider("💰 Initial investment amount (₪)", 100, 20000, 5000, step=100)
    monthly_contribution = st.slider("📥 Monthly contribution (₪)", 0, 5000, 500, step=100)
    years = st.slider("⏳ How many years will you invest?", 1, 40, 30)
    investment_option = st.selectbox("📊 Choose your investment type:", ("Bank Deposit", "Index Fund", "Crypto"))

    if investment_option == "Bank Deposit":
        annual_rate = 2.0
        explanation = "🔐 A safe but low-return investment. Ideal for risk-averse individuals."
    elif investment_option == "Index Fund":
        annual_rate = 7.0
        explanation = "📈 Long-term diversified stock investment. Balanced risk and return."
    else:
        annual_rate = 12.0
        explanation = "🚀 High potential return with high volatility. Risky but possibly rewarding."

    st.info(explanation)
    info = f"You chose to invest ₪{initial_amount} initially and ₪{monthly_contribution} per month for {years} years (Total invested: ₪{initial_amount + monthly_contribution * years * 12:,})."

st.markdown(f"#### 💡 Investment Summary\n{info}")

st.info("📈 Long-term diversified stock investment. Balanced risk and return.")

# --- Compound Interest Calculation ---
months = years * 12
monthly_rate = (1 + annual_rate / 100) ** (1 / 12) - 1

balance = []
cash_no_interest = []
current = initial_amount

for month in range(months + 1):
    if month > 0:
        current = current * (1 + monthly_rate) + monthly_contribution
    balance.append(current)
    cash_no_interest.append(initial_amount + monthly_contribution * month)

# --- Chart ---
st.markdown("### 📈 How your money grows over time")

fig, ax = plt.subplots()
ax.plot(range(years + 1), [balance[i * 12] for i in range(years + 1)], label="With Compound Interest")
ax.plot(range(years + 1), [cash_no_interest[i * 12] for i in range(years + 1)], label="No Interest (just deposits)")
ax.set_xlabel("Years", fontsize=12)
ax.set_ylabel("₪", fontsize=12)
ax.set_title(f"Growth Over {years} Years", fontsize=14)
ax.legend(loc='upper left')
ax.grid(True)

st.pyplot(fig)

# --- Summary ---
final_gain = balance[-1] - cash_no_interest[-1]
if scenario.startswith("Eyal"):
    name = "Eyal"
elif scenario.startswith("Bar"):
    name = "Bar"
elif scenario.startswith("Gal"):
    name = "Gal"
else:
    name = "you"

st.markdown(f"📌 After **{years} years**, {name} will have **₪{int(balance[-1]):,}**, including **₪{int(final_gain):,}** from compound interest.")

st.caption(f"🕒 That's a total of {months} months of saving and investing.")

# --- Quick Quiz ---
st.markdown("### ❓ Quick Quiz")
guess = st.number_input("If you save ₪300/month for 25 years at 7% interest – how much will you have?", min_value=0, step=1000)
true_value = 300 * (((1 + 0.07/12) ** (12*25) - 1) / (0.07/12))

if guess > 0:
    diff = abs(guess - true_value)
    if diff < 5000:
        st.success("🎉 Great job! You're very close to the correct answer.")
    else:
        st.error(f"Almost! The correct value is about ₪{int(true_value):,}")

# --- Final Tip ---
st.markdown("""
### 💡 Final Tip
Compound interest works best when you give it **time**. The earlier you start, the more your money can grow.
""")
