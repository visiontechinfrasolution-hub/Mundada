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
def format_date_df(df, date_col):
    """Dataframe ki date column ko 29-Apr-2026 format mein badalta hai"""
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%d-%b-%Y')
    return df

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.divider()
    # Sidebar mein bhi formatted date dikhayenge
    st.info(f"User: Mayur Patil\n\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        res = supabase.table("site_data").select("po_amt, received_amt, team_billing, team_paid_amt, wcc_amt").execute()
        if res.data:
            df = pd.DataFrame(res.data)
            st.markdown("### 📍 Project Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", f"{len(df)}")
            c2.metric("Total PO Amt", f"₹ {df['po_amt'].sum():,.0f}")
            st.divider()
            st.markdown("### 👥 Team & Vendor Status")
            c2_1, c2_2, c2_3 = st.columns(3)
            c2_1.metric("Total Team Billing", f"₹ {df['team_billing'].sum():,.0f}")
            c2_2.metric("Total Team Paid", f"₹ {df['team_paid_amt'].sum():,.0f}")
            c2_3.metric("Total Team Balance", f"₹ {(df['team_billing'].sum() - df['team_paid_amt'].sum()):,.0f}", delta_color="inverse")
            st.divider()
            st.markdown("### 💳 Client Recovery (WCC)")
            c3_1, c3_2, c3_3 = st.columns(3)
            c3_1.metric("Total WCC Amt", f"₹ {df['wcc_amt'].sum():,.0f}")
            c3_2.metric("Total Received Amt", f"₹ {df['received_amt'].sum():,.0f}")
            c3_3.metric("Total Balance", f"₹ {(df['wcc_amt'].sum() - df['received_amt'].sum()):,.0f}")
    except Exception as e: st.error(f"Error: {e}")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with t1:
        with st.form("c_f"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save"):
                supabase.table("client_master").insert({"client_name": cn}).execute()
                st.success("Saved")
        res_c = supabase.table("client_master").select("*").execute()
        if res_c.data:
            df_c = pd.DataFrame(res_c.data).drop(columns=['id'], errors='ignore')
            st.dataframe(df_c, use_container_width=True)

    with t2:
        with st.form("t_f"):
            tn = st.text_input("Team Name")
            if st.form_submit_button("Save"):
                supabase.table("team_master").insert({"team_name": tn}).execute()
                st.success("Saved")
        res_t = supabase.table("team_master").select("*").execute()
        if res_t.data:
            df_t = pd.DataFrame(res_t.data).drop(columns=['id'], errors='ignore')
            st.dataframe(df_t, use_container_width=True)

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    c_res = supabase.table("client_master").select("client_name").execute()
    t_res = supabase.table("team_master").select("team_name").execute()
    clients = [c['client_name'] for c in c_res.data] if c_res.data else []
    teams = [t['team_name'] for t in t_res.data] if t_res.data else []

    with st.form("s_f", clear_on_submit=True):
        r1, r2, r3 = st.columns(3)
        p_id, s_id, cl = r1.text_input("Project ID"), r2.text_input("Site ID"), r3.selectbox("Client", ["Select"]+clients)
        # ... Other fields same as before ...
        if st.form_submit_button("SYNC DATA"):
            # Insert logic same as before
            st.success("Synced")
    
    st.divider()
    s_res = supabase.table("site_data").select("*").execute()
    if s_res.data:
        df_s = pd.DataFrame(s_res.data).drop(columns=['id'], errors='ignore')
        # Created_at ko format karenge
        df_s = format_date_df(df_s, 'created_at')
        st.dataframe(df_s, use_container_width=True)

# --- 8. FINANCE LEDGER (WITH 29-Apr-2026 FORMAT) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    
    trans_type = st.radio("Select Transaction Type", ["Payment Received", "Payment Paid"], horizontal=True)
    
    c_res = supabase.table("client_master").select("client_name").execute()
    s_res = supabase.table("site_data").select("project_id").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    project_list = [s['project_id'] for s in s_res.data] if s_res.data else []

    if trans_type == "Payment Received":
        with st.form("received_form", clear_on_submit=True):
            st.subheader("💰 Record Payment Received")
            c_select = st.selectbox("Received From", ["Select Client"] + client_list + ["dilip mundada"])
            r_date = st.date_input("Date", datetime.now())
            r_amt = st.number_input("Received Amt", min_value=0.0)
            
            proj_id = None
            if c_select != "dilip mundada" and c_select != "Select Client":
                proj_id = st.selectbox("Select Project ID", ["Select Project ID"] + project_list)

            if st.form_submit_button("Submit Received Payment"):
                # Finance Entry
                fin_data = {"received_from": c_select, "transaction_date": str(r_date), "received_amt": r_amt, "paid_amount": 0, "paid_to": "Internal"}
                supabase.table("finance").insert(fin_data).execute()

                # Site Data Update
                if proj_id and proj_id != "Select Project ID" and c_select != "dilip mundada":
                    curr = supabase.table("site_data").select("received_amt").eq("project_id", proj_id).execute()
                    if curr.data:
                        new_val = float(curr.data[0]['received_amt'] or 0) + r_amt
                        supabase.table("site_data").update({"received_amt": new_val}).eq("project_id", proj_id).execute()
                st.success(f"Logged on {r_date.strftime('%d-%b-%Y')}")

    # --- Ledger Table with Formatted Date ---
    st.divider()
    st.subheader("💰 Transaction History")
    f_res = supabase.table("finance").select("*").order('transaction_date', desc=True).execute()
    if f_res.data:
        df_f = pd.DataFrame(f_res.data).drop(columns=['id'], errors='ignore')
        # Transaction Date ko format kar rahe hain
        df_f = format_date_df(df_f, 'transaction_date')
        
        search = st.text_input("🔍 Search History")
        if search:
            df_f = df_f[df_f.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.dataframe(df_f, use_container_width=True)
        st.download_button("📥 Export Formatted Ledger", data=to_excel(df_f), file_name=f"Ledger_{datetime.now().strftime('%d-%b-%Y')}.xlsx")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
