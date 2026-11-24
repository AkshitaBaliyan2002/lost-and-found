import pytest
import app as app_module
from app import app


@pytest.fixture(autouse=True)
def clean_items():
    app_module.items.clear()


def test_home_page_loads():
    client = app.test_client()
    assert client.get("/").status_code == 200


def test_add_item():
    client = app.test_client()
    r = client.post("/add", data={"name": "Umbrella", "place": "Library", "kind": "Lost"},
                    follow_redirects=True)
    assert b"Umbrella" in r.data


def test_empty_name_not_added():
    client = app.test_client()
    client.post("/add", data={"name": " ", "place": "Lab", "kind": "Lost"})
    assert len(app_module.items) == 0


def test_claim_item():
    client = app.test_client()
    client.post("/add", data={"name": "Umbrella", "place": "Library", "kind": "Lost"})
    item_id = app_module.items[0]["id"]
    r = client.get(f"/claim/{item_id}", follow_redirects=True)
    assert b"CLAIMED" in r.data


def test_search():
    client = app.test_client()
    client.post("/add", data={"name": "Umbrella", "place": "Library", "kind": "Lost"})
    client.post("/add", data={"name": "Bottle", "place": "Canteen", "kind": "Found"})
    r = client.get("/?q=umb")
    assert b"Umbrella" in r.data
    assert b"Bottle" not in r.data


def test_delete_item():
    client = app.test_client()
    client.post("/add", data={"name": "Umbrella", "place": "Library", "kind": "Lost"})
    item_id = app_module.items[0]["id"]
    client.get(f"/delete/{item_id}")
    assert len(app_module.items) == 0


def test_filter_by_kind():
    client = app.test_client()
    client.post("/add", data={"name": "Umbrella", "place": "Library", "kind": "Lost"})
    client.post("/add", data={"name": "Bottle", "place": "Canteen", "kind": "Found"})
    r = client.get("/?kind=Lost")
    assert b"Umbrella" in r.data
    assert b"Bottle" not in r.data