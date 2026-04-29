import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & CLEAN UI ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #ffffff; color: #1e293b; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    [data-testid="stMetricValue"] > div { color: #0f172a !important; font-weight: 800; }
    div.stForm { background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; border: none; padding: 10px 25px; }
    .stButton>button:hover { background: linear-gradient(135deg, #0ea5e9 0%, #2dd4bf 100%); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPERS ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def format_df_dates(df):
    date_cols = ['transaction_date', 'created_at', 'Date', 'date']
    for col in df.columns:
        if any(d in col.lower() for d in date_cols) and col in df.columns:
            try: df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%Y')
            except: pass
    return df

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5 & 6. DASHBOARD & REGISTRATION (STABLE - NO CHANGE) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        if s_res.data:
            df_s, df_f = pd.DataFrame(s_res.data), (pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame())
            st.markdown("### 📍 Project Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            st.divider()
            st.markdown("### 👥 Team & WCC Recovery")
            c3_1, c3_2, c3_3 = st.columns(3)
            c3_1.metric("Total Team Billing", f"₹ {df_s['team_billing'].sum():,.0f}")
            c3_2.metric("Total WCC Amt", f"₹ {df_s['wcc_amt'].sum():,.0f}")
            c3_3.metric("Total Received Amt", f"₹ {df_s['received_amt'].sum():,.0f}")
    except: pass

elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("client_master_form", clear_on_submit=True):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
    with tab2:
        with st.form("team_master_form", clear_on_submit=True):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY (100% COLUMNS MAPPED) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Operational Registry</h1>", unsafe_allow_html=True)
    
    if st.button("➕ Add New Site Entry (Full Columns)"):
        st.session_state.show_form = not st.session_state.get('show_form', False)

    if st.session_state.get('show_form', False):
        with st.form("site_100_percent_form", clear_on_submit=True):
            st.subheader("Complete Site Data Entry")
            # All 15+ potential columns mapped
            r1c1, r1c2, r1c3 = st.columns(3)
            p_id = r1c1.text_input("Project ID (Unique)*")
            s_id = r1c2.text_input("Site ID")
            s_nm = r1c3.text_input("Site Name")
            
            r2c1, r2c2, r2c3 = st.columns(3)
            cluster = r2c1.text_input("Cluster")
            p_amt = r2c2.number_input("Project Amount", value=None)
            status = r2c3.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])

            r3c1, r3c2, r3c3 = st.columns(3)
            po_n, po_a = r3c1.text_input("PO Number"), r3c2.number_input("PO Amount", value=None)
            w_desc = r3c3.text_area("Work Description", height=65)

            r4c1, r4c2, r4c3 = st.columns(3)
            t_name = r4c1.text_input("Team Name")
            t_bill = r4c2.number_input("Team Billing", value=None)
            t_paid = r4c3.number_input("Team Paid Amount", value=None)

            r5c1, r5c2, r5c3 = st.columns(3)
            wcc_n = r5c1.text_input("WCC Number")
            wcc_a = r5c2.number_input("WCC Amount", value=None)
            r_amt = r5c3.number_input("Received Amount", value=None)

            if st.form_submit_button("🚀 Save Full Entry"):
                # Duplicate Check Logic
                check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
                if check.data:
                    st.error(f"Remark: Project ID '{p_id}' already available in system.")
                elif p_id:
                    data = {
                        "project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, 
                        "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, 
                        "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, 
                        "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0,
                        "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0
                    }
                    supabase.table("site_data").insert(data).execute()
                    st.success("New site data synced successfully!")
                    st.rerun()

    st.divider()
    # Compact Bar: Upload, Download, Search
    b1, b2, b3, b4 = st.columns([1, 0.6, 0.6, 2])
    with b1: up_file = st.file_uploader("Upload", type=['xlsx'], label_visibility="collapsed")
    with b2:
        if up_file and st.button("✅ Sync"):
            up_df = pd.read_excel(up_file).fillna(0)
            existing = [x['project_id'] for x in supabase.table("site_data").select("project_id").execute().data]
            to_add, dups = [], []
            for _, r in up_df.iterrows():
                row_dict = r.to_dict()
                if str(row_dict.get('project_id')) in existing: dups.append(str(row_dict.get('project_id')))
                else: to_add.append(row_dict)
            if to_add: supabase.table("site_data").insert(to_add).execute()
            if dups: st.warning(f"Duplicates skipped: {', '.join(dups)}")
            st.success(f"Added {len(to_add)} records."); st.rerun()
    
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    if not df.empty:
        df['team_balance'] = df['team_billing'].astype(float) - df['team_paid_amt'].astype(float)

    with b3:
        if not df.empty: st.download_button("📥 Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    with b4: search = st.text_input("🔍 Search Database...")

    if not df.empty:
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        # Displaying 100% columns in Table
        st.subheader("Live Database (Edit Directly)")
        edited_df = st.data_editor(
            df, 
            column_order=["project_id", "site_id", "site_name", "cluster", "project_amt", "po_no", "po_amt", "site_status", "team_name", "team_billing", "team_paid_amt", "team_balance", "wcc_no", "wcc_amt", "received_amt", "work_description"],
            column_config={"id": None, "team_balance": st.column_config.NumberColumn("Team Balance", disabled=True)},
            use_container_width=True,
            num_rows="dynamic",
            key="site_editor_100"
        )
        if st.button("💾 Save Table Edits"):
            for _, row in edited_df.iterrows():
                if 'id' in row:
                    d = row.to_dict(); d.pop('team_balance', None)
                    supabase.table("site_data").update(d).eq('id', row['id']).execute()
            st.success("All changes synced to cloud!")

# --- 8. FINANCE LEDGER (STABLE - NO CHANGE) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # ... Finance Logic (Same as before)
