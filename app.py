# --- UPDATE SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    # Naya Option: Master Registration
    page = st.radio("MAIN NAVIGATION", [
        "🏠 Overview Dashboard", 
        "📝 Master Registration", # Naya Page
        "🏗️ Project Site Registry", 
        "💸 Financial Control Center"
    ])
    st.divider()

# --- NEW PAGE: MASTER REGISTRATION ---
if page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registration</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👥 Client Registration", "🛠️ Team Registration"])
    
    # --- CLIENT REGISTRATION ---
    with tab1:
        with st.form("client_form", clear_on_submit=True):
            st.subheader("Add New Client")
            c_name = st.text_input("Client Name (Company Name)")
            col1, col2 = st.columns(2)
            c_person = col1.text_input("Contact Person")
            c_phone = col2.text_input("Contact Number")
            c_email = st.text_input("Email Address")
            
            if st.form_submit_button("Register Client"):
                if c_name:
                    client_data = {
                        "client_name": c_name,
                        "contact_person": c_person,
                        "contact_number": c_phone,
                        "email": c_email
                    }
                    try:
                        supabase.table("client_master").insert(client_data).execute()
                        st.success(f"Client '{c_name}' registered successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Client Name is required.")

    # --- TEAM REGISTRATION ---
    with tab2:
        with st.form("team_form", clear_on_submit=True):
            st.subheader("Add New Team / Vendor")
            t_name = st.text_input("Team Name (Agency Name)")
            col1, col2 = st.columns(2)
            t_leader = col1.text_input("Team Leader Name")
            t_phone = col2.text_input("Leader Contact Number")
            t_spec = st.text_input("Specialization (e.g. Electrical, Civil)")
            
            if st.form_submit_button("Register Team"):
                if t_name:
                    team_data = {
                        "team_name": t_name,
                        "leader_name": t_leader,
                        "leader_contact": t_phone,
                        "specialization": t_spec
                    }
                    try:
                        supabase.table("team_master").insert(team_data).execute()
                        st.success(f"Team '{t_name}' registered successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Team Name is required.")
