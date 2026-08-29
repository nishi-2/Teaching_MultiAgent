from app.coordinator.router import CoordinatorRouter


def test_router_always_selects_teaching_agent() -> None:
    router = CoordinatorRouter()

    agents = router.select_agents("What is Python?")

    assert agents == ["teaching_agent"]


def test_router_selects_pdf_agent() -> None:
    router = CoordinatorRouter()

    agents = router.select_agents("Teach me from my uploaded PDF.")

    assert "teaching_agent" in agents
    assert "pdf_rag_agent" in agents


def test_router_selects_web_and_github_agents() -> None:
    router = CoordinatorRouter()

    agents = router.select_agents(
        "Find the latest GitHub repository code example."
    )

    assert "teaching_agent" in agents
    assert "web_research_agent" in agents
    assert "github_agent" in agents
