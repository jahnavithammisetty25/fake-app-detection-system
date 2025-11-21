import streamlit as st
import json
import sys
import os

# FIX PATH SO PYTHON CAN FIND src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(
    page_title="Fake App Detection",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

html, body {
    background-color:#020611 !important;
    color:#E0F7FF !important;
    font-family:'Orbitron', sans-serif;
}

/* FIX TOP WHITE BAR */
[data-testid="stHeader"], header, [data-testid="stToolbar"] {
    background-color:#020611 !important;
}

/* FIX MAIN BACKGROUND */
[data-testid="stAppViewContainer"], .block-container {
    background-color:#020611 !important;
    color:#E0F7FF !important;
}

/* FIX LABEL TEXT (previously too dark) */
label, .stMarkdown p, [data-testid="stWidgetLabel"], .css-16idsys p {
    color:#7ee2f2 !important;
    font-size:15px !important;
}

/* INPUT BOX */
div[data-baseweb="input"] > div {
    background-color:rgba(0,40,60,0.7) !important;
    border:1px solid #00eaff !important;
    color:#E0F7FF !important;
}

/* SIDEBAR DARK MODE */
[data-testid="stSidebar"] {
    background:#000 !important;
    border-right:3px solid #00eaff;
    box-shadow:0 0 25px #00eaffaa;
}

/* SIDEBAR TEXT COLOR */
[data-testid="stSidebar"] * {
    color:#45caff !important;
}

/* FIX SIDEBAR CODE BLOCK (WAS WHITE) */
.sidebar-code, [data-testid="stCodeBlock"], pre, code {
    background:rgba(0, 20, 40, 0.9) !important;
    color:#7ee2f2 !important;
    border:1px solid #00eaff66 !important;
    border-radius:10px !important;
    padding:12px !important;
    font-size:14px !important;
}

/* MAIN TITLE */
.neon-title {
    font-size:48px;
    font-weight:800;
    color:#00f2ff;
    text-align:center;
    text-shadow:0 0 10px #00eaff, 0 0 25px #00eaff;
}

/* SUBTITLE */
.subtitle {
    text-align:center;
    color:#7ee2f2;
    margin-bottom:30px;
}

/* BUTTON */
.stButton>button {
    width:100%;
    padding:14px;
    border-radius:12px;
    border:2px solid #00eaff;
    background:rgba(0,20,40,0.8);
    color:#00eaff !important;
    font-size:18px;
    transition:0.3s;
}
.stButton>button:hover {
    background:#00eaff;
    color:#00151c !important;
    box-shadow:0 0 20px #00eaff;
    transform:scale(1.03);
}

/* RESULT CARD */
.card {
    background:rgba(0,20,40,0.55);
    padding:25px;
    border-radius:15px;
    border:2px solid #00eaff;
    margin-top:20px;
}

/* REASON BOX */
.reason {
    background:rgba(0,60,80,0.45);
    border-left:4px solid #00eaff;
    padding:10px;
    border-radius:8px;
    margin-top:6px;
}

/* RISK TAGS */
.tag {
    padding:6px 14px;
    border-radius:15px;
    font-weight:600;
    color:black !important;
}
.tag-high { background:#ff0048; box-shadow:0 0 20px #ff0048aa; }
.tag-medium { background:#ffaa00; box-shadow:0 0 20px #ffaa00aa; }
.tag-low { background:#00ff85; box-shadow:0 0 20px #00ff85aa; }

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.markdown("<h2 class='sidebar-title'>⚡ TEAM G4</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🟦 Features")
st.sidebar.markdown("- Risk Scoring Engine")
st.sidebar.markdown("- Fake App Detection")
st.sidebar.markdown("- Evidence Kit Export")

st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Instructions")
st.sidebar.info("Enter a UPI brand name in the main screen and click **Run Analysis**.")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🧪 Example Brands")

# FIX CODE BLOCK WRAPPER
st.sidebar.markdown(
    "<pre class='sidebar-code'>PhonePe\GPay\Paytm\BHIM</pre>", 
    unsafe_allow_html=True
)

# ---------------- HEADER ---------------- #
st.markdown("<h1 class='neon-title'>🕵️‍♂️ Fake App Detection</h1>", unsafe_allow_html=True)

# ---------------- INPUT ---------------- #
brand = st.text_input("Enter UPI Brand (PhonePe / Paytm / GPay / BHIM)", placeholder="Type brand here...")

def risk_tag(score):
    if score > 80:
        return "<span class='tag tag-high'>🔴 HIGH RISK</span>"
    elif score > 50:
        return "<span class='tag tag-medium'>🟠 MEDIUM RISK</span>"
    else:
        return "<span class='tag tag-low'>🟢 LOW RISK</span>"


def generate_kit(result):
    text = "==== EVIDENCE KIT ====\n\n"
    for r in result:
        text += f"App Name: {r['app_name']}\n"
        text += f"Risk: {r['risk']}\n"
        text += "Reasons:\n"
        for s in r['reasons']:
            text += f" • {s}\n"
        text += "\n"
    return text

if st.button("Run Analysis"):
    from src.pipeline import run_detection
    result = run_detection(brand)

    for r in result:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h2>{r['app_name']}</h2>", unsafe_allow_html=True)
        st.markdown(risk_tag(r["risk"]), unsafe_allow_html=True)

        st.write("### Reasons:")
        for reason in r["reasons"]:
            st.markdown(f"<div class='reason'>• {reason}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.download_button("📄 Download Evidence Kit", generate_kit(result), "evidence.txt")
