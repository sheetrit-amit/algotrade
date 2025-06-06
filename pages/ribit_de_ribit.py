import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title
st.title("💸 What Will Happen to Your Money? Choose and Invest Wisely")

st.markdown("This is an interactive simulator that shows how your money can grow over time – depending on **how much you save** and **where you invest** it.")

# Inputs
initial_amount = st.slider("💰 Initial investment amount (₪)", 100, 20000, 1000, step=100)
monthly_contribution = st.slider("📥 Monthly contribution (₪)", 0, 5000, 500, step=100)
years = st.slider("⏳ Investment duration (years)", 1, 40, 10)

investment_option = st.radio(
    "📊 Choose your type of investment",
    (
        "Bank deposit (low risk)",
        "Index fund (medium risk)",
        "Cryptocurrency (high risk)"
    )
)

# Assign interest rate and explanation
if investment_option == "Bank deposit (low risk)":
    annual_rate = 2.0
    explanation = """
    🔐 **Bank deposit** is a safe and stable option. Very low risk, but also low returns.
    Ideal for people who prefer stability and no surprises.
    """
elif investment_option == "Index fund (medium risk)":
    annual_rate = 7.0
    explanation = """
    📈 **Index funds** invest in a wide range of companies (e.g., S&P 500). Medium risk with strong long-term growth potential.
    A smart choice for long-term thinkers.
    """
else:
    annual_rate = 12.0
    explanation = """
    🚀 **Cryptocurrency** can rise fast – but also crash fast. It's highly volatile and risky.
    Not suitable for everyone and requires the ability to tolerate potential losses.
    """

# Show educational explanation
st.markdown("### 🧠 Financial Insight")
st.info(explanation)

# Compound interest calculation
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

# Chart
st.markdown("### 📉 Growth Over Time: With Interest vs. Without")

fig, ax = plt.subplots()
ax.plot(balance, label="With compound interest")
ax.plot(cash_no_interest, label="No interest (just savings)")
ax.set_xlabel("Months")
ax.set_ylabel("₪")
ax.set_title("Investment Growth Over Time")
ax.legend()
st.pyplot(fig)

# Summary
final_gain = balance[-1] - cash_no_interest[-1]
st.markdown(f"🎯 After {years} years, you'll have **₪{int(balance[-1]):,}**, compared to **₪{int(cash_no_interest[-1]):,}** without interest.")
st.success(f"💡 Total gain from compound interest: **₪{int(final_gain):,}**")
