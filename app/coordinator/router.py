from typing import List


class CoordinatorRouter:
    """Selects subagents based on the user question."""

    def select_agents(self, question: str) -> List[str]:
        normalized_question = question.lower()
        selected_agents = ["teaching_agent"]

        if any(keyword in normalized_question for keyword in ["pdf", "document", "notes", "uploaded"]):
            selected_agents.append("pdf_rag_agent")

        if any(keyword in normalized_question for keyword in ["latest", "current", "documentation", "version"]):
            selected_agents.append("web_research_agent")

        if any(keyword in normalized_question for keyword in ["github", "repository", "repo", "code example"]):
            selected_agents.append("github_agent")

        return selected_agents
