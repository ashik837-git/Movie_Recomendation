from .interface import PaymentProvider, SubscriptionPlanInfo, CheckoutSessionResult, WebhookProcessingResult
from .sandbox_provider import SandboxPaymentProvider
from .stripe_provider import StripePaymentProvider
from ..config import settings

_provider_instances = {}

def get_payment_provider() -> PaymentProvider:
    provider_type = settings.PAYMENT_PROVIDER.lower()
    if provider_type not in _provider_instances:
        if provider_type == "stripe":
            _provider_instances[provider_type] = StripePaymentProvider()
        else:
            _provider_instances[provider_type] = SandboxPaymentProvider()
    return _provider_instances[provider_type]

__all__ = [
    "PaymentProvider",
    "SubscriptionPlanInfo",
    "CheckoutSessionResult",
    "WebhookProcessingResult",
    "SandboxPaymentProvider",
    "StripePaymentProvider",
    "get_payment_provider",
]
