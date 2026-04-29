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
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #2d3436; }
    h1 { font-weight: 800; letter-spacing: -1.5px; color: #0984e3; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 20px; padding: 25px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); }
    .stButton>button { background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%); color: white; border-radius: 12px; font-weight: 700; width: 100%; border: none; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

@st.cache_resource
def get_supabase():
    return create_client(URL, KEY)

supabase = get_supabase()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", [
        "🏠 Overview Dashboard", 
        "📝 Master Registration", 
        "🏗️ Project Site Registry", 
        "💸 Financial Control Center"
    ])
    st.divider()
    st.info("User: Mayur Patil")

# --- 5. DASHBOARD ---
if page == "🏠 Overview Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Sites", "12")
    m2.metric("Collection", "₹ 28.5L")
    st.subheader("Recent Analytics")
    st.line_chart(pd.DataFrame({'Target': [10, 25, 45], 'Actual': [8, 22, 40]}))

# --- 6. MASTER REGISTRATION (CLIENT & TEAM) ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registration</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Client Registration", "🛠️ Team Registration"])
    
    with tab1:
        with st.form("client_form", clear_on_submit=True):
            st.subheader("Register New Client")
            c_name = st.text_input("Client Name")
            col1, col2 = st.columns(2)
            c_person = col1.text_input("Contact Person")
            c_phone = col2.text_input("Phone Number")
            if st.form_submit_button("Save Client"):
                if c_name:
                    supabase.table("client_master").insert({"client_name": c_name, "contact_person": c_person, "contact_number": c_phone}).execute()
                    st.success(f"Client {c_name} Added!")

    with tab2:
        with st.form("team_form", clear_on_submit=True):
            st.subheader("Register New Team")
            t_name = st.text_input("Team Name")
            col1, col2 = st.columns(2)
            t_leader = col1.text_input("Team Leader")
            t_phone = col2.text_input("Leader Phone")
            if st.form_submit_button("Save Team"):
                if t_name:
                    supabase.table("team_master").insert({"team_name": t_name, "leader_name": t_leader, "leader_contact": t_phone}).execute()
                    st.success(f"Team {t_name} Added!")

# --- 7. SITE REGISTRY ---
elif page == "🏗️ Project Site Registry":
    st.markdown("<h1>📝 Site Registration</h1>", unsafe_allow_html=True)
    
    # Fetching Clients and Teams for Dropdowns
    clients = supabase.table("client_master").select("client_name").execute()
    teams = supabase.table("team_master").select("team_name").execute()
    
    client_list = [c['client_name'] for c in clients.data] if clients.data else ["No Clients Registered"]
    team_list = [t['team_name'] for t in teams.data] if teams.data else ["No Teams Registered"]

    with st.form("site_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        p_id = c1.text_input("Project ID")
        s_id = c2.text_input("Site ID")
        # Client Name Dropdown
        client_selected = c3.selectbox("Client Name", client_list)
        
        c4, c5 = st.columns([1, 2])
        cluster = c4.text_input("Cluster")
        work_desc = c5.text_area("Work Description", height=70)
        
        st.divider()
        c6, c7, c8 = st.columns(3)
        p_amt = c6.number_input("Project Amt", min_value=0.0)
        po_no = c7.text_input("PO Number")
        # Team Name Dropdown
        team_selected = c8.selectbox("Assigned Team", team_list)
        
        if st.form_submit_button("Submit Site Data"):
            data = {"project_id": p_id, "site_id": s_id, "site_name": client_selected, "cluster": cluster, "team_name": team_selected, "project_amt": p_amt, "po_no": po_no}
            supabase.table("site_data").insert(data).execute()
            st.success("Site Data Logged!")

# --- 8. FINANCE PAGE ---
elif page == "💸 Financial Control Center":
    st.markdown("<h1>💰 Finance Control</h1>", unsafe_allow_html=True)
    with st.form("finance_form"):
        f1, f2, f3 = st.columns(3)
        if st.form_submit_button("Record Transaction"):
            st.info("Transaction feature ready.")

st.markdown("<div style='text-align: center; color: #636e72; padding: 20px;'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
