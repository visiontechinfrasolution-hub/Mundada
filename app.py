import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(
    page_title="Visiontech Mundada | Elegant Portal",
    page_icon="💎",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #2d3436; }
    h1 { font-weight: 800; color: #0984e3; margin-bottom: 10px; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 20px; padding: 25px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); }
    .stButton>button { background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%); color: white; border-radius: 12px; font-weight: 700; width: 100%; border: none; padding: 10px; }
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
def format_date_str(date_obj):
    if date_obj:
        return pd.to_datetime(date_obj).strftime('%d-%b-%Y')
    return ""

def format_df_dates(df):
    date_cols = ['transaction_date', 'created_at', 'Date']
    for col in df.columns:
        if col in date_cols or "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%Y')
            except: pass
    return df

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.divider()
    st.info(f"User: Mayur Patil\n\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        res = supabase.table("site_data").select("*").execute()
        if res.data and len(res.data) > 0:
            df = pd.DataFrame(res.data)
            
            # Line 1: Summary
            st.markdown("### 📍 Project Summary")
            c1_1, c1_2 = st.columns(2)
            c1_1.metric("Total Site Count", len(df))
            c1_2.metric("Total PO Amt", f"₹ {df['po_amt'].sum():,.2f}")
            
            # Line 2: Team Financials
            st.divider()
            st.markdown("### 👥 Team & Vendor Status")
            c2_1, c2_2, c2_3 = st.columns(3)
            t_bill = df['team_billing'].sum()
            t_paid = df['team_paid_amt'].sum()
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.2f}")
            c2_2.metric("Total Team Paid", f"₹ {t_paid:,.2f}")
            c2_3.metric("Total Team Balance", f"₹ {t_bill - t_paid:,.2f}")
            
            # Line 3: Client Financials
            st.divider()
            st.markdown("### 💳 Client Recovery (WCC)")
            c3_1, c3_2, c3_3 = st.columns(3)
            wcc_tot = df['wcc_amt'].sum()
            rec_tot = df['received_amt'].sum()
            c3_1.metric("Total WCC Amt", f"₹ {wcc_tot:,.2f}")
            c3_2.metric("Total Received Amt", f"₹ {rec_tot:,.2f}")
            c3_3.metric("Total Balance", f"₹ {wcc_tot - rec_tot:,.2f}")
        else:
            st.info("💡 Dashboard is empty because no sites are registered yet.")
    except Exception as e:
        st.error(f"Dashboard Load Error: {e}")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with t1:
        with st.form("c_f"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute()
                st.success("Client Saved")
        res_c = supabase.table("client_master").select("*").execute()
        if res_c.data:
            st.dataframe(format_df_dates(pd.DataFrame(res_c.data).drop(columns=['id'], errors='ignore')), use_container_width=True)

    with t2:
        with st.form("t_f"):
            tn = st.text_input("Team Name")
            if st.form_submit_button("Save"):
                if tn: supabase.table("team_master").insert({"team_name": tn}).execute()
                st.success("Team Saved")
        res_t = supabase.table("team_master").select("*").execute()
        if res_t.data:
            st.dataframe(format_df_dates(pd.DataFrame(res_t.data).drop(columns=['id'], errors='ignore')), use_container_width=True)

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    c_res = supabase.table("client_master").select("client_name").execute()
    clients = [c['client_name'] for c in c_res.data] if c_res.data else []

    with st.form("s_f", clear_on_submit=True):
        r1, r2, r3 = st.columns(3)
        p_id = r1.text_input("Project ID")
        s_id = r2.text_input("Site ID")
        cl = r3.selectbox("Client", ["Select"]+clients)
        
        r4, r5, r6 = st.columns(3)
        p_amt = r4.number_input("Project Amt", value=None)
        po_no = r5.text_input("PO No")
        po_amt = r6.number_input("PO Amt", value=None)
        
        if st.form_submit_button("🚀 SYNC DATA"):
            if s_id and cl != "Select":
                data = {"project_id": p_id, "site_id": s_id, "site_name": cl, "project_amt": p_amt or 0, "po_no": po_no, "po_amt": po_amt or 0}
                supabase.table("site_data").insert(data).execute()
                st.success("Site Logged Successfully")

    st.divider()
    res_s = supabase.table("site_data").select("*").execute()
    if res_s.data:
        st.dataframe(format_df_dates(pd.DataFrame(res_s.data).drop(columns=['id'], errors='ignore')), use_container_width=True)

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    
    trans_type = st.radio("Type", ["Payment Received", "Payment Paid"], horizontal=True)
    
    c_res = supabase.table("client_master").select("client_name").execute()
    s_res = supabase.table("site_data").select("project_id").execute()
    clients = [c['client_name'] for c in c_res.data] if c_res.data else []
    projects = [s['project_id'] for s in s_res.data] if s_res.data else []

    if trans_type == "Payment Received":
        c_sel = st.selectbox("Received From", ["Select"] + clients + ["dilip mundada"])
        
        with st.form("rec_f", clear_on_submit=True):
            r_dt = st.date_input("Date", datetime.now())
            r_at = st.number_input("Received Amt", value=None)
            
            p_sel = None
            if "indus tower" in c_sel.lower():
                p_sel = st.selectbox("Project ID", ["Select ID"] + projects)
            
            if st.form_submit_button("Submit"):
                if c_sel != "Select":
                    amt = r_at or 0
                    supabase.table("finance").insert({"received_from": c_sel, "transaction_date": str(r_dt), "received_amt": amt}).execute()
                    
                    if p_sel and p_sel != "Select ID":
                        curr = supabase.table("site_data").select("received_amt").eq("project_id", p_sel).execute()
                        if curr.data:
                            new_amt = float(curr.data[0]['received_amt'] or 0) + amt
                            supabase.table("site_data").update({"received_amt": new_amt}).eq("project_id", p_sel).execute()
                    st.success(f"Payment recorded on {format_date_str(r_dt)}")

    st.divider()
    f_res = supabase.table("finance").select("*").order('transaction_date', desc=True).execute()
    if f_res.data:
        df_f = format_df_dates(pd.DataFrame(f_res.data).drop(columns=['id'], errors='ignore'))
        st.dataframe(df_f, use_container_width=True)
