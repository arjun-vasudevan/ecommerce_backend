from contextlib import contextmanager
from fastapi.testclient import TestClient
from pytest import fixture
from unittest.mock import patch

from services.cart_service.main import app
from services.cart_service.models.models import Cart, CartItem


client = TestClient(app)

# Fixtures --------------------------------------------------------------------


@fixture(autouse=True)
def populate_database(setup_database, db):
    carts = [Cart(user_id=1), Cart(user_id=2)]
    cart_items = [
        CartItem(cart_id=1, product_id=100, quantity=55),
        CartItem(cart_id=1, product_id=101, quantity=10),
        CartItem(cart_id=2, product_id=200, quantity=12),
    ]

    db.add_all(carts)
    db.add_all(cart_items)
    db.commit()


@fixture(scope="session")
def mock_jwt_decode():

    @contextmanager
    def _mock_jwt_decode(user_id):
        with patch("services.cart_service.main.decode_access_token") as mock_decode:
            mock_decode.return_value = {"id": user_id}
            yield

    return _mock_jwt_decode


@fixture(scope="session")
def query():
    return {
        "query": """query Cart {
        cart {
            id
            userId
            items {
                id
                productId
                quantity
            }
        }
    }"""
    }


@fixture(scope="session")
def mutation():
    def _mutation(product_id, quantity=None):
        return f"""mutation AddItem {{
            addCartItem (productId: {product_id}{f', quantity: {quantity}' if quantity is not None else ''}) {{
                id
                cartId
                productId
                quantity
            }}
        }}"""

    return _mutation


# Query tests --------------------------------------------------------------


def test_get_cart(mock_jwt_decode, query):
    with mock_jwt_decode(user_id=2):
        response = client.post(
            "/graphql", json=query, headers={"Authorization": "Bearer token"}
        )

    expected_response = {
        "data": {
            "cart": {
                "id": 2,
                "userId": "2",
                "items": [{"id": 3, "productId": 200, "quantity": 12}],
            }
        }
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response


def test_get_null_cart(mock_jwt_decode, query):
    with mock_jwt_decode(user_id=3):
        response = client.post(
            "/graphql", json=query, headers={"Authorization": "Bearer token"}
        )

    expected_response = {"data": {"cart": None}}

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response


# Mutation tests --------------------------------------------------------------


def test_add_new_item_to_new_cart(mock_jwt_decode, mutation, db):
    new_user = 3
    with mock_jwt_decode(user_id=new_user):
        mutation_query = mutation(product_id=300, quantity=5)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {"addCartItem": {"id": 4, "cartId": 3, "productId": 300, "quantity": 5}}
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    new_cart = db.query(Cart).filter(Cart.user_id == new_user).first()
    assert new_cart is not None
    assert new_cart.user_id == new_user
    assert new_cart.items[0].cart_id == new_cart.id
    assert new_cart.items[0].product_id == 300
    assert new_cart.items[0].quantity == 5


def test_add_new_item_to_existing_cart(mock_jwt_decode, mutation, db):
    user_id = 1
    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=102, quantity=3)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {"addCartItem": {"id": 4, "cartId": 1, "productId": 102, "quantity": 3}}
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart is not None
    assert len(cart.items) == 3
    assert cart.items[2].cart_id == cart.id
    assert cart.items[2].product_id == 102
    assert cart.items[2].quantity == 3


def test_update_to_specific_quantity(mock_jwt_decode, mutation, db):
    user_id = 2
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart.items[0].quantity == 12

    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=200, quantity=18)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {
            "addCartItem": {"id": 3, "cartId": 2, "productId": 200, "quantity": 18}
        }
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    db.refresh(cart)
    assert cart is not None
    assert len(cart.items) == 1
    assert cart.items[0].cart_id == cart.id
    assert cart.items[0].product_id == 200
    assert cart.items[0].quantity == 18


def test_set_default_quantity_to_one(mock_jwt_decode, mutation, db):
    user_id = 3
    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=300)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {"addCartItem": {"id": 4, "cartId": 3, "productId": 300, "quantity": 1}}
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart is not None
    assert len(cart.items) == 1
    assert cart.items[0].cart_id == cart.id
    assert cart.items[0].product_id == 300
    assert cart.items[0].quantity == 1


def test_increment_quantity_by_one(mock_jwt_decode, mutation, db):
    user_id = 1
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart.items[0].quantity == 55

    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=100)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {
            "addCartItem": {"id": 1, "cartId": 1, "productId": 100, "quantity": 56}
        }
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    db.refresh(cart)
    assert cart is not None
    assert len(cart.items) == 2
    assert cart.items[0].cart_id == cart.id
    assert cart.items[0].product_id == 100
    assert cart.items[0].quantity == 56


def test_remove_item_from_non_existent_cart(mock_jwt_decode, mutation, db):
    user_id = 3
    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=300, quantity=0)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    assert response.status_code == 200
    data = response.json()

    assert "data" in data
    assert data["data"] is None

    assert "errors" in data
    assert data["errors"][0]["message"] == "404: Cart not found"

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart is None


def test_remove_non_existent_item_from_cart(mock_jwt_decode, mutation, db):
    user_id = 1
    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=103, quantity=0)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    assert response.status_code == 200
    data = response.json()

    assert "data" in data
    assert data["data"] is None

    assert "errors" in data
    assert data["errors"][0]["message"] == "404: Cart item not found"

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart is not None
    assert len(cart.items) == 2


def test_remove_item_from_cart(mock_jwt_decode, mutation, db):
    user_id = 1
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert len(cart.items) == 2

    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=101, quantity=0)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {"addCartItem": {"id": 2, "cartId": 1, "productId": 101, "quantity": 0}}
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    db.refresh(cart)
    assert cart is not None
    assert len(cart.items) == 1


def test_remove_last_item_from_cart(mock_jwt_decode, mutation, db):
    user_id = 2
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert len(cart.items) == 1

    with mock_jwt_decode(user_id=user_id):
        mutation_query = mutation(product_id=200, quantity=0)
        response = client.post(
            "/graphql",
            json={"query": mutation_query},
            headers={"Authorization": "Bearer token"},
        )

    expected_response = {
        "data": {"addCartItem": {"id": 3, "cartId": 2, "productId": 200, "quantity": 0}}
    }

    assert response.status_code == 200
    data = response.json()
    assert data == expected_response

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    assert cart is None
