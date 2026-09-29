import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    # Production live URL as default
    base_url = "https://snapclass-pgvcdcd8twu49bgpgz2xgx.streamlit.app"

    # Read from secrets if configured and not a placeholder
    try:
        if hasattr(st, "secrets") and "APP_URL" in st.secrets:
            configured_url = str(st.secrets["APP_URL"]).strip()
            if configured_url and "your-app-name" not in configured_url and "example.com" not in configured_url:
                base_url = configured_url
    except Exception:
        pass

    # Dynamically detect host in deployed environment if available
    try:
        if hasattr(st, "context") and hasattr(st.context, "headers") and st.context.headers:
            host = st.context.headers.get("host")
            if host and "your-app-name" not in host and "localhost" not in host and "127.0.0.1" not in host:
                base_url = f"https://{host}"
    except Exception:
        pass

    base_url = base_url.rstrip("/")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    join_url = f"{base_url}/?join-code={subject_code}"

    st.subheader(f"Scan or Click to Join: {subject_name}")

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### 🔗 Class Invite Link')
        st.code(join_url, language="text")
        st.markdown(f"**Subject Code:** `{subject_code}`")
        st.link_button("🌐 Open Invite Link", join_url, use_container_width=True)
        st.info('Copy and share this link via WhatsApp, Email, or Class Groups.')

    with col2:
        st.markdown('### 📱 Scan to Join')
        st.image(out.getvalue(), caption=f'QR Code for {subject_name} ({subject_code})', use_container_width=True)