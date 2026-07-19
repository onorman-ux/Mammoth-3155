from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from ..controllers import orders as controller
from ..main import app
from ..schemas import orders as schema


client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    order_data = schema.OrderCreate(
        customer_id=None,
        promotion_id=None,
        guest_name="John Doe",
        guest_email="john@example.com",
        guest_phone="555-0100",
        tracking_number="TEST-ORDER-001",
        order_status="pending",
        order_type="takeout",
        delivery_address=None,
        total_price=Decimal("25.50"),
    )

    created_order = controller.create(db_session, order_data)

    assert created_order is not None
    assert created_order.guest_name == "John Doe"
    assert created_order.tracking_number == "TEST-ORDER-001"
    assert created_order.total_price == Decimal("25.50")
