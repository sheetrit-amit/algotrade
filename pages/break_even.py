import streamlit as st

st.set_page_config(page_title="Break Even Game", page_icon="📉", layout="centered")

st.title("📉 Break Even Game!")
st.write("Learn how when a stock falls, it needs a bigger % rise to break even.")

st.header("How it works:")
st.write("""
👉 If a stock falls by X%,  
you need **more than X%** rise to get back to the original value!  
This is because the new value is smaller.
""")

# Interactive slider
percent_drop = st.slider("Choose how much % the stock fell:", min_value=1, max_value=95, value=10)

# Compute break-even % rise
drop_fraction = percent_drop / 100
remaining_fraction = 1 - drop_fraction
percent_needed_up = (1 / remaining_fraction - 1) * 100

# Display result
st.subheader(f"📉 The stock fell by {percent_drop} %")
st.subheader(f"📈 It now needs to rise by **{percent_needed_up:.1f} %** to break even!")

# Visual illustration
st.progress(int(percent_drop))
st.write("⬇️ Fall")
st.progress(int(min(percent_needed_up, 100)))
st.write("⬆️ Rise needed to break even")

# Fun tip for kids
st.info("💡 The more a stock falls, the harder it is to recover! Be patient and think long-term! 🚀")

