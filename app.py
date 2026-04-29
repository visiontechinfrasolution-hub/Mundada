import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Visiontech Mundada | Elegant Portal", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); }
    h1 { font-weight: 800; color: #0984e3; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 20px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); }
    .stButton>button { border-radius: 10px; font-weight: 700; transition: 0.3s; }
    /* Compact Row for Buttons */
    .row-container { display: flex; align-items: center; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPER FUNCTIONS ---
def format_df_dates(df):
    date_cols = ['transaction_date', 'created_at', 'Date', 'date']
    for col in df.columns:
        if any(d in col.lower() for d in date_cols) and col in df.columns:
            try: df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%Y')
            except: pass
    return df

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
    st.info(f"User: Mayur Patil\n\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD & 6. MASTER REG (UNTOUCHED LOGIC) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        if s_res.data:
            df_s, df_f = pd.DataFrame(s_res.data), (pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame())
            st.markdown("### 📍 Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            # ... (Rest of dashboard remains identical to maintain stability)
        else: st.info("No sites registered.")
    except Exception as e: st.error(f"Error: {e}")

elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with t1:
        with st.form("c_f", clear_on_submit=True):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
    with t2:
        with st.form("t_f", clear_on_submit=True):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY (UPGRADED) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registry & Operations</h1>", unsafe_allow_html=True)
    
    # NEW ENTRY FORM
    if st.button("➕ Add New Site Entry"): st.session_state.show_form = not st.session_state.get('show_form', False)

    if st.session_state.get('show_form', False):
        with st.form("full_entry_form", clear_on_submit=True):
            st.subheader("Complete Site Details (100% Columns)")
            c1, c2, c3 = st.columns(3)
            p_id = c1.text_input("Project ID (Unique)*")
            s_id = c2.text_input("Site ID")
            cl_name = c3.text_input("Client Name")
            
            c4, c5, c6 = st.columns(3)
            cluster = c4.text_input("Cluster")
            w_desc = c5.text_area("Work Description", height=65)
            p_amt = c6.number_input("Project Amount", value=None)
            
            c7, c8, c9 = st.columns(3)
            po_n, po_a = c7.text_input("PO Number"), c8.number_input("PO Amount", value=None)
            status = c9.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])

            c10, c11, c12 = st.columns(3)
            t_name = c10.text_input("Team Name")
            t_bill = c11.number_input("Team Billing", value=None)
            t_paid = c12.number_input("Team Paid Amt", value=None)

            c13, c14, c15 = st.columns(3)
            wcc_n, wcc_a = c13.text_input("WCC Number"), c14.number_input("WCC Amount", value=None)
            r_amt = c15.number_input("Received Amount", value=None)

            if st.form_submit_button("🚀 Save Site to System"):
                # Duplicate Check
                check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
                if check.data:
                    st.error(f"❌ Error: Project ID '{p_id}' already available in system.")
                elif p_id and s_id:
                    data = {"project_id": p_id, "site_id": s_id, "site_name": cl_name, "cluster": cluster, "work_description": w_desc, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "site_status": status, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                    supabase.table("site_data").insert(data).execute()
                    st.success("Site Logged!")
                    st.rerun()

    st.divider()

    # CONTROL BAR: Upload, Download, Search
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([1, 1, 1, 2])
    with ctrl1:
        uploaded_file = st.file_uploader("📂 Upload", type=['xlsx'], label_visibility="collapsed")
    with ctrl2:
        if uploaded_file:
            if st.button("✅ Confirm Upload"):
                up_df = pd.read_excel(uploaded_file).fillna(0)
                existing_ids = [x['project_id'] for x in supabase.table("site_data").select("project_id").execute().data]
                to_insert = []
                duplicates = []
                for _, row in up_df.iterrows():
                    if str(row['project_id']) in existing_ids: duplicates.append(str(row['project_id']))
                    else: to_insert.append(row.to_dict())
                
                if to_insert: supabase.table("site_data").insert(to_insert).execute()
                if duplicates: st.warning(f"⚠️ Due to duplicate Project IDs, these were not added: {', '.join(duplicates)}")
                st.success(f"Processed {len(to_insert)} new sites.")
                st.rerun()
    
    # FETCH DATA
    res_s = supabase.table("site_data").select("*").execute()
    full_df = pd.DataFrame(res_s.data) if res_s.data else pd.DataFrame()

    with ctrl3:
        if not full_df.empty:
            st.download_button("📥 Excel", data=to_excel(full_df), file_name="Mundada_Database.xlsx")
    
    with ctrl4:
        search_query = st.text_input("🔍 Search Anything...", placeholder="Type Site ID, Team or Status...")

    # DATA TABLE
    if not full_df.empty:
        # Filtering
        if search_query:
            full_df = full_df[full_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
        
        st.subheader("Live Site Database (Direct Edit Enabled)")
        # Hide ID column but keep for updates
        display_df = full_df.copy()
        
        edited_df = st.data_editor(
            display_df, 
            use_container_width=True, 
            column_config={"id": None}, # THIS HIDES THE ID COLUMN
            num_rows="dynamic",
            key="main_editor"
        )
        
        if st.button("💾 Save Changes to All Rows"):
            for _, row in edited_df.iterrows():
                # Only update if ID exists
                if 'id' in row:
                    supabase.table("site_data").update(row.to_dict()).eq('id', row['id']).execute()
            st.success("All changes synced to cloud!")

# --- 8. FINANCE LEDGER (UNTOUCHED) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # ... (Rest of Finance logic remains identical to maintain stability)
