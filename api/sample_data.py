from datetime import datetime, timedelta
from decimal import Decimal

from .dependencies.database import Base, SessionLocal, engine
from .models.customers import Customer
from .models.menu_items import MenuItem
from .models.order_details import OrderDetail
from .models.orders import Order
from .models.payments import Payment
from .models.promotions import Promotion
from .models.recipes import Recipe
from .models.resources import Resource
from .models.reviews import Review


def add_sample_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        bun = Resource(item="Burger Bun", amount=50, unit="pieces")
        patty = Resource(item="Beef Patty", amount=40, unit="pieces")
        cheese = Resource(item="Cheese Slice", amount=60, unit="slices")
        fries_resource = Resource(item="Fries", amount=25, unit="pounds")
        salad = Resource(item="Salad", amount=20, unit="cups")

        db.add_all([
            bun,
            patty,
            cheese,
            fries_resource,
            salad,
        ])
        db.flush()

        burger = MenuItem(
            name="Basic Cheeseburger",
            description="Burger with cheese",
            price=Decimal("10.99"),
            calories=720,
            category="burger",
            is_available=True
        )

        fries = MenuItem(
            name="French Fries",
            description="Potato sslices",
            price=Decimal("4.49"),
            calories=380,
            category="side",
            is_available=True
        )

        salad = MenuItem(
            name="Garden Salad",
            description="Fresh vegetarian salad",
            price=Decimal("7.99"),
            calories=240,
            category="vegetarian",
            is_available=True
        )

        db.add_all([burger, fries, salad])
        db.flush()

        db.add_all([
            Recipe(
                menu_item_id=burger.id,
                resource_id=bun.id,
                amount=1
            ),
            Recipe(
                menu_item_id=burger.id,
                resource_id=patty.id,
                amount=1
            ),
            Recipe(
                menu_item_id=burger.id,
                resource_id=cheese.id,
                amount=1
            ),
            Recipe(
                menu_item_id=fries.id,
                resource_id=fries_resource.id,
                amount=Decimal("0.50")
            ),
            Recipe(
                menu_item_id=salad.id,
                resource_id=salad.id,
                amount=2
            )
        ])

        customer = Customer(
            name="Mika Klymenko",
            email="mika@charlotte.edu",
            phone="704-555-0101",
            address="123 Charlotte NC"
        )

        promotion = Promotion(
            code="SAVE10",
            description="Ten percent off",
            discount_type="percentage",
            discount_value=10,
            expiration_date=datetime.now() + timedelta(days=30),
            is_active=True
        )

        db.add_all([customer, promotion])
        db.flush()

        order = Order(
            customer_id=customer.id,
            promotion_id=promotion.id,
            tracking_number="trackingnumber-123",
            order_status="completed",
            order_type="takeout",
            total_price=Decimal("14.83")
        )

        db.add(order)
        db.flush()

        db.add_all([
            OrderDetail(
                order_id=order.id,
                menu_item_id=burger.id,
                quantity=1,
                unit_price=burger.price
            ),
            OrderDetail(
                order_id=order.id,
                menu_item_id=fries.id,
                quantity=1,
                unit_price=fries.price
            )
        ])

        payment = Payment(
            order_id=order.id,
            payment_type="card",
            transaction_status="paid",
            transaction_id="SAMPLE-MKK-001",
            amount=Decimal("14.83"),
            card_last_four="4242",
            paid_at=datetime.now()
        )

        review = Review(
            order_id=order.id,
            customer_id=customer.id,
            rating=5,
            review_text="The burger was just so delicious, i will visit this restaurant a billion more times!<3"
        )

        db.add_all([payment, review])
        db.commit()

        print("Sample data added successfully.")

    except Exception as error:
        db.rollback()
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    add_sample_data()