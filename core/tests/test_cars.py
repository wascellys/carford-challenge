import json


def test_cars_list_200(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/v1/cars")

    assert resp.status_code == 200


def test_car_post_201(test_app, test_database, add_owner):
    client = test_app.test_client()
    owner = add_owner("Edy")
    resp = client.post(
        "/v1/cars",
        content_type="application/json",
        data=json.dumps({
            "name": "Ferrari", "color": "Blue", "model": "Sedan", "owner_id": owner.id
        })
    )

    assert resp.status_code == 201


def test_car_post_invalid_model(test_app, test_database, add_owner):
    client = test_app.test_client()
    owner = add_owner("Edy")
    resp = client.post(
        "/v1/cars",
        content_type="application/json",
        data=json.dumps({
            "name": "Ferrari", "color": "Blue", "model": "SUV", "owner_id": owner.id
        })
    )

    assert resp.status_code == 500


def test_car_post_invalid_color(test_app, test_database, add_owner):
    client = test_app.test_client()
    owner = add_owner("Edy")
    resp = client.post(
        "/v1/cars",
        content_type="application/json",
        data=json.dumps({
            "name": "Ferrari", "color": "Brown", "model": "Sedan", "owner_id": owner.id
        })
    )

    assert resp.status_code == 500


def test_car_get_200(test_app, test_database, add_car, add_owner):
    owner = add_owner("Edy")
    _car = add_car(name="test_car_get_200", color="Blue", model="Sedan", owner_id=owner.id)
    client = test_app.test_client()
    resp = client.get(f"/v1/cars/{_car.id}")

    assert resp.status_code == 200


def test_car_get_404(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/v1/cars/3242")
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404


def test_car_put_200(test_app, test_database, add_car, add_owner):
    owner = add_owner("Wascellys")
    _car = add_car(name="test_car_put_200", color="Blue", model="Sedan", owner_id=owner.id)
    client = test_app.test_client()
    resp = client.put(
        f"/v1/cars/{_car.id}",
        content_type="application/json",
        data=json.dumps({
            "name": "Wascellys",
            "color": "Blue",
            "model": "Sedan",
            "owner_id": owner.id
        })
    )

    assert resp.status_code == 200


def test_car_put_404(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/v1/cars/342343",
        content_type="application/json",
        data=json.dumps({
            "name": "Wascellys",
            "color": "Blue",
            "model": "Sedan",
            "owner_id": 9999
        })
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404


def test_car_delete_204(test_app, test_database, add_car, add_owner):
    owner = add_owner("Ferreira")
    _car = add_car(name="test_car_delete_204", color="Blue", model="Sedan", owner_id=owner.id)
    client = test_app.test_client()
    resp = client.delete(f"/v1/cars/{_car.id}")

    assert resp.status_code == 204


def test_car_delete_404(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/v1/cars/343243")
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
