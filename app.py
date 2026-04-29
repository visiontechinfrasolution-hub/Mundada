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
    .stApp { background-color: #ffffff; color: #1e293b; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    div.stForm { background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; border: none; padding: 10px 25px; }
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

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5 & 6. DASHBOARD & REGISTRATION (STABLE) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    # Logic remains same...

elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    # Logic remains same...

# --- 7. SITE DATA ENTRY (HAR LINE EDIT ACTION) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Operational Registry</h1>", unsafe_allow_html=True)
    
    # Fetch Data First for Edit Logic
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    
    # EDIT LOGIC: Row selector
    selected_row = None
    if not df.empty:
        st.subheader("🛠️ Row Action")
        edit_choice = st.selectbox("Select Project ID to Edit/Update", ["None"] + df['project_id'].tolist())
        if edit_choice != "None":
            selected_row = df[df['project_id'] == edit_choice].iloc[0]

    # ENTRY / EDIT FORM
    form_label = "➕ Add New Site Entry" if selected_row is None else f"📝 Editing Project: {selected_row['project_id']}"
    
    with st.expander(form_label, expanded=(selected_row is not None)):
        with st.form("site_master_form", clear_on_submit=(selected_row is None)):
            r1c1, r1c2, r1c3 = st.columns(3)
            # Pre-fill if editing
            p_id = r1c1.text_input("Project ID (Unique)*", value=selected_row['project_id'] if selected_row is not None else "")
            s_id = r1c2.text_input("Site ID", value=selected_row['site_id'] if selected_row is not None else "")
            s_nm = r1c3.text_input("Site Name", value=selected_row['site_name'] if selected_row is not None else "")
            
            r2c1, r2c2, r2c3 = st.columns(3)
            cluster = r2c1.text_input("Cluster", value=selected_row['cluster'] if selected_row is not None else "")
            p_amt = r2c2.number_input("Project Amount", value=float(selected_row['project_amt']) if selected_row is not None else None)
            st_list = ["Planning", "WIP", "WCC Done", "Closed"]
            st_idx = st_list.index(selected_row['site_status']) if selected_row is not None and selected_row['site_status'] in st_list else 0
            status = r2c3.selectbox("Status", st_list, index=st_idx)

            r3c1, r3c2, r3c3 = st.columns(3)
            po_n = r3c1.text_input("PO Number", value=selected_row['po_no'] if selected_row is not None else "")
            po_a = r3c2.number_input("PO Amount", value=float(selected_row['po_amt']) if selected_row is not None else None)
            w_desc = r3c3.text_area("Work Description", value=selected_row['work_description'] if selected_row is not None else "")

            r4c1, r4c2, r4c3 = st.columns(3)
            t_name = r4c1.text_input("Team Name", value=selected_row['team_name'] if selected_row is not None else "")
            t_bill = r4c2.number_input("Team Billing", value=float(selected_row['team_billing']) if selected_row is not None else None)
            t_paid = r4c3.number_input("Team Paid Amount", value=float(selected_row['team_paid_amt']) if selected_row is not None else None)

            r5c1, r5c2, r5c3 = st.columns(3)
            wcc_n = r5c1.text_input("WCC Number", value=selected_row['wcc_no'] if selected_row is not None else "")
            wcc_a = r5c2.number_input("WCC Amount", value=float(selected_row['wcc_amt']) if selected_row is not None else None)
            r_amt = r5c3.number_input("Received Amount", value=float(selected_row['received_amt']) if selected_row is not None else None)

            btn_text = "🚀 Update Site Data" if selected_row is not None else "🚀 Save New Entry"
            if st.form_submit_button(btn_text):
                data = {
                    "project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, 
                    "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, 
                    "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, 
                    "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0,
                    "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0
                }
                
                if selected_row is not None:
                    supabase.table("site_data").update(data).eq('id', selected_row['id']).execute()
                    st.success("Changes updated successfully!")
                else:
                    # Duplicate check for new entries
                    check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
                    if check.data:
                        st.error(f"Remark: Project ID '{p_id}' already available!")
                    else:
                        supabase.table("site_data").insert(data).execute()
                        st.success("New site logged!")
                st.rerun()

    st.divider()
    # Compact Bar: Search, Download
    b1, b2 = st.columns([1, 3])
    with b1:
        if not df.empty: st.download_button("📥 Export Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    with b2:
        search = st.text_input("🔍 Quick Search Database...", placeholder="Search Site ID, Team, etc.")

    # DATA TABLE DISPLAY
    if not df.empty:
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        df['team_balance'] = df['team_billing'].astype(float) - df['team_paid_amt'].astype(float)
        
        # Displaying All Columns
        cols = ["project_id", "site_id", "site_name", "cluster", "project_amt", "po_no", "po_amt", "site_status", "team_name", "team_billing", "team_paid_amt", "team_balance", "wcc_no", "wcc_amt", "received_amt", "work_description"]
        st.dataframe(df[cols], use_container_width=True)

# --- 8. FINANCE LEDGER (STABLE) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Logic remains same...
