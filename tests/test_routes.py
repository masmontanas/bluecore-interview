import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture(scope="module")
def client():
    app = create_app()
    return TestClient(app)


def test_healthcheck_returns_200(client):
    response = client.get("/healthz")
    assert response.status_code == 200


def test_redis_circuit_breaker_trips_for_get(client, caplog):
    """
    A bit hacky, though we don't want to expose details specific to redis being unavailable
    in the response for security reasons, so we'll parse the logs to verify that the circuit
    breaker has been tripped.
    # TODO: Improve this test and related functionality to better infer circuit breaker state.
    """

    caplog.set_level("WARNING")

    for _ in range(3):
        res = client.get("/read")
        assert res.status_code == 503

    res = client.get("/read")
    assert res.status_code == 503
    assert any("Circuit breaker opened" in m for m in caplog.messages)


def test_redis_circuit_breaker_trips_for_post(client, caplog):
    """
    A bit hacky, though we don't want to expose details specific to redis being unavailable
    in the response for security reasons, so we'll parse the logs to verify that the circuit
    breaker has been tripped.
    # TODO: Improve this test and related functionality to better infer circuit breaker state.
    """

    caplog.set_level("WARNING")

    for _ in range(3):
        res = client.post("/write")
        assert res.status_code == 503

    res = client.post("/write")
    assert res.status_code == 503
    assert any("Circuit breaker is OPEN," in m for m in caplog.messages)
