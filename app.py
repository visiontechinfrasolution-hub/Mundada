import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="Visiontech Mundada | Elegant Portal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE ELEGANT LIGHT UI STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    /* Global Overrides */
    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Background - Soft Gradient */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        color: #2d3436;
    }

    /* Header Styling */
    h1 {
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #0984e3; /* Royal Blue */
        margin-bottom: 0px;
    }
    h2, h3 {
        color: #2d3436;
        font-weight: 600;
    }

    /* Professional Sidebar - White & Clean */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e1e4e8;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 2rem;
    }

    /* Metric Cards - Elegant White */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(9, 132, 227, 0.15);
        border-color: #0984e3;
    }
    [data-testid="stMetricValue"] > div {
        color: #0984e3 !important;
        font-weight: 800;
    }

    /* Glassmorphism Forms - Light Theme */
    div.stForm {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid #ffffff;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        margin-top: 20px;
    }

    /* Input Fields styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #ffffff !important;
        border: 1px solid #dfe6e9 !important;
        color: #2d3436 !important;
        border-radius: 12px;
        padding: 10px 15px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #0984e3 !important;
        box-shadow: 0 0 8px rgba(9, 132, 227, 0.2) !important;
    }

    /* Elegant Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.4s ease;
        box-shadow: 0 4px 15px rgba(9, 132, 227, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(9, 132, 227, 0.4);
    }
    
    /* Footer */
    .elegant-footer {
        text-align: center;
        padding: 40px;
        color: #636e72;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

@st.cache_resource
def get_supabase():
    return create_client(URL, KEY)

supabase = get_supabase()

# --- 4. SIDEBAR REDESIGN ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #636e72; font-weight: 600; margin-bottom: 30px;'>OPERATIONS PORTAL</div>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Overview Dashboard", "🏗️ Project Site Registry", "💸 Financial Control Center"])
    st.divider()
    st.info("Authorized Personnel Only\n\nUser: Mayur Patil")

# --- 5. DASHBOARD PAGE ---
if page == "🏠 Overview Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #636e72; font-size: 18px; margin-bottom: 30px;'>Mundada operational status at a glance.</p>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Sites", "12", "+2")
    m2.metric("PO Value", "₹ 45.2L", "Updated Today")
    m3.metric("Collection", "₹ 28.5L", "63% Target")
    m4.metric("Payables", "₹ 4.1L", "Processing")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Performance Snapshot")
    chart_data = pd.DataFrame({'Target': [10, 20, 30, 40, 50], 'Actual': [8, 18, 25, 38, 48]})
    st.line_chart(chart_data)

# --- 6. SITE DATA PAGE ---
elif page == "🏗️ Project Site Registry":
    st.markdown("<h1>📝 Site Registration</h1>", unsafe_allow_html=True)
    
    with st.form("elegant_form", clear_on_submit=True):
        st.markdown("### 📍 Location & Description")
        c1, c2, c3 = st.columns(3)
        p_id = c1.text_input("Project ID")
        s_id = c2.text_input("Site ID")
        s_name = c3.text_input("Site Name")
        
        c4, c5 = st.columns([1, 2])
        cluster = c4.text_input("Cluster")
        work_desc = c5.text_area("Work Description", height=70)
        
        st.divider()
        st.markdown("### 📑 PO & Team Assignment")
        c6, c7, c8 = st.columns(3)
        p_amt = c6.number_input("Project Amt (₹)", min_value=0.0)
        po_no = c7.text_input("PO Number")
        po_amt = c8.number_input("PO Amount (₹)", min_value=0.0)
        
        c9, c10, c11 = st.columns(3)
        status = c9.selectbox("Status", ["Planning", "Execution", "WCC Done", "Closed"])
        t_name = c10.text_input("Assigned Team")
        t_bill = c11.number_input("Team Billing (₹)", min_value=0.0)

        st.divider()
        st.markdown("### 💳 Client Billing (WCC)")
        c12, c13, c14 = st.columns(3)
        w_no = c12.text_input("WCC No.")
        w_amt = c13.number_input("WCC Amt (₹)", min_value=0.0)
        r_amt = c14.number_input("Received Amt (₹)", min_value=0.0)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("🚀 SUBMIT SITE LOG"):
            if not s_id:
                st.error("Site ID missing!")
            else:
                data = {
                    "project_id": p_id, "site_id": s_id, "site_name": s_name,
                    "cluster": cluster, "work_description": work_desc, "project_amt": p_amt,
                    "po_no": po_no, "po_amt": po_amt, "site_status": status,
                    "team_name": t_name, "team_billing": t_bill, "team_paid_amt": 0,
                    "wcc_no": w_no, "wcc_amt": w_amt, "received_amt": r_amt
                }
                supabase.table("site_data").insert(data).execute()
                st.success("Entry Saved Successfully!")

# --- 7. FINANCE PAGE ---
elif page == "💸 Financial Control Center":
    st.markdown("<h1>💰 Finance Control</h1>", unsafe_allow_html=True)
    
    with st.form("finance_form"):
        f1, f2, f3 = st.columns(3)
        payer = f1.text_input("From")
        payee = f2.text_input("To")
        fdate = f3.date_input("Date")
        
        f4, f5 = st.columns(2)
        ramt = f4.number_input("Received Amount (₹)", min_value=0.0)
        pamt = f5.number_input("Paid Amount (₹)", min_value=0.0)
        
        if st.form_submit_button("📝 LOG TRANSACTION"):
            f_log = {"received_from": payer, "paid_to": payee, "transaction_date": str(fdate), "received_amt": ramt, "paid_amount": pamt}
            supabase.table("finance").insert(f_log).execute()
            st.success("Logged.")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026 • Elegant Operations Portal</div>", unsafe_allow_html=True)
