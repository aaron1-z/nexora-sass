"""FastAPI dependencies for auth and org resolution"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.config import settings
import logging
import re
import uuid

logger = logging.getLogger(__name__)
security = HTTPBearer()


# ------------------------
# Supabase Clients
# ------------------------

def get_supabase_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_key)


def get_service_supabase_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_key)


# ------------------------
# Auth
# ------------------------

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials

    try:
        supabase = get_service_supabase_client()
        user_response = supabase.auth.get_user(token)

        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return {
            "user_id": user_response.user.id,
            "email": user_response.user.email,
            "token": token,
        }

    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def get_current_user(
    user_info: dict = Depends(verify_token),
) -> dict:
    return user_info


# ------------------------
# Org Resolution (AUTO-CREATE + SLUG FIX)
# ------------------------

async def get_user_primary_org(
    user_info: dict = Depends(verify_token),
) -> dict:
    """
    Get user's primary org.
    If none exists, automatically create a personal workspace.
    """
    supabase = get_service_supabase_client()

    # 1️⃣ Try existing org
    response = (
        supabase.table("org_members")
        .select("org_id, role, organizations(*)")
        .eq("user_id", user_info["user_id"])
        .limit(1)
        .execute()
    )

    if response.data:
        membership = response.data[0]
        return {
            "org_id": membership["org_id"],
            "user_id": user_info["user_id"],
            "role": membership["role"],
            "org": membership["organizations"],
        }

    # 2️⃣ Create personal org WITH slug (FIX)
    workspace_name = f"{user_info['email']}'s workspace"

    slug_base = re.sub(r"[^a-z0-9]+", "-", workspace_name.lower()).strip("-")
    slug = f"{slug_base}-{uuid.uuid4().hex[:8]}"

    org_insert = (
        supabase.table("organizations")
        .insert({
            "name": workspace_name,
            "slug": slug,
        })
        .execute()
    )

    if not org_insert.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization",
        )

    org = org_insert.data[0]

    # 3️⃣ Add user as admin
    supabase.table("org_members").insert({
        "user_id": user_info["user_id"],
        "org_id": org["id"],
        "role": "admin",
    }).execute()

    return {
        "org_id": org["id"],
        "user_id": user_info["user_id"],
        "role": "admin",
        "org": org,
    }


# ------------------------
# Role Guards
# ------------------------

async def require_admin_primary(
    org_context: dict = Depends(get_user_primary_org),
) -> dict:
    if org_context["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return org_context


async def require_analyst_or_admin_primary(
    org_context: dict = Depends(get_user_primary_org),
) -> dict:
    role = org_context.get("role")

    if role not in ("admin", "analyst"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires admin or analyst role",
        )

    return org_context
