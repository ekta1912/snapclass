import streamlit as st
import segno
import io
import urllib.parse


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    # Production live URL
    base_url = "https://snapclass-pgvcdcd8twu49bgpgz2xgx.streamlit.app"

    # Only accept secret APP_URL if valid and not a placeholder
    try:
        if hasattr(st, "secrets") and "APP_URL" in st.secrets:
            app_url_val = str(st.secrets["APP_URL"]).strip()
            if app_url_val and "your-app-name" not in app_url_val and "example" not in app_url_val:
                base_url = app_url_val
    except Exception:
        pass

    # Ensure protocol and format
    base_url = base_url.rstrip("/")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    clean_code = str(subject_code).strip()
    encoded_code = urllib.parse.quote(clean_code)
    join_url = f"{base_url}/?join-code={encoded_code}"

    st.subheader(f"Scan or Click to Join: {subject_name}")

    # Generate QR Code with join URL
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### 🔗 Class Invite Link')
        st.code(join_url, language="text")
        st.markdown(f"**Subject Code:** `{clean_code}`")
        st.link_button("🌐 Open Invite Link", join_url, use_container_width=True)
        st.info('Copy and share this link via WhatsApp, Email, or Class Groups.')

    with col2:
        st.markdown('### 📱 Scan to Join')
        st.image(out.getvalue(), caption=f'QR Code for {subject_name} ({clean_code})', use_container_width=True)
