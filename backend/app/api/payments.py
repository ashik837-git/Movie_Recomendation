"""
CinePulse Subscriptions & Payments API
Provider-agnostic router supporting Stripe and Sandbox checkouts with webhook verification.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel

from ..auth.jwt_validator import AuthenticatedUser, get_optional_current_user
from ..payments import get_payment_provider
from ..payments.interface import SubscriptionPlanInfo

router = APIRouter(prefix="/payments", tags=["payments"])

class CreateCheckoutRequest(BaseModel):
    plan_id: str
    success_url: str
    cancel_url: str

@router.get("/plans", response_model=List[SubscriptionPlanInfo])
def list_subscription_plans():
    """Returns available subscription tiers, pricing, and feature entitlements."""
    provider = get_payment_provider()
    return provider.get_plans()

@router.post("/create-checkout-session")
def create_checkout_session(
    body: CreateCheckoutRequest,
    current_user: Optional[AuthenticatedUser] = Depends(get_optional_current_user)
):
    """
    Creates an authenticated server-side checkout session.
    If user is not logged in, generates an anonymous checkout placeholder.
    """
    provider = get_payment_provider()
    user_id = current_user.user_id if current_user else "guest_user"
    user_email = current_user.email if current_user and current_user.email else "guest@cinepulse.example.com"

    try:
        session = provider.create_checkout_session(
            user_id=user_id,
            user_email=user_email,
            plan_id=body.plan_id,
            success_url=body.success_url,
            cancel_url=body.cancel_url
        )
        return {
            "checkout_url": session.checkout_url,
            "session_id": session.session_id,
            "provider": session.provider
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/webhook")
async def handle_payment_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="Stripe-Signature")
):
    """
    Ingests provider webhook callbacks, validates signatures, and idempotently updates subscriptions.
    """
    provider = get_payment_provider()
    payload = await request.body()
    result = provider.process_webhook(payload=payload, signature_header=stripe_signature)

    if result.status == "rejected":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)

    return {
        "status": result.status,
        "event_id": result.event_id,
        "processed": result.processed,
        "message": result.message
    }
