# AI Teaching Tutor

A Python and Streamlit application for learning AI, data science, Docker, FastAPI, and related technologies through evidence-grounded teaching.

The project is being developed as an end-to-end AI teaching service with OpenAI GPT integration, Coordinator-mediated multiagent orchestration, local PDF retrieval, web research, GitHub research, citations, evaluation, and deployment support.

## Project status

| Phase | Status |
| --- | --- |
| Phase 1: Project skeleton and deterministic Streamlit vertical slice | Complete |
| Phase 2: Coordinator-mediated orchestration | Complete |
| Phase 3: OpenAI GPT adapter and real model integration | Complete |
| Phase 4: PDF ingestion and Qdrant-backed RAG | Complete |
| Phase 5: Web research and source retrieval | Next |
| Phase 6: Evidence-grounded citations and verification | Planned |
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

Phase 1 created the initial Python and Streamlit project skeleton. The project folder, Python virtual environment, dependency file, Git ignore rules, environment template, package directories, project configuration, settings module, domain models, base subagent interface, deterministic Teaching Agent, Coordinator, Streamlit entrypoint, smoke test, logging configuration, and README were created.

The initial application flow was:

```
Streamlit → Coordinator → Teaching Agent → Coordinator → Streamlit
```

Phase 1 was validated by compiling the application and running the automated smoke test successfully.

## Phase 2 implementation

Phase 2 formalized the multiagent architecture. Typed communication models were added for tutor requests, tutor responses, Coordinator tasks, subagent results, agent names, task status, approved context, follow-up objectives, and metadata.

A restricted Coordinator Gateway was created. It defines controlled operations for submitting findings, requesting approved context, and requesting follow-up work.

A central Coordinator context store was implemented. It groups findings by parent request and supports adding, retrieving, searching, and clearing findings.

The Coordinator was updated to maintain task-to-request relationships, accept findings from subagents, return approved context, use a router, dispatch registered agents, aggregate findings, and handle failed agents.

A deterministic router was added for selecting the Teaching, PDF RAG, Web Research, and GitHub agents based on the user question. Temporary PDF, Web Research, and GitHub stubs were added so routing and multiagent dispatch could be tested before implementing real retrieval logic.

Phase 2 was validated with tests covering communication models, mediated context exchange, routing, multiagent dispatch, PDF-agent dispatch, failure handling, request isolation, context search, context cleanup, and the Streamlit workflow.

## Phase 3 implementation

Phase 3 integrated OpenAI GPT while preserving the Coordinator architecture and keeping automated tests independent of external API calls.

The default teaching model is configurable and currently set to `gpt-5-mini`. The model name is read from environment variables rather than being hardcoded throughout the application.

A centralized OpenAI client adapter was created. It handles model configuration, Chat Completions requests, completion limits, visible-response validation, and token usage extraction.

A typed usage record was added for prompt tokens, completion tokens, and total tokens. Structured JSON Schema output support was also added for future Coordinator plans, evidence records, citation reports, and answer models.

A GPT-backed Teaching Agent was created. It builds the teaching prompt, includes learner level, invokes the centralized OpenAI adapter, submits the answer to the Coordinator, and returns usage metadata.

The GPT Teaching Agent is testable through dependency injection. Automated tests use fake LLM adapters and do not call OpenAI.

The Streamlit application now uses the GPT Teaching Agent for real questions and displays controlled errors when the model returns an empty response or when a runtime failure occurs.

Phase 3 was validated through real Streamlit requests and automated tests covering the model adapter, usage tracking, structured output, GPT Teaching Agent, empty responses, learner-level prompting, and the existing Coordinator workflow.

## Phase 4 implementation

Phase 4 added local PDF ingestion, OpenAI embeddings, Qdrant vector storage, active-document isolation, Streamlit document upload, and PDF-grounded GPT teaching.

A document metadata model was created to track filenames, paths, hashes, statuses, page counts, chunk counts, errors, and timestamps. PDF page extraction and page-aware chunking preserve the source page for future citations.

SHA-256 document hashing and a JSON ingestion manifest were added to detect document identity and persist indexing status. The document indexer connects extraction, chunking, embeddings, Qdrant upsert, and manifest persistence.

An interchangeable embedding interface and an OpenAI embedding provider were implemented. Real embedding generation was verified successfully, producing 1,536-dimensional vectors for the configured embedding model.

Qdrant was added through Docker Compose with persistent local storage. The Qdrant store supports collection creation, vector upsert, payload metadata, similarity search, optional document filtering, and compatibility with test doubles.

A real PDF RAG Agent was implemented. It embeds the user question, searches Qdrant, validates results through the typed PDF evidence model, applies a similarity threshold, and submits page-aware findings only through the Coordinator.

The Coordinator now collects retrieval evidence before invoking the GPT Teaching Agent. Approved findings are passed through the task context, and raw retrieval chunks are not returned as the final user-facing answer.

Active-document isolation was added. Streamlit stores the document ID returned after indexing, attaches it to each Tutor Request, and the PDF RAG Agent restricts Qdrant retrieval to that document. This prevents older documents, including earlier test content, from contaminating answers about a newly uploaded PDF.

Streamlit now supports PDF upload, safe filename handling, save-and-index actions, indexing status, indexed-document listing, active-document tracking, and PDF-grounded questions.

Phase 4 was validated through automated tests and real Streamlit verification covering PDF extraction, chunking, hashing, manifests, embeddings, Qdrant operations, indexing, evidence validation, similarity thresholds, upload safety, active-document filtering, Coordinator-to-GPT evidence flow, and document-status display.

