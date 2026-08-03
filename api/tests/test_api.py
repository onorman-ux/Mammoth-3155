import os
os.environ["DATABASE_URL"] = "sqlite:///./test_oros.db"

from fastapi.testclient import TestClient
from api.main import app
from api.dependencies.database import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_root_and_crud():
    assert client.get("/").status_code == 200
    resource = client.post("/resources/", json={"item":"Bread","amount":20,"unit":"slices"})
    assert resource.status_code == 200
    menu = client.post("/menu-items/", json={"name":"Toast","description":"Simple toast","price":3.5,"calories":150,"category":"vegetarian","is_available":True})
    assert menu.status_code == 200
    recipe = client.post("/recipes/", json={"menu_item_id":menu.json()["id"],"resource_id":resource.json()["id"],"amount":2})
    assert recipe.status_code == 200


def test_checkout_and_tracking():
    menu_id = client.get("/menu-items/").json()[0]["id"]
    response=client.post("/orders/checkout",json={"guest_name":"Test Guest","guest_phone":"555-0100","order_type":"takeout","items":[{"menu_item_id":menu_id,"quantity":2}]})
    assert response.status_code == 200, response.text
    tracking=response.json()["tracking_number"]
    tracked=client.get(f"/orders/track/{tracking}")
    assert tracked.status_code == 200
    assert tracked.json()["order_status"] == "received"
