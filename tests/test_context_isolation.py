from app.coordinator.context_store import CoordinatorContextStore


def test_context_store_keeps_requests_isolated() -> None:
    store = CoordinatorContextStore()

    store.add_finding("request-1", "Finding for request one")
    store.add_finding("request-2", "Finding for request two")

    assert store.get_findings("request-1") == ["Finding for request one"]
    assert store.get_findings("request-2") == ["Finding for request two"]
    assert store.get_findings("unknown-request") == []
