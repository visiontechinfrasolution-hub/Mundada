import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(
    page_title="Visiontech Mundada | Elegant Portal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #2d3436; }
    h1 { font-weight: 800; letter-spacing: -1.5px; color: #0984e3; margin-bottom: 10px; }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); }
    .stButton>button { background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%); color: white; border-radius: 12px; font-weight: 700; width: 100%; }
    .elegant-footer { text-align: center; padding: 40px; color: #636e72; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

@st.cache_resource
def get_supabase():
    return create_client(URL, KEY)

supabase = get_supabase()

# --- 3. HELPER FUNCTIONS ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])

# --- 5. DASHBOARD (OMITTED FOR BREVITY - SAME AS BEFORE) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    # ... (Dashboard code remains same as previous version)

# --- 6. MASTER REGISTRATION (OMITTED FOR BREVITY - SAME AS BEFORE) ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    # ... (Master Reg code remains same as previous version)

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    # Fetching dropdowns
    c_res = supabase.table("client_master").select("client_name").execute()
    t_res = supabase.table("team_master").select("team_name").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    team_list = [t['team_name'] for t in t_res.data] if t_res.data else []

    with st.form("site_entry_form", clear_on_submit=True):
        r1_1, r1_2, r1_3 = st.columns(3)
        p_id, s_id, client = r1_1.text_input("Project ID"), r1_2.text_input("Site ID"), r1_3.selectbox("Client Name", ["Select"] + client_list)
        # ... (Rest of site entry form fields)
        if st.form_submit_button("🚀 SYNC TO CLOUD"):
            # ... (Sync logic)
            st.success("Site Data Logged!")

# --- 8. FINANCE LEDGER (NEW CONDITIONAL LOGIC) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    
    # 1st Option: Type of Transaction
    trans_type = st.radio("Select Transaction Type", ["Payment Received", "Payment Paid"], horizontal=True)

    # Fetching Dropdowns
    c_res = supabase.table("client_master").select("client_name").execute()
    s_res = supabase.table("site_data").select("project_id").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    project_list = [s['project_id'] for s in s_res.data] if s_res.data else []

    if trans_type == "Payment Received":
        with st.form("received_form", clear_on_submit=True):
            st.subheader("💰 Record Payment Received")
            c_select = st.selectbox("Received From (Client)", ["Select Client"] + client_list + ["dilip mundada"])
            r_date = st.date_input("Date", datetime.now())
            r_amt = st.number_input("Received Amt", min_value=0.0, step=1000.0)
            
            # Condition for Project ID (Only if not dilip mundada)
            proj_id = None
            if c_select != "dilip mundada" and c_select != "Select Client":
                proj_id = st.selectbox("Select Project ID", ["Select Project ID"] + project_list)

            if st.form_submit_button("Submit Received Payment"):
                if c_select == "Select Client":
                    st.error("Please select a client.")
                else:
                    # 1. Update Finance Table
                    fin_data = {
                        "received_from": c_select,
                        "transaction_date": str(r_date),
                        "received_amt": r_amt,
                        "paid_amount": 0,
                        "paid_to": "Internal"
                    }
                    supabase.table("finance").insert(fin_data).execute()

                    # 2. Update Site Data (Only if Project ID is selected)
                    if proj_id and proj_id != "Select Project ID" and c_select != "dilip mundada":
                        # Get existing amount
                        curr_site = supabase.table("site_data").select("received_amt").eq("project_id", proj_id).execute()
                        if curr_site.data:
                            new_total = float(curr_site.data[0]['received_amt'] or 0) + r_amt
                            supabase.table("site_data").update({"received_amt": new_total}).eq("project_id", proj_id).execute()
                            st.success(f"Amount updated in Site Data for {proj_id}!")
                    
                    st.success("Transaction logged in Finance.")

    else: # Payment Paid
        with st.form("paid_form", clear_on_submit=True):
            st.subheader("💸 Record Payment Paid")
            # Logic for Payment Paid remains standard or as needed
            st.info("Payment Paid logic remains the same.")
            st.form_submit_button("Submit Paid Payment")

    # --- Ledger Table ---
    st.divider()
    st.subheader("💰 Transaction History")
    f_res = supabase.table("finance").select("*").order('transaction_date', desc=True).execute()
    if f_res.data:
        df_f = pd.DataFrame(f_res.data).drop(columns=['id'], errors='ignore')
        search = st.text_input("🔍 Search History")
        if search:
            df_f = df_f[df_f.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.dataframe(df_f, use_container_width=True)
        st.download_button("📥 Export Ledger", data=to_excel(df_f), file_name="Finance_Ledger.xlsx")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
