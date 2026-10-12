"""
CinePulse Payment Provider Interface & Data Contracts
Defines provider-agnostic abstractions for subscription checkout, webhooks, and entitlement management.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class SubscriptionPlanInfo(BaseModel):
    id: str
    name: str
    price_monthly: float
    currency: str
    recommendation_limit: str
    features: List[str]
    badge: Optional[str] = None

class CheckoutSessionResult(BaseModel):
    checkout_url: str
    session_id: str
    provider: str

class WebhookProcessingResult(BaseModel):
    event_id: str
    event_type: str
    user_id: Optional[str] = None
    plan_id: Optional[str] = None
    status: str
    processed: bool
    message: str

class PaymentProvider(ABC):
    """Abstract Base Class for all payment processors (Stripe, SSLCommerz, Sandbox)."""

    @abstractmethod
    def get_plans(self) -> List[SubscriptionPlanInfo]:
        """Returns the configured subscription tiers and entitlements."""
        pass

    @abstractmethod
    def create_checkout_session(
        self,
        user_id: str,
        user_email: str,
        plan_id: str,
        success_url: str,
        cancel_url: str
    ) -> CheckoutSessionResult:
        """Initiates an authenticated checkout session with the provider."""
        pass

    @abstractmethod
    def process_webhook(self, payload: bytes, signature_header: Optional[str]) -> WebhookProcessingResult:
        """Verifies signature idempotently and translates provider events to subscription updates."""
        pass
