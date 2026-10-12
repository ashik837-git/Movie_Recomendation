"""
CinePulse Sandbox Payment Provider
Simulates end-to-end checkout, entitlement granting, and webhook processing for local testing.
Compatible with test workflows in Bangladesh and non-Stripe environments.
"""
import hashlib
import time
import uuid
from typing import Dict, List, Optional

from .interface import CheckoutSessionResult, PaymentProvider, SubscriptionPlanInfo, WebhookProcessingResult

# Configurable subscription plans
SANDBOX_PLANS = [
    SubscriptionPlanInfo(
        id="free",
        name="Free Explorer",
        price_monthly=0.00,
        currency="USD",
        recommendation_limit="25 requests / day",
        features=[
            "Browse entire cinematic catalog",
            "Real-time metadata search",
            "Up to 25 NLP recommendation queries daily",
            "Standard community support",
        ],
    ),
    SubscriptionPlanInfo(
        id="premium",
        name="CinePulse Premium",
        price_monthly=9.99,
        currency="USD",
        recommendation_limit="Unlimited queries",
        features=[
            "Unlimited NLP similarity requests",
            "Personalized watchlist persistence",
            "Early access to new catalog arrivals",
            "High-priority similarity ranking engine",
            "Ad-free cinematic interface",
        ],
        badge="Most Popular",
    ),
    SubscriptionPlanInfo(
        id="pro",
        name="Auteur Pro",
        price_monthly=19.99,
        currency="USD",
        recommendation_limit="Unlimited + API Access",
        features=[
            "Everything in Premium tier",
            "Custom metadata soup weighting weights",
            "Direct REST API key access",
            "Raw CSV export & analytics exports",
            "Priority 24/7 technical assistance",
        ],
        badge="Studio Grade",
    ),
]

class SandboxPaymentProvider(PaymentProvider):
    def __init__(self):
        self.processed_events: set = set()

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
        # Verify plan exists
        valid_plan = next((p for p in SANDBOX_PLANS if p.id == plan_id), None)
        if not valid_plan:
            raise ValueError(f"Unknown subscription plan: {plan_id}")

        session_id = f"cs_test_sandbox_{uuid.uuid4().hex[:12]}"
        # In sandbox, redirecting directly to success_url with simulated session token
        separator = "&" if "?" in success_url else "?"
        simulated_checkout_url = f"{success_url}{separator}session_id={session_id}&plan={plan_id}&provider=sandbox"

        return CheckoutSessionResult(
            checkout_url=simulated_checkout_url,
            session_id=session_id,
            provider="sandbox"
        )

    def process_webhook(self, payload: bytes, signature_header: Optional[str]) -> WebhookProcessingResult:
        """Processes simulated sandbox webhook payloads idempotently."""
        event_hash = hashlib.sha256(payload).hexdigest()[:16]
        event_id = f"evt_sandbox_{event_hash}"

        if event_id in self.processed_events:
            return WebhookProcessingResult(
                event_id=event_id,
                event_type="sandbox.checkout.completed",
                status="duplicate",
                processed=False,
                message="Event already processed previously (idempotent ignore)."
            )

        self.processed_events.add(event_id)
        return WebhookProcessingResult(
            event_id=event_id,
            event_type="sandbox.checkout.completed",
            status="active",
            processed=True,
            message="Sandbox subscription successfully provisioned."
        )
