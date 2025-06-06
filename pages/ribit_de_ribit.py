import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# --- הגדרות עיצוב עברית לגרפים ---
rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# --- כותרת ---
st.set_page_config(page_title="ריבית דריבית", layout="centered")
st.markdown("""
<h1 style='text-align: right; direction: rtl;'>
💸 ריבית דריבית: תשקיע חכם, תרוויח בגדול
</h1>
<p style='text-align: right; direction: rtl;'>
זהו סימולטור אינטראקטיבי שממחיש את <strong>הכוח של ריבית דריבית</strong>.
באמצעות הדגמות, גרפים, שאלות והשוואות - תבין למה כדאי להתחיל לחסוך כמה שיותר מוקדם.
</p>
""", unsafe_allow_html=True)

# --- תרחישי הדגמה ---
st.markdown("<h3 style='text-align: right; direction: rtl;'>📊 השוואה בין תרחישים</h3>", unsafe_allow_html=True)
scenario = st.radio("בחר תרחיש להשוואה:", (
    "אייל התחיל לחסוך בגיל 20", 
    "בר חוסכת מגיל 30", 
    "גל התחיל רק בגיל 40",
    "אני מגדיר לבד"
), index=3)

if scenario == "אייל התחיל לחסוך בגיל 20":
    initial_amount = 5000
    monthly_contribution = 500
    years = 40
    investment_option = "קרן מדדים"
elif scenario == "בר חוסכת מגיל 30":
    initial_amount = 5000
    monthly_contribution = 700
    years = 30
    investment_option = "קרן מדדים"
elif scenario == "גל התחיל רק בגיל 40":
    initial_amount = 10000
    monthly_contribution = 1000
    years = 20
    investment_option = "קריפטו"
else:
    st.markdown("---")
    initial_amount = st.slider("💰 סכום התחלתי (ש""ח)", 100, 20000, 5000, step=100)
    monthly_contribution = st.slider("📥 הפקדה חודשית (ש""ח)", 0, 5000, 500, step=100)
    years = st.slider("⏳ כמה שנים תחסוך?", 1, 40, 30)
    investment_option = st.selectbox("בחר סוג השקעה", ("פיקדון בנקאי", "קרן מדדים", "קריפטו"))

# --- קביעת ריבית ---
if investment_option == "פיקדון בנקאי":
    annual_rate = 2.0
    explanation = "🔐 השקעה בטוחה אך עם תשואה נמוכה. מתאימה למי שמעדיף יציבות."
elif investment_option == "קרן מדדים":
    annual_rate = 7.0
    explanation = "📈 השקעה לטווח ארוך במניות מגוונות. תשואה ממוצעת ויציבות יחסית."
else:
    annual_rate = 12.0
    explanation = "🚀 השקעה תנודתית עם פוטנציאל רווח גבוה - וגם סיכון בהתאם."

st.markdown(f"<div style='direction: rtl; text-align: right;'>{explanation}</div>", unsafe_allow_html=True)

# --- חישוב ריבית דריבית ---
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

# --- גרף בעברית ---
st.markdown("<h3 style='text-align: right; direction: rtl;'>📈 כך הכסף שלך גדל עם הזמן</h3>", unsafe_allow_html=True)

fig, ax = plt.subplots()
ax.plot(balance, label="עם ריבית דריבית")
ax.plot(cash_no_interest, label="בלי ריבית (רק הפקדות)")
ax.set_xlabel("חודשים", fontsize=12)
ax.set_ylabel("ש""ח", fontsize=12)
ax.set_title(f"צמיחה לאורך {years} שנים", fontsize=14)
ax.legend(loc='upper left')
ax.grid(True)

st.pyplot(fig)

# --- תוצאה ---
final_gain = balance[-1] - cash_no_interest[-1]
st.markdown(f"<div style='direction: rtl; text-align: right;'>📌 אחרי <strong>{years}</strong> שנים תחסוך <strong>{int(balance[-1]):,}</strong> ש""ח, מתוכם <strong>{int(final_gain):,}</strong> ש""ח בזכות ריבית דריבית.</div>", unsafe_allow_html=True)

st.caption(f"🕒 זה שווה ערך ל-{months} חודשים של חיסכון והשקעה.")

# --- חידון קטן ---
st.markdown("<h3 style='text-align: right; direction: rtl;'>❓ חידון מהיר</h3>", unsafe_allow_html=True)
guess = st.number_input("אם תחסוך 300 ש""ח בחודש למשך 25 שנה בריבית של 7% – כמה תצבור בערך?", min_value=0, step=1000)
true_value = 300 * (((1 + 0.07/12) ** (12*25) - 1) / (0.07/12))

if guess > 0:
    diff = abs(guess - true_value)
    if diff < 5000:
        st.success("🎉 כל הכבוד! אתה מאוד קרוב לתוצאה האמיתית")
    else:
        st.error(f"כמעט! הסכום הנכון הוא בערך {int(true_value):,} ש""ח")

# --- טיפ מסכם ---
st.markdown("""
<h3 style='text-align: right; direction: rtl;'>💡 טיפ חשוב לסיום</h3>
<p style='text-align: right; direction: rtl;'>
ריבית דריבית עובדת לטובתך – אבל רק אם תיתן לה <strong>זמן</strong>. 
ככל שתתחיל מוקדם יותר, כך הכסף שלך יוכל לגדול יותר.
</p>
""", unsafe_allow_html=True)
