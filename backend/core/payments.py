"""Simplified payment processing utilities."""
from __future__ import annotations


def process_payment(provider: str, amount: float) -> str:
    """Process a payment through the selected provider.

    This is a lightweight placeholder implementation which simulates
    successful payments for MercadoPago and Stripe. In a real-world
    scenario, this function would interact with the providers' SDKs.
    """
    provider = provider.lower()
    if provider == "stripe":
        # Simulate Stripe payment processing
        return f"stripe_{int(amount * 100)}"
    if provider == "mercadopago":
        # Simulate MercadoPago payment processing
        return f"mp_{int(amount * 100)}"
    raise ValueError("Unsupported payment provider")
