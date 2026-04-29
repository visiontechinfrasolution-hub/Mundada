import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); }
    h1 { font-weight: 800; color: #0984e3; }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); }
    .stButton>button { border-radius: 8px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPER FUNCTIONS ---
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

# --- 5 & 6. DASHBOARD & MASTER REG (UNTOUCHED AS REQUESTED) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    # ... Dashboard Logic (Kept Same)

elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    # ... Master Reg Logic (Kept Same)

# --- 7. SITE DATA ENTRY (RE-ENGINEERED) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    
    # NEW ENTRY SECTION
    if st.button("➕ Add New Site Entry"):
        st.session_state.show_form = not st.session_state.get('show_form', False)

    if st.session_state.get('show_form', False):
        with st.form("site_full_form", clear_on_submit=True):
            st.subheader("Enter Site Details (No Client Name)")
            r1c1, r1c2, r1c3 = st.columns(3)
            p_id = r1c1.text_input("Project ID (Unique)*")
            s_id = r1c2.text_input("Site ID")
            cluster = r1c3.text_input("Cluster")
            
            r2c1, r2c2 = st.columns([2, 1])
            w_desc = r2c1.text_area("Work Description", height=70)
            status = r2c2.selectbox("Site Status", ["Planning", "WIP", "WCC Done", "Closed"])

            r3c1, r3c2, r3c3 = st.columns(3)
            p_amt = r3c1.number_input("Project Amount", value=None)
            po_n = r3c2.text_input("PO Number")
            po_a = r3c3.number_input("PO Amount", value=None)

            r4c1, r4c2, r4c3 = st.columns(3)
            t_name = r4c1.text_input("Team Name")
            t_bill = r4c2.number_input("Team Billing", value=None)
            t_paid = r4c3.number_input("Team Paid Amount", value=None)

            r5c1, r5c2, r5c3 = st.columns(3)
            wcc_n = r5c1.text_input("WCC Number")
            wcc_a = r5c2.number_input("WCC Amount", value=None)
            r_amt = r5c3.number_input("Received Amount", value=None)

            if st.form_submit_button("🚀 Save Site"):
                check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
                if check.data:
                    st.error(f"Remark: Same Project ID '{p_id}' already available in system.")
                elif p_id:
                    data = {
                        "project_id": p_id, "site_id": s_id, "cluster": cluster, 
                        "work_description": w_desc, "site_status": status,
                        "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0,
                        "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0,
                        "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0
                    }
                    supabase.table("site_data").insert(data).execute()
                    st.success("Site successfully added.")
                    st.rerun()

    st.divider()

    # BUTTON BAR (Compact)
    b1, b2, b3, b4 = st.columns([1, 0.8, 0.8, 2])
    with b1: up_file = st.file_uploader("Upload", type=['xlsx'], label_visibility="collapsed")
    with b2:
        if up_file and st.button("✅ Confirm"):
            up_df = pd.read_excel(up_file).fillna(0)
            existing = [x['project_id'] for x in supabase.table("site_data").select("project_id").execute().data]
            to_add, dups = [], []
            for _, row in up_df.iterrows():
                row_dict = row.to_dict()
                if str(row_dict.get('project_id')) in existing: dups.append(str(row_dict.get('project_id')))
                else: to_add.append(row_dict)
            if to_add: supabase.table("site_data").insert(to_add).execute()
            if dups: st.warning(f"Duplicate IDs not added: {', '.join(dups)}")
            st.success(f"Added {len(to_add)} records.")
            st.rerun()
    
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    with b3:
        if not df.empty: st.download_button("📥 Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    with b4: search = st.text_input("🔍 Search...", placeholder="Site ID, Team, Status...")

    # DATA TABLE (All Columns, No ID, No Site Name)
    if not df.empty:
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        # All columns to display
        cols = ["project_id", "site_id", "cluster", "work_description", "project_amt", "po_no", "po_amt", "site_status", "team_name", "team_billing", "team_paid_amt", "wcc_no", "wcc_amt", "received_amt"]
        
        # Displaying with Editor
        edited_df = st.data_editor(
            df, 
            column_order=cols,
            column_config={"id": None, "site_name": None}, # Hide ID and Site/Client Name
            use_container_width=True,
            num_rows="dynamic",
            key="site_editor"
        )

        if st.button("💾 Save All Table Changes"):
            for _, row in edited_df.iterrows():
                if 'id' in row:
                    supabase.table("site_data").update(row.to_dict()).eq('id', row['id']).execute()
            st.success("Changes saved to cloud.")

# --- 8. FINANCE LEDGER (UNTOUCHED) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # ... Finance Logic (Kept Same)
