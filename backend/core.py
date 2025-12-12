import os
from typing import Optional

from supabase import create_client


def _load_env():
    try:
        from dotenv import load_dotenv

        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        dotenv_path = os.path.join(repo_root, ".env")
        load_dotenv(dotenv_path)
    except Exception:
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            dotenv_path = os.path.join(repo_root, ".env")
            if not os.path.exists(dotenv_path):
                dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
            if os.path.exists(dotenv_path):
                with open(dotenv_path, "r", encoding="utf-8") as fh:
                    for ln in fh:
                        ln = ln.strip()
                        if not ln or ln.startswith("#"):
                            continue
                        if "=" in ln:
                            k, v = ln.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k and (k not in os.environ):
                                os.environ[k] = v
        except Exception:
            pass


_load_env()

SUPABASE_URL: Optional[str] = os.environ.get("VITE_SUPABASE_URL")
SUPABASE_KEY: Optional[str] = (
    os.environ.get("VITE_SUPABASE_ANON_KEY")
)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise ValueError("Authorization header missing")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Invalid authorization header")
    return parts[1]


def extract_discord_id_from_user(user) -> Optional[str]:
    try:
        if isinstance(user, dict):
            identities = user.get("identities") or user.get("user_metadata", {}).get("identities")
        else:
            identities = getattr(user, "identities", None)
        if identities and isinstance(identities, (list, tuple)) and len(identities) > 0:
            first = identities[0]
            if isinstance(first, dict):
                return first.get("id")
            return getattr(first, "id", None)
    except Exception:
        return None
    return None


def get_user_by_token(token: str):
    try:
        resp_user = supabase.auth.get_user(token)
        if isinstance(resp_user, dict):
            user = resp_user.get("data") or resp_user.get("user")
            err = resp_user.get("error")
        else:
            user = getattr(resp_user, "data", None) or getattr(resp_user, "user", None)
            err = getattr(resp_user, "error", None)
        if err:
            raise RuntimeError(str(err))
        return user
    except Exception as e:
        raise RuntimeError(f"failed to validate token: {e}")
