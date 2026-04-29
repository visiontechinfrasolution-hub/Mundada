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
def format_date_df(df):
    """Sabh tables mein date ko strictly 29-Apr-2026 format mein convert karta hai"""
    date_cols = ['transaction_date', 'created_at', 'Date', 'date']
    for col in df.columns:
        if any(d in col.lower() for d in date_cols):
            try:
                df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%Y')
            except:
                pass
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

# --- 5. DASHBOARD & MASTER REG (SAME AS BEFORE) ---
# ... (Dashboard aur Master Reg ka code logic same rakha gaya hai)

# --- 7. SITE DATA ENTRY (BLANK AMOUNTS) ---
if page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    c_res = supabase.table("client_master").select("client_name").execute()
    clients = [c['client_name'] for c in c_res.data] if c_res.data else []

    with st.form("s_f", clear_on_submit=True):
        r1_1, r1_2, r1_3 = st.columns(3)
        p_id, s_id, cl = r1_1.text_input("Project ID"), r1_2.text_input("Site ID"), r1_3.selectbox("Client", ["Select"]+clients)
        
        r2_1, r2_2, r2_3 = st.columns(3)
        p_amt = r2_1.number_input("Project Amt", value=None) # Blank
        po_no = r2_2.text_input("PO No")
        po_amt = r2_3.number_input("PO Amt", value=None) # Blank
        
        if st.form_submit_button("🚀 SYNC DATA"):
            if s_id and cl != "Select":
                data = {"project_id": p_id, "site_id": s_id, "site_name": cl, "project_amt": p_amt or 0, "po_no": po_no, "po_amt": po_amt or 0}
                supabase.table("site_data").insert(data).execute()
                st.success("Site Data Logged!")

    st.divider()
    s_res = supabase.table("site_data").select("*").execute()
    if s_res.data:
        df_s = format_date_df(pd.DataFrame(s_res.data).drop(columns=['id'], errors='ignore'))
        st.dataframe(df_s, use_container_width=True)

# --- 8. FINANCE LEDGER (CONDITIONAL PROJECT ID) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    
    trans_type = st.radio("Select Transaction Type", ["Payment Received", "Payment Paid"], horizontal=True)
    
    c_res = supabase.table("client_master").select("client_name").execute()
    s_res = supabase.table("site_data").select("project_id").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    project_list = [s['project_id'] for s in s_res.data] if s_res.data else []

    if trans_type == "Payment Received":
        # Form ke bahar Selectbox taaki state change detect ho sake
        c_select = st.selectbox("Received From", ["Select Client"] + client_list + ["dilip mundada"])
        
        with st.form("received_form", clear_on_submit=True):
            r_date = st.date_input("Date", datetime.now())
            r_amt = st.number_input("Received Amt", value=None) # Blank field
            
            # CONDITION: Agar Indus Towers select hai tabhi Project ID dikhao
            proj_id = None
            if "indus tower" in c_select.lower():
                proj_id = st.selectbox("Select Project ID", ["Select Project ID"] + project_list)
            
            if st.form_submit_button("Submit Received Payment"):
                if c_select == "Select Client":
                    st.error("Pehle Client select karein.")
                else:
                    amt_to_save = r_amt or 0
                    # 1. Finance Entry
                    supabase.table("finance").insert({
                        "received_from": c_select, 
                        "transaction_date": str(r_date), 
                        "received_amt": amt_to_save, 
                        "paid_amount": 0
                    }).execute()

                    # 2. Site Data Update (Only for Indus Towers)
                    if proj_id and proj_id != "Select Project ID":
                        curr = supabase.table("site_data").select("received_amt").eq("project_id", proj_id).execute()
                        if curr.data:
                            new_total = float(curr.data[0]['received_amt'] or 0) + amt_to_save
                            supabase.table("site_data").update({"received_amt": new_total}).eq("project_id", proj_id).execute()
                            st.success(f"Amount updated in Project: {proj_id}")

                    st.success(f"Payment saved for {c_select} on {r_date.strftime('%d-%b-%Y')}")

    # --- Transaction Ledger Table ---
    st.divider()
    st.subheader("💰 Transaction History")
    f_res = supabase.table("finance").select("*").order('transaction_date', desc=True).execute()
    if f_res.data:
        df_f = format_date_df(pd.DataFrame(f_res.data).drop(columns=['id'], errors='ignore'))
        
        search = st.text_input("🔍 Search History")
        if search:
            df_f = df_f[df_f.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.dataframe(df_f, use_container_width=True)
        st.download_button("📥 Export Excel", data=to_excel(df_f), file_name=f"Ledger_{datetime.now().strftime('%d-%b-%Y')}.xlsx")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
