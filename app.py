import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); }
    h1 { font-weight: 800; color: #0984e3; }
    div.stForm { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 8px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPER ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5 & 6. UNTOUCHED SECTIONS ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    # Same as previous version...

elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    # Same as previous version...

# --- 7. SITE DATA ENTRY (FINAL FIX) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    
    if st.button("➕ Add New Site Entry"):
        st.session_state.show_form = not st.session_state.get('show_form', False)

    if st.session_state.get('show_form', False):
        with st.form("site_complete_form", clear_on_submit=True):
            st.subheader("Enter All Site Details")
            c1, c2, c3 = st.columns(3)
            p_id = c1.text_input("Project ID (Unique)*")
            s_id = c2.text_input("Site ID")
            s_nm = c3.text_input("Site Name")
            
            c4, c5, c6 = st.columns(3)
            cluster = c4.text_input("Cluster")
            p_amt = c5.number_input("Project Amount", value=None)
            status = c6.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])

            c7, c8, c9 = st.columns(3)
            po_n, po_a = c7.text_input("PO Number"), c8.number_input("PO Amount", value=None)
            w_desc = c9.text_area("Work Description", height=65)

            c10, c11, c12 = st.columns(3)
            t_name = c10.text_input("Team Name")
            t_bill = c11.number_input("Team Billing", value=None)
            t_paid = c12.number_input("Team Paid Amount", value=None)

            c13, c14, c15 = st.columns(3)
            wcc_n = c13.text_input("WCC Number")
            wcc_a = c14.number_input("WCC Amount", value=None)
            r_amt = c15.number_input("Received Amount", value=None)

            if st.form_submit_button("🚀 Save Site"):
                check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
                if check.data:
                    st.error(f"Remark: Project ID '{p_id}' already available!")
                elif p_id:
                    data = {
                        "project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, 
                        "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, 
                        "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, 
                        "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0,
                        "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0
                    }
                    supabase.table("site_data").insert(data).execute()
                    st.success("Site Added!")
                    st.rerun()

    st.divider()

    # COMPACT BAR: Upload, Download, Search
    b1, b2, b3, b4 = st.columns([1, 0.6, 0.6, 2])
    with b1: up_file = st.file_uploader("Upload", type=['xlsx'], label_visibility="collapsed")
    with b2:
        if up_file and st.button("✅ Sync"):
            up_df = pd.read_excel(up_file).fillna(0)
            existing = [x['project_id'] for x in supabase.table("site_data").select("project_id").execute().data]
            to_add, dups = [], []
            for _, row in up_df.iterrows():
                row_dict = row.to_dict()
                if str(row_dict.get('project_id')) in existing: dups.append(str(row_dict.get('project_id')))
                else: to_add.append(row_dict)
            if to_add: supabase.table("site_data").insert(to_add).execute()
            if dups: st.warning(f"Duplicates: {', '.join(dups)}")
            st.success(f"Added {len(to_add)} records."); st.rerun()
    
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    # Calculate Team Balance
    if not df.empty:
        df['team_balance'] = df['team_billing'].astype(float) - df['team_paid_amt'].astype(float)

    with b3:
        if not df.empty: st.download_button("📥 Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    with b4: search = st.text_input("🔍 Search Database...", placeholder="Search Site, Team, Project ID...")

    # DATA TABLE (ALL COLUMNS + EDITABLE)
    if not df.empty:
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        # Display Columns in order
        all_cols = ["project_id", "site_id", "site_name", "cluster", "work_description", "project_amt", 
                    "po_no", "po_amt", "site_status", "team_name", "team_billing", "team_paid_amt", 
                    "team_balance", "wcc_no", "wcc_amt", "received_amt"]
        
        st.subheader("Live Database (Double-click to Edit any row)")
        
        # Action Buttons for the Table
        edited_df = st.data_editor(
            df, 
            column_order=all_cols,
            column_config={
                "id": None, # Hide ID
                "project_id": st.column_config.TextColumn("Project ID", required=True),
                "team_balance": st.column_config.NumberColumn("Team Balance", disabled=True)
            },
            use_container_width=True,
            num_rows="dynamic", # Enables Add/Delete rows
            key="site_editor_final"
        )

        if st.button("💾 Save All Table Changes"):
            for _, row in edited_df.iterrows():
                if 'id' in row:
                    data_to_sync = row.to_dict()
                    if 'team_balance' in data_to_sync: del data_to_sync['team_balance'] # Don't sync calculated col
                    supabase.table("site_data").update(data_to_sync).eq('id', row['id']).execute()
            st.success("Cloud Sync Complete!")

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Untouched logic...
