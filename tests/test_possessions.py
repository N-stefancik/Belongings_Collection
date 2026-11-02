"""End-to-end API tests for the first project milestone."""

from uuid import uuid4


def create(client, name="Camera", **extra):
    response = client.post("/possessions", json={"name": name, **extra})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_and_retrieve(client):
    item = create(client, "Guitar", category="Instruments", attributes={"year": 2018})
    result = client.get(f"/possessions/{item['id']}")
    assert result.status_code == 200
    assert result.json()["name"] == "Guitar"
    assert result.json()["attributes"] == {"year": 2018}
    assert result.json()["created_at"]


def test_list_and_pagination(client):
    create(client, "Camera")
    create(client, "Ring")
    create(client, "Book")
    all_items = client.get("/possessions").json()
    assert len(all_items) == 3
    assert len(client.get("/possessions?limit=2&offset=1").json()) == 2
    assert client.get("/possessions?limit=0").status_code == 422


def test_update_only_requested_fields(client):
    item = create(client, "Camera", category="Electronics")
    response = client.patch(f"/possessions/{item['id']}", json={"description": "Vintage"})
    assert response.status_code == 200
    assert response.json()["name"] == "Camera"
    assert response.json()["category"] == "Electronics"
    assert response.json()["description"] == "Vintage"


def test_delete(client):
    item = create(client)
    assert client.delete(f"/possessions/{item['id']}").status_code == 204
    assert client.get(f"/possessions/{item['id']}").status_code == 404


def test_invalid_inputs(client):
    for payload in [{"name": ""}, {"name": "  "}, {"name": 123}, {"name": "Valid", "surprise": 1}]:
        assert client.post("/possessions", json=payload).status_code == 422
    item = create(client)
    assert client.patch(f"/possessions/{item['id']}", json={"name": None}).status_code == 422
    assert client.patch(f"/possessions/{item['id']}", json={"attributes": None}).status_code == 422


def test_not_found(client):
    missing = str(uuid4())
    assert client.get(f"/possessions/{missing}").status_code == 404
    assert client.patch(f"/possessions/{missing}", json={"name": "None"}).status_code == 404
    assert client.delete(f"/possessions/{missing}").status_code == 404
    assert client.get("/possessions/not-a-uuid").status_code == 422


def test_persistence_across_connections(client):
    item = create(client, "Heirloom watch")
    # Each API request obtains a new session; the saved item must remain accessible.
    assert client.get(f"/possessions/{item['id']}").json()["name"] == "Heirloom watch"


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
