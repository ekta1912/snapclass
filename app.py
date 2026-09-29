import streamlit as st
from src.database.config import is_supabase_configured
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog


def show_setup_instructions():
    st.markdown("""
    <div style="background-color: #5865F2; padding: 2rem; border-radius: 1.5rem; color: white; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">📸 SNAPCLASS</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">AI-Powered Attendance System</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ **Supabase Credentials Required**")

    st.markdown("""
    To get started, please configure your Supabase database credentials:

    ### 1️⃣ Local Development
    Edit `.streamlit/secrets.toml` in the project root:
    ```toml
    SUPABASE_URL = "https://your-project-id.supabase.co"
    SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
    ```
    *You can find these in your [Supabase Dashboard](https://supabase.com/dashboard) under **Project Settings ➡️ API**.*

    ### 2️⃣ Streamlit Community Cloud Deployment
    1. Deploy this repository to [share.streamlit.io](https://share.streamlit.io).
    2. Go to your app dashboard ➡️ **Settings** (⚙️) ➡️ **Secrets**.
    3. Paste:
    ```toml
    SUPABASE_URL = "https://your-project-id.supabase.co"
    SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
    ```
    4. Save and your app will automatically restart!

    ### 3️⃣ Database Tables Setup
    Run the provided `supabase_schema.sql` in the **SQL Editor** on your Supabase dashboard to create all required tables with one click.
    """)


def main():
    st.set_page_config(
        page_title='SnapClass - AI Attendance System',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",
        layout="wide"
    )

    if not is_supabase_configured():
        show_setup_instructions()
        return

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.get('login_type') != 'student':
            st.session_state['login_type'] = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)


if __name__ == '__main__':
    main()