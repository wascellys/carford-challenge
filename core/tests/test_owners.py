import json


def test_owners_list_200(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/v1/owners")

    assert resp.status_code == 200


def test_owner_post_201(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/v1/owners",
        content_type="application/json",
        data=json.dumps({
            "name": "Edy",
        })
    )

    assert resp.status_code == 201


def test_owner_get_200(test_app, test_database, add_owner):
    _owner = add_owner("test_owner_get_200")
    client = test_app.test_client()
    resp = client.get(f"/v1/owners/{_owner.id}")

    assert resp.status_code == 200


def test_owner_get_404(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/v1/owners/3242")
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404


def test_owner_put_200(test_app, test_database, add_owner):

    _owner = add_owner("test_owner_put_200")
    client = test_app.test_client()
    resp = client.put(
        f"/v1/owners/{_owner.id}",
        content_type="application/json",
        data=json.dumps({
            "name": "Wascellys"
        })
    )

    assert resp.status_code == 200


def test_owner_put_404(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/v1/owners/342343",
        content_type="application/json",
        data=json.dumps({
            "name": "Ferreira",
        })
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404


def test_owner_delete_204(test_app, test_database, add_owner):

    _owner = add_owner("test_owner_delete_204")
    client = test_app.test_client()
    resp = client.delete(f"/v1/owners/{_owner.id}")

    assert resp.status_code == 204

def test_owner_delete_404(test_app, test_database):

    client = test_app.test_client()
    resp = client.delete("/api/v1/owners/343243")
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404

