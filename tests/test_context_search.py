from app.coordinator.context_store import CoordinatorContextStore


def test_context_store_search_and_clear() -> None:
    store = CoordinatorContextStore()

    store.add_finding("request-1", "Python uses indentation.")
    store.add_finding("request-1", "Docker packages applications.")

    python_findings = store.search_findings("request-1", "python")
    assert python_findings == ["Python uses indentation."]

    store.clear_request("request-1")
    assert store.get_findings("request-1") == []
