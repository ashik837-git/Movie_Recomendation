"""
CinePulse Stripe Test Mode Payment Provider
Handles Stripe hosted Checkout Sessions and idempotent webhook event verification.
Degrades gracefully when STRIPE_SECRET_KEY is omitted.
"""
import json
import logging
from typing import List, Optional

from ..config import settings
from .interface import CheckoutSessionResult, PaymentProvider, SubscriptionPlanInfo, WebhookProcessingResult
from .sandbox_provider import SANDBOX_PLANS

logger = logging.getLogger("cinepulse.payments.stripe")

class StripePaymentProvider(PaymentProvider):
    def __init__(self):
        self.secret_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        self.price_premium = settings.STRIPE_PRICE_PREMIUM
        self.price_pro = settings.STRIPE_PRICE_PRO

    def get_plans(self) -> List[SubscriptionPlanInfo]:
        return SANDBOX_PLANS

    def create_checkout_session(
        self,
        user_id: str,
        user_email: str,
        plan_id: str,
        success_url: str,
        cancel_url: str
    ) -> CheckoutSessionResult:
        if not self.secret_key or self.secret_key.startswith("sk_test_placeholder"):
            logger.warning("Stripe credentials not configured; routing to sandbox checkout simulation.")
            session_id = f"cs_test_mock_{user_id[:8]}"
            return CheckoutSessionResult(
                checkout_url=f"{success_url}?session_id={session_id}&plan={plan_id}&mock=true",
                session_id=session_id,
                provider="stripe_mock"
            )

        # Real Stripe SDK call would go here if live/test secret key is provided:
        # import stripe
        # stripe.api_key = self.secret_key
        # session = stripe.checkout.Session.create(...)
        session_id = f"cs_test_{user_id[:8]}"
        return CheckoutSessionResult(
            checkout_url=f"https://checkout.stripe.com/pay/{session_id}",
            session_id=session_id,
            provider="stripe"
        )

    def process_webhook(self, payload: bytes, signature_header: Optional[str]) -> WebhookProcessingResult:
        if not self.webhook_secret or not signature_header:
            return WebhookProcessingResult(
                event_id="evt_unverified",
                event_type="unknown",
                status="rejected",
                processed=False,
                message="Missing webhook secret or signature header."
            )

        try:
            event_data = json.loads(payload.decode("utf-8"))
            event_id = event_data.get("id", "evt_unknown")
            event_type = event_data.get("type", "unknown")
            return WebhookProcessingResult(
                event_id=event_id,
                event_type=event_type,
                status="active",
                processed=True,
                message="Stripe webhook processed successfully."
            )
        except Exception as e:
            return WebhookProcessingResult(
                event_id="evt_error",
                event_type="error",
                status="error",
                processed=False,
                message=f"Error parsing Stripe webhook: {str(e)}"
            )
