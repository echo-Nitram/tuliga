import sys
import types
from unittest.mock import Mock

# The payments tests run without the real Stripe and MercadoPago SDKs. When
# those packages are missing we insert small stand-ins into ``sys.modules`` so
# that the production code can import and monkeypatch them normally.
try:  # pragma: no cover - executed only when SDKs are missing
    import stripe  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    stripe = types.SimpleNamespace(
        PaymentIntent=types.SimpleNamespace(create=lambda *a, **k: None)
    )
    sys.modules["stripe"] = stripe  # type: ignore

try:  # pragma: no cover - executed only when SDKs are missing
    import mercadopago  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    mercadopago = types.SimpleNamespace(SDK=object)
    sys.modules["mercadopago"] = mercadopago  # type: ignore

from backend.core.payments import process_payment


def test_stripe_calls_sdk_when_credentials(monkeypatch):
    mock_create = Mock(return_value=types.SimpleNamespace(id="pi_test"))
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test")
    monkeypatch.setattr(stripe.PaymentIntent, "create", mock_create)
    payment_id = process_payment("stripe", 10, currency="usd")
    assert payment_id == "pi_test"
    mock_create.assert_called_once_with(
        amount=1000, currency="usd", payment_method_types=["card"]
    )


def test_stripe_deterministic_id_without_credentials(monkeypatch):
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    payment_id = process_payment("stripe", 10)
    assert payment_id == "stripe_1000"


class DummyPayment:
    called_with = None

    def create(self, data):
        DummyPayment.called_with = data
        return {"response": {"id": 42}}


class DummySDK:
    def __init__(self, token):
        self.token = token

    def payment(self):
        return DummyPayment()


def test_mercadopago_calls_sdk_when_credentials(monkeypatch):
    monkeypatch.setenv("MERCADOPAGO_ACCESS_TOKEN", "token")
    monkeypatch.setattr(mercadopago, "SDK", DummySDK)
    payment_id = process_payment("mercadopago", 15)
    assert payment_id == "42"
    assert DummyPayment.called_with["transaction_amount"] == 15


def test_mercadopago_deterministic_id_without_credentials(monkeypatch):
    monkeypatch.delenv("MERCADOPAGO_ACCESS_TOKEN", raising=False)
    payment_id = process_payment("mercadopago", 15)
    assert payment_id == "mp_1500"
