import os
import streamlit as st
from supabase import create_client, Client


def get_supabase_credentials():
    url = None
    key = None
    try:
        if hasattr(st, "secrets"):
            if "SUPABASE_URL" in st.secrets:
                url = st.secrets["SUPABASE_URL"]
            if "SUPABASE_KEY" in st.secrets:
                key = st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")

    return url, key


def is_supabase_configured() -> bool:
    url, key = get_supabase_credentials()
    if not url or not key:
        return False
    if "your-project-id" in url or "your-supabase" in key or "placeholder" in url:
        return False
    return True


_url, _key = get_supabase_credentials()

if is_supabase_configured():
    supabase: Client = create_client(_url, _key)
else:
    try:
        supabase: Client = create_client(
            _url or "https://placeholder-project.supabase.co",
            _key or "placeholder-anon-key"
        )
    except Exception:
        supabase = None