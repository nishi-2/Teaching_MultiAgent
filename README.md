# AI Teaching Tutor

A Python and Streamlit application for learning AI, data science, Docker, FastAPI, and related technologies through evidence-grounded teaching.

The project is being developed as an end-to-end AI teaching service with OpenAI GPT integration, local PDF retrieval, web research, GitHub research, citations, evaluation, and deployment support.

## Project status

| Phase | Status |
| --- | --- |
| Phase 1: Project skeleton and deterministic Streamlit vertical slice | Complete |
| Phase 2: Coordinator-mediated orchestration | Complete |
| Phase 3: OpenAI GPT adapter and real model integration | Next |
| PDF RAG with Qdrant | Planned |
| Web research and citations | Planned |
| GitHub research | Planned |
| Evaluation and production hardening | Planned |
| Deployment | Planned |

## Current architecture

The application follows a strict Coordinator hub-and-spoke architecture:

```
User
  ↓
Streamlit
  ↓
Coordinator
  ├── Teaching Agent
  ├── PDF RAG Agent
  ├── Web Research Agent
  └── GitHub Agent
  ↓
Coordinator Context Store
  ↓
Streamlit response
```

The Coordinator is the central workflow controller. It creates tasks, selects agents, dispatches work, stores findings, shares approved context, aggregates results, handles failures, and returns the final response to the user interface.

Subagents may communicate with the Coordinator through the approved Coordinator Gateway. They may submit findings, request approved context, and request follow-up work through the Coordinator.

Subagents may not communicate directly with one another. They cannot access the agent registry, bypass Coordinator policies, send messages directly to the user, or execute unapproved tools.

The permitted communication pattern is:

```
Subagent → Coordinator Gateway → Coordinator Context Store

Coordinator → approved context → Subagent
```

The prohibited communication pattern is:

```
Subagent A → Subagent B
```

## Phase 1 implementation

Phase 1 created the initial Python and Streamlit project skeleton.

The project folder, Python virtual environment, dependency file, Git ignore rules, environment template, package directories, project configuration, settings module, domain models, base subagent interface, deterministic Teaching Agent, Coordinator, Streamlit entrypoint, smoke test, logging configuration, and README were created.

The initial application flow was:

```
Streamlit → Coordinator → Teaching Agent → Coordinator → Streamlit
```

The Teaching Agent in Phase 1 was a deterministic mock. It did not call an AI model or external service.

Phase 1 was validated by compiling the application and running the automated smoke test successfully.

## Phase 2 implementation

Phase 2 formalized the multiagent architecture.

Typed models were added for tutor requests, tutor responses, Coordinator tasks, subagent results, agent names, task status, approved context, follow-up objectives, and metadata.

A restricted Coordinator Gateway was created. It defines controlled operations for submitting findings, requesting approved context, and requesting follow-up work.

A central Coordinator context store was implemented. It groups findings by parent request and supports adding findings, retrieving findings, searching findings by topic, and clearing completed request context.

The Coordinator was updated to maintain task-to-request relationships, accept findings from subagents, return approved context, use a router, dispatch registered agents, aggregate findings, and handle failed agents.

A deterministic router was added for selecting the Teaching, PDF RAG, Web Research, and GitHub agents based on the user question.

Temporary PDF, Web Research, and GitHub stubs were added so routing and multiagent dispatch could be tested before implementing real retrieval logic.

Phase 2 tests cover communication models, mediated context exchange, routing, multiagent dispatch, PDF-agent dispatch, failure handling, request isolation, context search, context cleanup, and the complete Streamlit workflow.

## Current temporary limitations

The Teaching Agent is still deterministic and does not yet call OpenAI GPT.

The PDF RAG, Web Research, and GitHub agents are temporary stubs. They do not yet retrieve real documents, websites, repositories, or code examples.

Qdrant has not yet been connected to the application.

Citation verification has not yet been implemented.

The Coordinator currently dispatches the registered agents sequentially. More advanced parallel execution, retries, timeout enforcement, evidence normalization, and verification will be added in later phases.

The application does not execute code retrieved from GitHub or other sources.

## Planned technology stack

| Area | Planned technology |
| --- | --- |
| Language | Python 3.10.8 or later |
| User interface | Streamlit |
| Initial model provider | OpenAI GPT |
| Initial default model | `gpt-5-mini` |
| Vector database | Qdrant |
| PDF processing | Python PDF extraction library |
| Testing | pytest |
| Formatting and quality | Ruff and mypy |
| Containerization | Docker and Docker Compose |
| Initial deployment style | Private Dockerized deployment |

The OpenAI model name will be configured through environment variables so it can be changed without modifying agent code. The application will also use mock model clients in tests so tests do not require API access.

## Planned final workflow

```
User question
    ↓
Streamlit interface
    ↓
Coordinator validates and routes the request
    ├── Teaching Agent
    ├── PDF RAG Agent
    ├── Web Research Agent
    └── GitHub Agent
    ↓
Coordinator aggregates evidence
    ↓
Citation and Fact Checker
    ↓
Coordinator approves or requests revision
    ↓
Answer Composer
    ↓
Coordinator final policy check
    ↓
Streamlit answer with citations and exercises
```

All results will return to the Coordinator before being passed to another agent. For example, the Web Research Agent will return documentation findings to the Coordinator. If the Teaching Agent needs those findings, the Coordinator will provide approved context in a new task.

## Local setup

Create and activate a virtual environment in Windows CMD:

```
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

When external model configuration is needed, copy the environment template:

```
copy .env.example .env
```

Never commit the real `.env` file or any API key.

## Run the application

From the project root:

```
streamlit run streamlit_app.py
```

The current application accepts a question, sends it to the Coordinator, dispatches the Teaching Agent or relevant temporary stubs, and displays the aggregated response.

## Run tests

```
pytest -q
```

The Phase 2 test suite currently covers the Coordinator, context store, router, temporary agents, failure behavior, and request isolation.

## Project directories

```
app/          Application source code
  agents/     Subagent implementations
  config/     Environment and logging configuration
  coordinator/Coordinator, routing, gateway, and context store
  domain/     Typed communication models
  llm/        Planned model adapters
  ui/         Planned reusable Streamlit components

data/         Local documents, generated data, storage, and logs
tests/        Unit and integration tests
scripts/      Planned command-line utilities
docs/         Architecture, deployment, security, and evaluation documentation
```

## Development principles

The project is being built incrementally. Each phase must produce a runnable and testable result before the next phase begins.

The system will prefer evidence over unsupported claims. Retrieved claims should contain source provenance, and the final answer should distinguish retrieved evidence from general explanation.

Untrusted content from PDFs, websites, and repositories will be treated as data, not instructions. Retrieved code will not be executed automatically.

The Coordinator will enforce subagent permissions, execution limits, context boundaries, and final-answer quality checks.

## Next phase

Phase 3 will implement the OpenAI GPT adapter and replace the deterministic Teaching Agent with a real GPT-backed agent.

The first Phase 3 objectives are to centralize OpenAI client configuration, add structured model responses, add usage tracking, add error handling, and preserve the existing mock-based tests.

## Documentation records

- `process_followed.md` — Phase 1 process record

- `phase_2_process_followed.md` — Phase 2 process record

- `README.md` — Project overview and current status