import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="Visiontech Mundada | HD Portal",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LAVISH CUSTOM CSS (HD STYLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Font & Background */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Modern Card Design */
    div[data-testid="stVerticalBlock"] > div:has(div.stForm) {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Metric Styling */
    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #007bff;
    }

    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #007bff 0%, #00d4ff 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,123,255,0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,123,255,0.4);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e1e2f;
        color: white;
    }
    
    /* Header Text */
    h1, h2, h3 {
        color: #1e1e2f;
        font-weight: 800;
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

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: white; text-align: center;'>VIS MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("Menu", ["🏠 Dashboard", "🏗️ Site Registry", "💸 Finance Control"])
    st.divider()
    st.caption("Developed for Visiontech Infra Solutions")

# --- 5. DASHBOARD (HD METRICS) ---
if page == "🏠 Dashboard":
    st.markdown("# 📈 Mundada Overview")
    st.write("Real-time project analytics and financial status.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Sites", "12", "+2")
    m2.metric("Total PO Value", "₹ 45.2L")
    m3.metric("Collection", "₹ 28.5L", "63%")
    m4.metric("Team Payable", "₹ 4.1L", "-12%")
    
    st.divider()
    # Placeholder for a Chart
    st.subheader("Monthly Progress")
    chart_data = pd.DataFrame({'Site Progress': [10, 25, 45, 30, 60]})
    st.area_chart(chart_data)

# --- 6. SITE REGISTRY (LAVISH FORM) ---
elif page == "🏗️ Site Registry":
    st.markdown("# 🏗️ Project & Site Data")
    st.write("Enter site details with high-precision tracking.")
    
    with st.form("lavish_site_form", clear_on_submit=True):
        st.markdown("### 📍 Location & Scope")
        c1, c2, c3 = st.columns(3)
        p_id = c1.text_input("Project ID", placeholder="PRJ-2026-01")
        s_id = c2.text_input("Site ID", placeholder="INDUS-MH-...")
        s_name = c3.text_input("Site Name")
        
        c4, c5 = st.columns([1, 2])
        cluster = c4.text_input("Cluster")
        work_desc = c5.text_input("Work Description")
        
        st.markdown("---")
        st.markdown("### 📑 Commercials & Teams")
        c6, c7, c8 = st.columns(3)
        p_amt = c6.number_input("Project Amount (₹)", min_value=0.0)
        po_no = c7.text_input("PO Number")
        po_amt = c8.number_input("PO Amount (₹)", min_value=0.0)
        
        c9, c10, c11 = st.columns(3)
        status = c9.selectbox("Status", ["Planning", "Material Dispatch", "Installation", "WCC Process", "Closed"])
        t_name = c10.text_input("Assigned Team")
        t_bill = c11.number_input("Team Billing (₹)", min_value=0.0)

        st.markdown("---")
        st.markdown("### 💳 Client Billing (WCC)")
        c12, c13, c14 = st.columns(3)
        wcc_no = c12.text_input("WCC Number")
        wcc_amt = c13.number_input("WCC Value (₹)", min_value=0.0)
        rec_amt = c14.number_input("Amount Received (₹)", min_value=0.0)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 SYNC DATA TO CLOUD")
        
        if submitted:
            if not s_id:
                st.error("Site ID is mandatory for cloud sync.")
            else:
                data = {
                    "project_id": p_id, "site_id": s_id, "site_name": s_name,
                    "cluster": cluster, "work_description": work_desc, "project_amt": p_amt,
                    "po_no": po_no, "po_amt": po_amt, "site_status": status,
                    "team_name": t_name, "team_billing": t_bill, "team_paid_amt": 0,
                    "wcc_no": wcc_no, "wcc_amt": wcc_amt, "received_amt": rec_amt
                }
                try:
                    supabase.table("site_data").insert(data).execute()
                    st.balloons()
                    st.success(f"Site {s_id} successfully registered in Mundada Portal.")
                except Exception as e:
                    st.error(f"Cloud Error: {e}")

# --- 7. FINANCE CONTROL ---
elif page == "💸 Finance Control":
    st.markdown("# 💰 Financial Ledger")
    st.write("Track every rupee moving in and out of the project.")
    
    with st.form("finance_form"):
        f1, f2, f3 = st.columns(3)
        r_from = f1.text_input("Payer Name")
        p_to = f2.text_input("Payee Name")
        date = f3.date_input("Transaction Date")
        
        f4, f5 = st.columns(2)
        ramt = f4.number_input("Amount Received (+)", min_value=0.0)
        pamt = f5.number_input("Amount Paid (-)", min_value=0.0)
        
        if st.form_submit_button("📝 LOG TRANSACTION"):
            f_data = {"received_from": r_from, "paid_to": p_to, "transaction_date": str(date), "received_amt": ramt, "paid_amount": pamt}
            supabase.table("finance").insert(f_data).execute()
            st.success("Entry added to Ledger.")

# Footer
st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666;'>
        Visiontech Automation System • Mundada Project © 2026
    </div>
    """, unsafe_allow_html=True)
