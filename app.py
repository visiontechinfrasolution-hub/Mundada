import streamlit as st
from supabase import create_client, Client

# Supabase Connection (Apne URL aur Key yaha daalein)
url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_KEY"
supabase: Client = create_client(url, key)

def save_site_data(data_dict):
    try:
        response = supabase.table("site_data").insert(data_dict).execute()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

st.title("Visiontech Management - Mundada")

# Sidebar for Navigation
menu = ["Dashboard", "Site Data", "Finance"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Site Data":
    st.subheader("🏗️ Add New Site Data")
    
    with st.form("site_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            project_id = st.text_input("Project ID")
            site_id = st.text_input("Site ID")
            site_name = st.text_input("Site Name")
            cluster = st.text_input("Cluster")
            work_desc = st.text_area("Work Description")
            project_amt = st.number_input("Project Amt", min_value=0.0)
            
        with col2:
            po_no = st.text_input("PO No")
            po_amt = st.number_input("PO Amt", min_value=0.0)
            site_status = st.selectbox("Site Status", ["Pending", "In Progress", "Completed"])
            team_name = st.text_input("Team Name")
            team_billing = st.number_input("Team Billing", min_value=0.0)
            team_paid = st.number_input("Team Paid Amt", min_value=0.0)

        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            wcc_no = st.text_input("WCC No.")
            wcc_amt = st.number_input("WCC Amt", min_value=0.0)
        with col4:
            received_amt = st.number_input("Received Amt", min_value=0.0)

        if st.form_submit_button("Save to Supabase"):
            # Data Dictionary for Supabase
            new_entry = {
                "project_id": project_id,
                "site_id": site_id,
                "site_name": site_name,
                "cluster": cluster,
                "work_description": work_desc,
                "project_amt": project_amt,
                "po_no": po_no,
                "po_amt": po_amt,
                "site_status": site_status,
                "team_name": team_name,
                "team_billing": team_billing,
                "team_paid_amt": team_paid,
                "wcc_no": wcc_no,
                "wcc_amt": wcc_amt,
                "received_amt": received_amt
            }
            
            if save_site_data(new_entry):
                st.success(f"Site {site_id} ka data save ho gaya hai!")

elif choice == "Finance":
    st.subheader("💰 Finance Entry")
    # Yaha Finance table ka form aayega
