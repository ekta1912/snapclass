import os
import streamlit as st
from supabase import create_client, Client


def get_supabase_credentials():
    url = None
    key = None

    # 1. Try Streamlit secrets
    try:
        if hasattr(st, "secrets"):
            if "SUPABASE_URL" in st.secrets:
                url = st.secrets["SUPABASE_URL"]
            if "SUPABASE_KEY" in st.secrets:
                key = st.secrets["SUPABASE_KEY"]
            elif "SUPABASE_SECRET_KEY" in st.secrets:
                key = st.secrets["SUPABASE_SECRET_KEY"]
            elif "SUPABASE_PUBLISHABLE_KEY" in st.secrets:
                key = st.secrets["SUPABASE_PUBLISHABLE_KEY"]
    except Exception:
        pass

    # 2. Try direct read from .streamlit/secrets.toml
    if not url or not key:
        try:
            import toml
            for path in [".streamlit/secrets.toml", os.path.join(os.getcwd(), ".streamlit", "secrets.toml")]:
                if os.path.exists(path):
                    data = toml.load(path)
                    if not url:
                        url = data.get("SUPABASE_URL")
                    if not key:
                        key = (
                            data.get("SUPABASE_KEY")
                            or data.get("SUPABASE_SECRET_KEY")
                            or data.get("SUPABASE_PUBLISHABLE_KEY")
                        )
                    break
        except Exception:
            pass

    # 3. Try Environment Variables
    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = (
            os.environ.get("SUPABASE_KEY")
            or os.environ.get("SUPABASE_SECRET_KEY")
            or os.environ.get("SUPABASE_PUBLISHABLE_KEY")
        )

    return url, key


def is_supabase_configured() -> bool:
    url, key = get_supabase_credentials()
    if not url or not key:
        return False
    if "your-project-id" in url or "placeholder" in url:
        return False
    return True


class SupabaseProxy:
    """Dynamic proxy ensuring Supabase client always uses the latest configured credentials."""
    def __init__(self):
        self._client = None
        self._cached_key = None

    def _get_client(self):
        url, key = get_supabase_credentials()
        if not url or not key or "your-project-id" in url or "placeholder" in url:
            return None
        if self._client is None or self._cached_key != key:
            try:
                self._client = create_client(url, key)
                self._cached_key = key
            except Exception:
                pass
        return self._client

    def __getattr__(self, name):
        client = self._get_client()
        if client is None:
            try:
                client = create_client("https://placeholder-project.supabase.co", "placeholder-key")
            except Exception:
                raise RuntimeError("Supabase client is not configured.")
        return getattr(client, name)


supabase = SupabaseProxy()