## Current workflow

```
User uploads PDF
        ↓
Streamlit saves PDF
        ↓
Document indexer extracts pages and chunks
        ↓
OpenAI embedding provider creates vectors
        ↓
Qdrant stores vectors and page-aware metadata
        ↓
User asks a question
        ↓
Coordinator identifies the active document
        ↓
PDF RAG Agent searches only that document
        ↓
Coordinator passes approved evidence to GPT
        ↓
GPT Teaching Agent explains the evidence
        ↓
Streamlit displays the teaching answer
```

## Current temporary limitations

Web research and GitHub research remain temporary stubs. They do not yet retrieve live websites, official documentation, repositories, or code examples.

Formal citation verification and cross-source evidence normalization have not yet been implemented. PDF findings currently preserve filename, page number, excerpt, and similarity metadata, but final citation-quality enforcement is a later phase.

The application currently uses OpenAI for teaching completions and embeddings and requires a configured API key for real requests. Automated tests use fake clients to avoid external calls.

The Coordinator currently dispatches registered agents sequentially. More advanced parallel execution, retries, timeout enforcement, source freshness checks, and verification will be added later.

The local Qdrant and document filesystem are suitable for development and private deployment. Public deployment requires a deliberate persistence and privacy strategy for uploaded documents and vector storage.

The application does not execute code retrieved from GitHub or other sources.

## Technology stack

| Area | Technology |
| --- | --- |
| Language | Python 3.10.8 or later |
| User interface | Streamlit |
| Teaching model provider | OpenAI GPT |
| Default teaching model | `gpt-5-mini` |
| Embedding provider | OpenAI embeddings |
| Default embedding model | `text-embedding-3-small` |
| Vector database | Qdrant |
| PDF processing | `pypdf` |
| Testing | pytest |
| Formatting and quality | Ruff and mypy |
| Containerization | Docker and Docker Compose |
| Initial deployment style | Private Dockerized deployment |

Model names, API keys, Qdrant connection details, retrieval thresholds, document paths, and logging levels are configured through environment variables. The application supports fake model and retrieval clients in tests.

## Planned final workflow

```
User question
    ↓
Streamlit interface
    ↓
Coordinator validates and routes the request
    ├── PDF RAG Agent
    ├── Web Research Agent
    ├── GitHub Agent
    └── GPT Teaching Agent
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

All results return to the Coordinator before being passed to another agent. If the GPT Teaching Agent needs PDF, web, or GitHub findings, the Coordinator provides approved context in a new task.

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

## Start Qdrant

Docker Desktop must be running. From the project root:

```
docker compose up -d qdrant
```

## Run the application

From the project root:

```
streamlit run streamlit_app.py
```

The current application supports GPT teaching, PDF upload, PDF indexing, indexed-document status, active-document filtering, and PDF-grounded responses.

## Run tests

```
pytest -q
```

The test suite covers the Coordinator, context store, router, temporary agents, failure behavior, OpenAI adapter, structured output, GPT Teaching Agent, PDF extraction, chunking, hashing, manifests, embeddings, Qdrant operations, indexing, evidence validation, upload safety, document isolation, and end-to-end grounding.

## Manual connectivity checks

Run the OpenAI GPT check from the project root:

```
python -m scripts.test_openai_connection
```

Run the OpenAI embedding check:

```
python -m scripts.test_openai_embeddings
```

Run the Qdrant connection check:

```
python -m scripts.test_qdrant_connection
```

Index the sample PDF manually:

```
python -m scripts.index_sample_pdf
```

These scripts perform real local or external operations and should not be included in the normal pytest suite.

## Project directories

```
app/          Application source code
  agents/     Subagent implementations
  config/     Environment and logging configuration
  coordinator/Coordinator, routing, gateway, and context store
  domain/     Typed communication, document, and evidence models
  ingestion/  Hashing, manifests, and document indexing
  llm/        OpenAI model adapters, structured output, and usage tracking
  retrieval/  PDF extraction, chunking, embeddings, and Qdrant storage
  ui/         Streamlit upload and document-management helpers

data/        Local documents, generated data, storage, and logs
tests/        Unit and integration tests
scripts/      Manual command-line utilities
docs/         Architecture, deployment, security, and evaluation documentation
```

## Development principles

The project is built incrementally. Each phase must produce a runnable and testable result before the next phase begins.

The system prefers evidence over unsupported claims. Retrieved claims should contain source provenance, and the final answer should distinguish retrieved evidence from general explanation.

Untrusted content from PDFs, websites, and repositories is treated as data, not instructions. Retrieved code is not executed automatically.

The Coordinator enforces subagent permissions, context boundaries, and final-answer control. Model calls are centralized, usage is measured, and automated tests use fake clients where external access is unnecessary.

The active document must be explicitly tracked when the user asks about an uploaded PDF. Retrieval must not silently combine unrelated documents.

## Documentation records

- `process_followed.md` — Phase 1 process record

- `phase_2_process_followed.md` — Phase 2 process record

- `phase_3_process_followed.md` — Phase 3 process record

- `phase_4_process_followed.md` — Phase 4 process record

- `README.md` — Project overview and current status

## Next phase

Phase 5 will implement controlled web research. The Web Research Agent will search for relevant pages, fetch source content, normalize passages, preserve URLs and retrieval metadata, and return findings to the Coordinator. The Coordinator will then decide what information can be passed to the GPT Teaching Agent and future Citation Agent.

**Author:** Manus AI