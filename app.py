import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. SUPERIOR PAGE CONFIG ---
st.set_page_config(
    page_title="Visiontech Mundada | Lavish HD Portal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE LAVISH & HD UI STYLE (ULTRA-CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    /* Global Overrides */
    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Background & Glass Effect */
    .stApp {
        background: radial-gradient(circle at top right, #394457 0%, #1e2633 100%);
        color: #e6e9ef;
    }

    /* Header Styling */
    h1 {
        font-weight: 800;
        letter-spacing: -2px;
        color: #ffffff;
        margin-bottom: 0px;
    }
    h2, h3 {
        color: #e6e9ef;
        font-weight: 600;
    }

    /* Professional Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #121620 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stSidebarNav"] {
        padding-top: 2rem;
    }
    .st-emotion-cache-16idsys p {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 16px;
    }
    /* Sidebar Item Hover */
    [data-testid="stSidebarNavItem"] {
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebarNavItem"]:hover {
        background-color: rgba(0, 123, 255, 0.1) !important;
    }

    /* Lavish Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 123, 255, 0.2);
        border-color: rgba(0, 123, 255, 0.3);
    }
    [data-testid="stMetricValue"] > div {
        color: #00d4ff !important;
        font-weight: 800;
    }

    /* Glassmorphism Forms */
    div.stForm {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 50px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        margin-top: 20px;
    }

    /* Input Fields styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 12px 15px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
    }

    /* Glowing Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #007bff 0%, #00d4ff 100%);
        color: white;
        border: none;
        padding: 18px;
        border-radius: 15px;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 1px;
        transition: all 0.4s ease;
        box-shadow: 0 5px 20px rgba(0, 123, 255, 0.4);
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00d4ff 0%, #007bff 100%);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 123, 255, 0.6);
    }
    
    /* Footer */
    .lavish-footer {
        text-align: center;
        padding: 40px;
        color: rgba(255, 255, 255, 0.3);
        font-size: 14px;
        letter-spacing: 1px;
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
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 20px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #00d4ff; font-weight: 600; margin-bottom: 30px;'>PROJECT PORTAL</div>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation", ["Overview Dashboard", "Project Site Registry", "Financial Control Center"])
    st.divider()
    st.caption("Developed by Visiontech Automation • v2.0")

# --- 5. DASHBOARD PAGE (LAVISH METRICS) ---
if page == "Overview Dashboard":
    st.markdown("<h1>📈 Project Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: rgba(255, 255, 255, 0.6); font-size: 18px; margin-bottom: 30px;'>Real-time analytical breakdown of Mundada operations.</p>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Sites", "12", "+2")
    m2.metric("Total PO Value", "₹ 45.2L", "8 Sites")
    m3.metric("Collection (WCC)", "₹ 28.5L", "63%")
    m4.metric("Vendor Payable", "₹ 4.1L", "WCC Done")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Placeholder Chart
    st.subheader("Performance Snapshot")
    chart_data = pd.DataFrame({'WCC Submission': [10, 25, 45, 30, 60], 'Payments Received': [8, 20, 38, 28, 55]})
    st.area_chart(chart_data)

# --- 6. SITE DATA PAGE (LAVISH FORM) ---
elif page == "Project Site Registry":
    st.markdown("<h1>🏗️ Site & Operational Data</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: rgba(255, 255, 255, 0.6); font-size: 18px; margin-bottom: 30px;'>Logistics and project execution tracking entry.</p>", unsafe_allow_html=True)
    
    with st.form("lavish_registry_form", clear_on_submit=True):
        
        st.markdown("<h3>📍 Basic Details & Scope</h3>", unsafe_allow_html=True)
        r1c1, r1c2, r1c3 = st.columns(3)
        p_id = r1c1.text_input("Project ID", placeholder="PRJ-2026-X")
        s_id = r1c2.text_input("Site ID", placeholder="UNIQUE SITE CODE")
        s_name = r1c3.text_input("Site Name", placeholder="Location Name")
        
        r2c1, r2c2 = st.columns([1, 2])
        cluster = r2c1.text_input("Cluster", placeholder="Region")
        work_desc = r2c2.text_area("Work Description", placeholder="Detailed breakdown of scope...", height=70)
        
        st.divider()
        
        st.markdown("<h3>📑 PO & Team Assignment</h3>", unsafe_allow_html=True)
        r3c1, r3c2, r3c3 = st.columns(3)
        p_amt = r3c1.number_input("Project Amount (₹)", min_value=0.0, step=1000.0)
        po_no = r3c2.text_input("PO Number")
        po_amt = r3c3.number_input("PO Amount (₹)", min_value=0.0, step=1000.0)
        
        r4c1, r4c2, r4c3 = st.columns(3)
        status = r4c1.selectbox("Site Status", ["Planning", "Material Dispatch", "Work in Progress", "WCC Process", "Completed", "Closed"])
        t_name = r4c2.text_input("Team/Vendor Name")
        t_bill = r4c3.number_input("Team Billing (₹)", min_value=0.0, step=1000.0)
        # PaidAmt defaults to 0 on new entry

        st.divider()
        
        st.markdown("<h3>💳 Client Billing (WCC)</h3>", unsafe_allow_html=True)
        r5c1, r5c2, r5c3 = st.columns(3)
        wcc_no = r5c1.text_input("WCC Number")
        wcc_amt = r5c2.number_input("WCC Value (₹)", min_value=0.0, step=1000.0)
        rec_amt = r5c3.number_input("Amount Received (₹)", min_value=0.0, step=1000.0)

        st.markdown("<br><br>", unsafe_allow_html=True)
        # Premium Submit Button
        submitted = st.form_submit_button("🚀 SYNC DATA TO SECURE CLOUD")
        
        if submitted:
            if not s_id:
                st.error("❌ Mandatory Field: Site ID is required for cloud synchronization.")
            else:
                entry_data = {
                    "project_id": p_id, "site_id": s_id, "site_name": s_name,
                    "cluster": cluster, "work_description": work_desc, "project_amt": p_amt,
                    "po_no": po_no, "po_amt": po_amt, "site_status": status,
                    "team_name": t_name, "team_billing": t_bill, "team_paid_amt": 0,
                    "wcc_no": wcc_no, "wcc_amt": wcc_amt, "received_amt": rec_amt
                }
                try:
                    supabase.table("site_data").insert(entry_data).execute()
                    st.balloons()
                    st.success(f"✅ EXCLUSIVE SITE LOG: {s_id} successfully recorded in Mundada Portal.")
                except Exception as e:
                    st.error(f"❌ Cloud Sync Failed: {e}")

# --- 7. FINANCE CONTROL ---
elif page == "Financial Control Center":
    st.markdown("<h1>💸 Central Financial Ledger</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: rgba(255, 255, 255, 0.6); font-size: 18px; margin-bottom: 30px;'>Cash Flow Monitoring (Incoming & Outgoing Transactions)</p>", unsafe_allow_html=True)
    
    with st.form("lavish_finance_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        payer = f1.text_input("Payer Entity")
        payee = f2.text_input("Payee Entity")
        f_date = f3.date_input("Transaction Date", datetime.now())
        
        st.divider()
        
        f4, f5 = st.columns(2)
        r_amt = f4.number_input("Amount Received (+ ₹)", min_value=0.0, step=1000.0)
        p_amt = f5.number_input("Amount Paid (- ₹)", min_value=0.0, step=1000.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("📝 COMMIT ENTRY TO LEDGER"):
            fin_log = {
                "received_from": payer,
                "paid_to": payee,
                "transaction_date": str(f_date),
                "received_amt": r_amt,
                "paid_amount": p_amt
            }
            try:
                supabase.table("finance").insert(fin_log).execute()
                st.success("✅ Financial transaction logged successfully.")
            except Exception as e:
                st.error(f"❌ Error logging transaction: {e}")

# --- FOOTER ---
st.markdown("""
    <div class="lavish-footer">
        Visiontech Automation © 2026 • Mundada Exclusive HD Portal • Confidential
    </div>
    """, unsafe_allow_html=True)
