# AI Teaching Tutor

A Python and Streamlit application for learning AI, data science, Docker, FastAPI, and related technologies through evidence-grounded teaching.

The project is being developed as an end-to-end AI teaching service with OpenAI GPT integration, Coordinator-mediated multiagent orchestration, local PDF retrieval, web research, GitHub research, citations, evaluation, and deployment support.

## Project status

| Phase | Status |
| --- | --- |
| Phase 1: Project skeleton and deterministic Streamlit vertical slice | Complete |
| Phase 2: Coordinator-mediated orchestration | Complete |
| Phase 3: OpenAI GPT adapter and real model integration | Complete |
| Phase 4: PDF ingestion and Qdrant-backed RAG | Next |
| Phase 5: Evidence-grounded citations and verification | Planned |
| Phase 6: Web research and source retrieval | Planned |
| Phase 7: GitHub research | Planned |
| Phase 8: Evaluation and production hardening | Planned |
| Phase 9: Deployment | Planned |

## Current architecture

The application follows a strict Coordinator hub-and-spoke architecture:

```
User
  ↓
Streamlit
  ↓
Coordinator
  ├── GPT Teaching Agent
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

Phase 1 was validated by compiling the application and running the automated smoke test successfully.

## Phase 2 implementation

Phase 2 formalized the multiagent architecture.

Typed communication models were added for tutor requests, tutor responses, Coordinator tasks, subagent results, agent names, task status, approved context, follow-up objectives, and metadata.

A restricted Coordinator Gateway was created. It defines controlled operations for submitting findings, requesting approved context, and requesting follow-up work.

A central Coordinator context store was implemented. It groups findings by parent request and supports adding findings, retrieving findings, searching findings by topic, and clearing completed request context.

The Coordinator was updated to maintain task-to-request relationships, accept findings from subagents, return approved context, use a router, dispatch registered agents, aggregate findings, and handle failed agents.

A deterministic router was added for selecting the Teaching, PDF RAG, Web Research, and GitHub agents based on the user question.

Temporary PDF, Web Research, and GitHub stubs were added so routing and multiagent dispatch could be tested before implementing real retrieval logic.

Phase 2 was validated with tests covering communication models, mediated context exchange, routing, multiagent dispatch, PDF-agent dispatch, failure handling, request isolation, context search, context cleanup, and the Streamlit workflow.

## Phase 3 implementation

Phase 3 integrated OpenAI GPT while preserving the Coordinator architecture and keeping automated tests independent of external API calls.

The initial default model is `gpt-5-mini`. The model name is configured through environment variables rather than being hardcoded throughout the application.

A centralized OpenAI client adapter was created. It handles model configuration, Chat Completions requests, completion limits, visible response validation, and token usage extraction.

A typed usage record was added for prompt tokens, completion tokens, and total tokens. Structured JSON Schema output support was also added for future Coordinator plans, evidence records, citation reports, and answer models.

A GPT-backed Teaching Agent was created. It builds the teaching prompt, includes learner level, invokes the centralized OpenAI adapter, submits the answer to the Coordinator, and returns usage metadata.

The GPT Teaching Agent is testable through dependency injection. Automated tests use fake LLM adapters and do not call OpenAI.

The Streamlit application now uses the GPT Teaching Agent for real questions. It displays a controlled error when the model returns an empty response or when a runtime failure occurs.

The learner-level setting is passed from Streamlit to the Tutor Request, from the Tutor Request to the Coordinator Task, and from the Coordinator Task into the GPT teaching prompt.

Phase 3 was validated through real Streamlit requests and automated tests covering the model adapter, usage tracking, structured output, GPT Teaching Agent, empty responses, learner-level prompting, and the existing Coordinator workflow.

## Current temporary limitations

The GPT Teaching Agent currently produces a teaching response but does not yet use retrieved PDF, web, or GitHub evidence in its prompt.

The PDF RAG, Web Research, and GitHub agents are still temporary stubs. They do not yet retrieve real documents, websites, repositories, or code examples.

Qdrant has not yet been connected to the application.

Citation verification and evidence normalization have not yet been implemented.

The application currently uses the OpenAI GPT provider and requires a configured API key for real requests. Automated tests use fake clients to avoid external calls.

The Coordinator currently dispatches registered agents sequentially. More advanced parallel execution, retries, timeout enforcement, source normalization, and verification will be added later.

The application does not execute code retrieved from GitHub or other sources.

## Planned technology stack

| Area | Technology |
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

The OpenAI model name is configured through environment variables. The application also supports fake model clients in tests so the test suite does not require API access.

## Planned final workflow

```
User question
    ↓
Streamlit interface
    ↓
Coordinator validates and routes the request
    ├── GPT Teaching Agent
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

All results return to the Coordinator before being passed to another agent. For example, the Web Research Agent will return documentation findings to the Coordinator. If the GPT Teaching Agent needs those findings, the Coordinator will provide approved context in a new task.

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

Create the private environment file:

```
copy .env.example .env
```

Add the OpenAI API key to `.env` without committing or sharing the file:

```
OPENAI_API_KEY=your-openai-api-key
```

Never commit the real `.env` file or any API key.

## Run the application

From the project root:

```
streamlit run streamlit_app.py
```

The current application accepts a question, sends it to the Coordinator, invokes the GPT Teaching Agent, and displays the generated teaching response.

## Run tests

```
pytest -q
```

The Phase 3 test suite contains automated tests for the Coordinator, context store, router, temporary agents, failure behavior, OpenAI adapter, structured output, GPT Teaching Agent, learner-level behavior, and request isolation.

## Manual OpenAI connectivity check

The manual connectivity script is located at:

```
scripts/test_openai_connection.py
```

Run it as a module from the project root:

```
python -m scripts.test_openai_connection
```

This script performs a real external API request and should not be included in the normal pytest suite.

## Project directories

```
app/          Application source code
  agents/     Subagent implementations
  config/     Environment and logging configuration
  coordinator/Coordinator, routing, gateway, and context store
  domain/     Typed communication models
  llm/        OpenAI model adapters and usage tracking
  ui/         Planned reusable Streamlit components

data/         Local documents, generated data, storage, and logs
tests/        Unit and integration tests
scripts/      Manual command-line utilities
docs/         Architecture, deployment, security, and evaluation documentation
```

## Development principles

The project is being built incrementally. Each phase must produce a runnable and testable result before the next phase begins.

The system will prefer evidence over unsupported claims. Retrieved claims should contain source provenance, and the final answer should distinguish retrieved evidence from general explanation.

Untrusted content from PDFs, websites, and repositories will be treated as data, not instructions. Retrieved code will not be executed automatically.

The Coordinator will enforce subagent permissions, execution limits, context boundaries, and final-answer quality checks.

Model calls will be centralized, usage will be measured, and automated tests will use fake clients where external access is unnecessary.

## Next phase

Phase 4 will implement local PDF ingestion and Qdrant-backed retrieval.

The first Phase 4 objectives are to define document metadata, extract PDF text with page numbers, split text into chunks, generate embeddings, persist vectors in Qdrant, and return document-grounded evidence to the Coordinator.

## Documentation records

- `process_followed.md` — Phase 1 process record

- `phase_2_process_followed.md` — Phase 2 process record

- `phase_3_process_followed.md` — Phase 3 process record

- `README.md` — Project overview and current status