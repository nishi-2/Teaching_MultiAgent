# AI Teaching Tutor — Phase 1 Process Followed

## Phase 1 objective

The objective of Phase 1 was to create a working Python and Streamlit project skeleton with a deterministic teaching workflow. The initial workflow was intentionally kept small so that the project could be validated before adding OpenAI GPT, PDF RAG, web research, GitHub research, and advanced multiagent orchestration.

The completed Phase 1 workflow is:

```
Streamlit interface → Coordinator → Teaching Agent → Coordinator → Streamlit response
```

The Teaching Agent used in this phase is a deterministic mock. It does not yet call an AI model.

### Step 1: Create the project folder

A dedicated project folder named `ai-teaching-tutor` was created (in my local). This folder is the root directory for the application, source code, tests, configuration, data, and documentation.

### Step 2: Create the Python virtual environment

A project-specific Python virtual environment was created. The environment isolates this project’s dependencies from other Python projects on the computer.

The project was configured to support Python 3.10 and later.

### Step 3: Create the dependency file

A dependency file named `requirements.txt` was created. It lists the libraries that will be used throughout the project, including Streamlit, Pydantic Settings, OpenAI integration, Qdrant support, PDF processing, HTTP communication, testing, formatting, and type checking.

The dependencies were installed inside the project virtual environment.

### Step 4: Create the Git ignore file

A `.gitignore` file was created. It prevents virtual-environment files, Python caches, local secrets, generated document data, vector database storage, logs, and temporary database files from being committed to Git.

### Step 5: Create the environment variable

An `.env` file was created. It has the configuration variables that will eventually control the OpenAI model, Qdrant connection, document directory, collection name, and logging level.

This is the .env file structure -
-- OPENAI_API_KEY=<your key here>
-- OPENAI_MODEL=gpt-5-mini
-- OPENAI_REASONING_EFFORT=minimal
-- QDRANT_URL=http://localhost:6333
-- QDRANT_COLLECTION=ai_tutor_documents
-- DOCUMENTS_DIR=data/documents
-- LOG_LEVEL=INFO

### Step 6: Create the initial project directories

The initial application, test, and data directories were created. These directories establish the foundation for configuration, domain models, Coordinator logic, agents, LLM integration, user interface components, tests, documents, extracted text, manifests, and logs.

### Step 7: Create Python package files

Python package initialization files were added to the application folders. This allows the application modules to be imported consistently as Python packages.

### Step 8: Create the project configuration file

A `pyproject.toml` file was created. It defines the project metadata, build configuration, Python version requirement, pytest configuration, formatting line length, and package configuration.

### Step 9: Create the settings module

A centralized settings module was created at `app/config/settings.py`. It loads configuration values from the environment and provides safe defaults for development.

This establishes one place for application configuration instead of scattering configuration values across the codebase.

### Step 10: Create the initial domain models

The first domain models were created at `app/domain/messages.py`. These models represent a tutor request, tutor response, Coordinator task, and subagent result.

Using typed models establishes a consistent structure for communication between the Streamlit interface, Coordinator, and agents.

### Step 11: Create the restricted subagent interface

A base subagent interface was created at `app/agents/base.py`. It defines the common behavior expected from a subagent: receiving an assigned Coordinator task and returning a structured result.

The interface does not provide direct subagent-to-subagent communication.

### Step 12: Create the mock Teaching Agent

A deterministic Teaching Agent was created at `app/agents/teaching_agent.py`. It receives a task from the Coordinator and returns a simple teaching-plan finding based on the user’s question.

This mock agent allows the orchestration flow to be tested without depending on an external model or API key.

### Step 13: Create the initial Coordinator

A Coordinator was created at `app/coordinator/coordinator.py`. It receives a tutor request, creates a task, delegates the task to the Teaching Agent, receives the result, handles a failed result, and converts a successful result into a tutor response.

The Coordinator is the central workflow component.

A future refinement will add a restricted Coordinator interaction interface. This will allow subagents to submit findings, request approved context from the Coordinator, and request follow-up work through the Coordinator without directly contacting other subagents.

### Step 14: Create the Streamlit application

The Streamlit entrypoint was created at `streamlit_app.py`. It provides a page title, learner-level selector, question input, Ask Tutor button, Coordinator initialization, and tutor response display.

The Streamlit application was successfully launched in the browser and tested with a sample question.

### Step 15: Add the first automated test

A smoke test was created at `tests/test_smoke.py`. It verifies that the Coordinator can receive a tutor request, delegate to the Teaching Agent, return a successful response, and include the requested topic in the response.

### Step 16: Add application logging

A logging configuration module was created at `app/config/logging_config.py`. It establishes a consistent log format and allows the logging level to be controlled through configuration.

### Step 17: Connect logging to Streamlit

The Streamlit entrypoint was updated to initialize logging and record when a tutor question is received.

The application was restarted and verified after the logging integration.

### Step 18: Create the project README

A `README.md` file was created. It documents the project’s current status, the Phase 1 workflow, local setup, application startup command, and test command.

### Step 19: Run complete Phase 1 validation

The Python source files were compiled to check for syntax errors. The automated test suite was then run.

The Phase 1 validation completed successfully with one passing smoke test.

## Phase 1 result

Phase 1 produced a working deterministic vertical slice:

```
User question
    ↓
Streamlit
    ↓
Coordinator
    ↓
Teaching Agent
    ↓
Coordinator
    ↓
Streamlit response
```

The application currently does not yet use OpenAI GPT, Qdrant, PDF documents, web research, GitHub research, citation verification, or production deployment. Those capabilities will be implemented in later phases.

## Files created or updated during Phase 1

| File or directory | Purpose |
| --- | --- |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from Git |
| `.env.example` | Configuration template |
| `pyproject.toml` | Project and tool configuration |
| `streamlit_app.py` | Streamlit application entrypoint |
| `app/config/settings.py` | Environment-based settings |
| `app/config/logging_config.py` | Logging configuration |
| `app/domain/messages.py` | Initial typed domain models |
| `app/agents/base.py` | Base subagent interface |
| `app/agents/teaching_agent.py` | Deterministic mock Teaching Agent |
| `app/coordinator/coordinator.py` | Initial Coordinator workflow |
| `tests/test_smoke.py` | Phase 1 smoke test |
| `README.md` | Project documentation |
| `app/*/__init__.py` | Python package initialization |
| `data/*` | Document, generated-data, storage, and log directories |

## Deferred work

The restricted `CoordinatorGateway` and mediated context exchange are intentionally deferred to the appropriate later part of the plan. The current implementation establishes the initial Coordinator-to-subagent-to-Coordinator flow, while future phases will allow subagents to request and receive approved findings through the Coordinator.

## Phase 1 completion status

**Status:** Complete.

**Next phase:** Implement the formal Coordinator task flow, mediated context exchange, and stronger subagent communication contracts.



# AI Teaching Tutor — Phase 2 Process Followed

## Phase 2 objective

The objective of Phase 2 was to formalize the Coordinator-mediated multiagent architecture. The Phase 1 application already had a basic Streamlit interface, Coordinator, and deterministic Teaching Agent. Phase 2 expanded that foundation with typed task communication, a central context store, controlled subagent interaction, routing, multiagent dispatch, failure handling, isolation tests, and Streamlit verification.

The completed Phase 2 workflow is:

```
User → Streamlit → Coordinator → Selected Subagents → Coordinator → Streamlit response
```

The Coordinator remains the central control point. Subagents communicate with the Coordinator but do not communicate directly with one another.

### Step 1: Upgrade the communication models

The shared communication models were expanded to support the growing multiagent workflow.

The models now represent agent names, task statuses, tutor requests, tutor responses, Coordinator tasks, approved context, subagent findings, requested context, follow-up objectives, and metadata.

Coordinator tasks now contain a task ID, parent request ID, assigned agent, objective, user question, approved context, maximum step limit, and timeout value.

### Step 2: Create the Coordinator Gateway

A restricted Coordinator Gateway was introduced as the communication interface available to subagents.

The Gateway defines operations for submitting a finding, requesting approved context, and requesting follow-up work. It does not expose the full Coordinator internals or direct access to the agent registry.

This establishes the intended communication boundary between the Coordinator and its subagents.

### Step 3: Create the Coordinator context store

A central context store was created to keep subagent findings associated with their parent request.

The store supports adding findings, retrieving findings, searching findings by topic, and clearing all findings for a request.

The context store ensures that findings from one user request do not leak into another user request.

### Step 4: Connect the context store to the Coordinator

The Coordinator was updated to own the context store and maintain the relationship between individual task IDs and parent request IDs.

When a subagent submits a finding, the Coordinator identifies the related parent request and stores the finding centrally.

When a subagent requests context, the Coordinator returns approved findings from the relevant parent request.

### Step 5: Update the subagent interface

The base subagent interface was updated so every subagent receives a restricted Coordinator Gateway when it runs.

This allows a subagent to interact with the Coordinator without receiving unrestricted access to other agents or the complete workflow state.

### Step 6: Update the Teaching Agent

The deterministic Teaching Agent was updated to receive the Coordinator Gateway.

Instead of returning its finding directly as the final response, the Teaching Agent submits its finding through the Coordinator Gateway and returns a structured task result.

This demonstrates that subagents can communicate with the Coordinator through the approved interface.

### Step 7: Pass the Coordinator Gateway during dispatch

The Coordinator was updated to pass itself through the Gateway interface when invoking the Teaching Agent.

The Teaching Agent can now submit findings to the Coordinator while remaining unable to communicate directly with other agents.

### Step 8: Test mediated context exchange

A context-aware test agent was created for testing purposes.

The test agent submits a finding through the Coordinator, requests context through the Coordinator, and returns the approved context it received.

The test confirmed that a subagent can submit and request information through the Coordinator-mediated channel.

### Step 9: Create the Coordinator router

A deterministic Coordinator router was added.

The router examines the user question and selects relevant agent names. Teaching requests are routed to the Teaching Agent. Questions involving PDFs or uploaded documents are routed to the PDF RAG Agent. Current or documentation-related questions are routed to the Web Research Agent. Repository or code-example questions are routed to the GitHub Agent.

The router only makes a routing decision. It does not invoke agents itself.

### Step 10: Test the Coordinator router

Tests were added to confirm that the router always selects the Teaching Agent and selects the appropriate PDF, Web Research, and GitHub agents when relevant keywords appear in the question.

A test-discovery issue was corrected during this step to ensure that the new test file used the correct filename pattern and was collected by pytest.

### Step 11: Connect routing to the Coordinator

The Coordinator was updated to use the router before dispatching work.

The Coordinator now selects relevant registered agents, creates a separate task for each selected agent, tracks the tasks under the parent request, dispatches them, collects their results, and aggregates their findings.

Unregistered agents are skipped until their real implementations are added in later phases.

### Step 12: Create temporary research-agent stubs

Temporary stub versions of the PDF RAG Agent, Web Research Agent, and GitHub Agent were created.

The stubs do not yet search documents, access the web, or inspect GitHub repositories. They only submit confirmation findings to the Coordinator so the routing and dispatch architecture can be tested independently from retrieval implementation.

### Step 13: Register the temporary research agents

The temporary PDF, Web Research, and GitHub agents were registered in the Coordinator’s agent registry.

The Coordinator can now dispatch to all four current agent types: Teaching, PDF RAG, Web Research, and GitHub.

### Step 14: Test multiagent dispatch

A multiagent dispatch test was added.

The test submits a question involving the latest GitHub repository code example. The Coordinator routes the request to the Teaching Agent, Web Research Agent, and GitHub Agent, then combines their findings centrally.

The test confirmed that multiple agents can work on one request without communicating directly with one another.

### Step 15: Test PDF-agent dispatch

A PDF dispatch test was added.

The test submits a question involving an uploaded PDF document. The Coordinator routes the request to the Teaching Agent and PDF RAG Agent and combines both findings.

The PDF agent used at this stage is still a temporary stub. Real document ingestion and retrieval will be implemented in a later phase.

### Step 16: Test Coordinator failure handling

A failing mock Teaching Agent was created for testing purposes.

The test confirmed that when an assigned subagent returns a failed status, the Coordinator returns a controlled failed response rather than crashing or producing an invalid answer.

### Step 17: Test request-context isolation

A context isolation test was added.

The test confirmed that findings associated with one parent request are not returned for another parent request and that unknown requests return no findings.

This protects against cross-request context leakage.

### Step 18: Test context search and cleanup

A context search and cleanup test was added.

The test confirmed that the context store can find relevant findings by topic and remove all findings associated with a completed request.

A missing cleanup method was identified during testing and added to the context store implementation.

### Step 19: Run the complete Phase 2 test suite

The full automated test suite was executed after routing, dispatch, context, failure, and isolation behavior were implemented.

The final Phase 2 suite completed successfully with ten passing tests.

### Step 20: Verify the Streamlit application

The Streamlit application was started and tested with representative questions.

A basic conceptual question routed to the Teaching Agent. A PDF-related question routed to the Teaching Agent and PDF RAG stub. A GitHub and current-information question routed to the Teaching Agent, Web Research stub, and GitHub stub.

The application successfully displayed the aggregated Coordinator response.

## Phase 2 architecture result

Phase 2 established the following communication pattern:

```
Subagent → Coordinator Gateway → Coordinator Context Store

Coordinator → approved context → Subagent
```

The following direct communication pattern is not allowed:

```
Subagent A → Subagent B
```

The Coordinator now controls routing, task creation, dispatch, finding storage, context sharing, aggregation, failure handling, and final response delivery.

## Files created or updated during Phase 2

| File or directory | Purpose |
| --- | --- |
| `app/domain/messages.py` | Expanded typed communication models |
| `app/agents/base.py` | Gateway-aware subagent interface |
| `app/agents/teaching_agent.py` | Gateway-aware deterministic Teaching Agent |
| `app/agents/stub_agents.py` | Temporary PDF, Web, and GitHub agents |
| `app/coordinator/gateway.py` | Restricted Coordinator communication interface |
| `app/coordinator/context_store.py` | Central mediated finding store |
| `app/coordinator/router.py` | Question-based agent selection |
| `app/coordinator/coordinator.py` | Routing, dispatch, aggregation, and context control |
| `tests/test_coordinator_context.py` | Mediated context exchange test |
| `tests/test_router.py` | Router behavior tests |
| `tests/test_multiagent_dispatch.py` | Multiagent dispatch tests |
| `tests/test_pdf_dispatch.py` | PDF-agent routing test |
| `tests/test_failure_handling.py` | Failed-agent behavior test |
| `tests/test_context_isolation.py` | Request isolation test |
| `tests/test_context_search.py` | Context search and cleanup test |

## Temporary implementation limitations

The PDF, Web Research, and GitHub agents are currently stubs. They do not yet retrieve real evidence.

The Teaching Agent remains deterministic and does not yet call OpenAI GPT.

The Coordinator currently dispatches registered agents sequentially. More advanced parallel execution, retries, timeout enforcement, source normalization, and evidence verification will be added later.

Citation verification, real PDF ingestion, embeddings, Qdrant retrieval, web fetching, GitHub search, and OpenAI GPT integration are not part of the completed Phase 2 implementation.

## Phase 2 completion status

**Status:** Complete.

**Validated behavior:** Typed task communication, Coordinator-mediated findings, routing, multiagent dispatch, failure handling, request isolation, context search, context cleanup, and Streamlit integration.

**Next phase:** Integrate the OpenAI GPT adapter and replace the deterministic Teaching Agent with a real GPT-backed implementation.


# AI Teaching Tutor — Phase 3 Process Followed

## Phase 3 objective

The objective of Phase 3 was to integrate OpenAI GPT into the teaching workflow while preserving the Coordinator-mediated architecture and keeping automated tests independent of external API calls.

Phase 3 replaced the deterministic Teaching Agent in the Streamlit application with a GPT-backed Teaching Agent. The model configuration, OpenAI client, structured output support, usage tracking, error handling, learner-level prompting, and test doubles were added incrementally.

The completed Phase 3 workflow is:

```
User → Streamlit → Coordinator → GPT Teaching Agent → Coordinator → Streamlit response
```

The GPT Teaching Agent communicates with the Coordinator only. It does not communicate directly with the PDF RAG, Web Research, GitHub, Citation, or Composer agents.

### Step 1: Create the GPT model configuration

A typed GPT model configuration was created at `app/llm/models.py`.

The configuration stores the selected model name and reasoning setting. The model name is read from application settings rather than being repeated throughout the codebase.

The initial default model was configured as `gpt-5-mini`.

### Step 2: Create the OpenAI client adapter

A centralized OpenAI client adapter was created at `app/llm/client.py`.

The adapter receives application settings, creates the OpenAI client, sends Chat Completions requests, applies the configured model, limits completion size, and returns generated text.

Agents do not create independent unmanaged OpenAI clients. They use the centralized adapter.

### Step 3: Test the OpenAI adapter without using the API

A fake OpenAI client was created inside `tests/test_llm_client.py`.

The fake client checks that the configured model and completion limit are passed correctly and returns a simulated GPT response.

This test allows the adapter to be validated without consuming API quota or requiring network access.

### Step 4: Create usage tracking

A usage module was created at `app/llm/usage.py`.

It defines a typed usage record containing prompt tokens, completion tokens, and total tokens.

A safe extraction function was added so missing usage data does not cause the application to fail.

### Step 5: Connect usage tracking to the OpenAI adapter

The OpenAI adapter was updated to return both generated text and a typed usage record.

This provides the foundation for future cost controls, usage dashboards, request budgets, and operational monitoring.

### Step 6: Update the OpenAI adapter test

The adapter test was updated to verify both the generated response and token usage values.

The fake response now includes simulated prompt, completion, and total token counts.

### Step 7: Add structured GPT output

A structured output client was created at `app/llm/structured_output.py`.

It requests strict JSON Schema output and parses the model response into a JSON object.

This will later support predictable Coordinator plans, evidence records, citation reports, and answer models.

### Step 8: Test structured output

A structured-output test was added at `tests/test_structured_output.py`.

The test uses a fake client, verifies that a JSON Schema response format is requested, parses the response, and checks the expected fields.

### Step 9: Configure the local OpenAI key

A private `.env` file was created from `.env.example`.

The OpenAI API key was placed in the local environment file rather than in source code or chat messages.

The `.env` file remains excluded from Git through `.gitignore`.

### Step 10: Test real GPT connectivity

A temporary connection-checking script was created at `scripts/test_openai_connection.py`.

The script sends a short request through the centralized adapter and prints the generated response and token count.

The script was moved out of the `tests` directory because it performs a real external API call and should not run automatically as part of pytest.

The script was executed as a module from the project root to ensure the application package could be imported correctly.

### Step 11: Create the GPT Teaching Agent

A GPT-backed Teaching Agent was created at `app/agents/gpt_teaching_agent.py`.

The agent constructs a teaching prompt, sends it through the OpenAI adapter, submits the generated answer to the Coordinator, and returns usage metadata.

The agent does not communicate directly with any other subagent.

### Step 12: Make the GPT Teaching Agent testable

The GPT Teaching Agent was updated to accept an optional LLM adapter.

This dependency-injection design allows tests to provide a fake LLM instead of calling OpenAI.

The production application uses the real OpenAI adapter, while automated tests use a deterministic fake implementation.

### Step 13: Test the GPT Teaching Agent

A test was added at `tests/test_gpt_teaching_agent.py`.

The test uses a fake LLM, verifies that system and user messages are constructed, checks that the response is sent through the Coordinator, and confirms that usage metadata is returned.

### Step 14: Connect the GPT Teaching Agent to Streamlit

The Streamlit entrypoint was updated to instantiate `GPTTeachingAgent` instead of the deterministic Teaching Agent.

The application now sends conceptual questions through the Coordinator to the real GPT-backed agent.

A controlled exception handler was added around the request so an API or runtime failure displays a safe error message instead of crashing the user interface.

### Step 15: Validate the real GPT workflow

The Streamlit application was restarted after the adapter correction.

A real question was submitted through the interface, and the GPT Teaching Agent returned a visible teaching response through the Coordinator.

### Step 16: Add learner level to Coordinator tasks

The Coordinator task model was expanded with a learner-level field.

The supported levels are beginner, intermediate, and advanced.

The field has a default value so earlier task construction and tests remain compatible.

### Step 17: Pass learner level through the Coordinator

The Coordinator was updated to copy the learner level from the user’s tutor request into the assigned Coordinator task.

This makes learner-level information available to the GPT Teaching Agent without requiring the agent to access Streamlit state directly.

### Step 18: Use learner level in the GPT prompt

The GPT Teaching Agent was updated to include the selected learner level in its user prompt.

The model is now explicitly asked to create a beginner-level, intermediate-level, or advanced-level explanation based on the user’s selection.

### Step 19: Validate learner-level behavior

The Streamlit application was tested with the same question at beginner and advanced levels.

The requests completed successfully and produced responses using the selected learner-level context.

### Step 20: Add the learner-level regression test

A regression test was added at `tests/test_learner_level.py`.

The test uses a recording fake LLM to inspect the prompt sent by the GPT Teaching Agent.

It confirms that the selected advanced learner level and the requested topic are included in the prompt.

### Step 21: Test empty GPT responses

An error-handling test was added at `tests/test_llm_errors.py`.

The test simulates an empty model response and confirms that the OpenAI adapter raises a controlled runtime error containing the finish reason.

This protects the application from silently displaying empty answers.

### Step 22: Run the complete Phase 3 test suite

The complete automated test suite was run after GPT integration, structured output, usage tracking, error handling, and learner-level behavior were implemented.

The Phase 3 suite completed successfully with fifteen passing tests.

The test suite continues to use fake model clients where appropriate, so normal test execution does not require external API calls.

### Step 23: Verify the GPT-backed Streamlit application

The Streamlit application was started and tested with real OpenAI GPT requests.

The application successfully accepted a question, passed it through the Coordinator, invoked the GPT Teaching Agent, received the response, and displayed it in Streamlit.

Beginner and advanced learner-level settings were both verified.

## Phase 3 architecture result

Phase 3 established the following model communication pattern:

```
Coordinator → GPT Teaching Agent → OpenAI adapter → OpenAI GPT

OpenAI GPT response → OpenAI adapter → GPT Teaching Agent → Coordinator
```

The GPT Teaching Agent submits its final finding through the Coordinator Gateway. The Coordinator remains responsible for the final response flow.

The prohibited pattern remains:

```
GPT Teaching Agent → another subagent
```

## Files created or updated during Phase 3

| File or directory | Purpose |
| --- | --- |
| `app/llm/models.py` | GPT model configuration |
| `app/llm/client.py` | Centralized OpenAI GPT adapter |
| `app/llm/usage.py` | Token usage records and extraction |
| `app/llm/structured_output.py` | Strict JSON Schema response handling |
| `app/agents/gpt_teaching_agent.py` | GPT-backed Teaching Agent |
| `app/domain/messages.py` | Learner-level task field |
| `app/coordinator/coordinator.py` | Learner-level propagation and GPT dispatch compatibility |
| `streamlit_app.py` | GPT-backed Streamlit workflow and safe error handling |
| `tests/test_llm_client.py` | OpenAI adapter and usage tests |
| `tests/test_structured_output.py` | Structured response test |
| `tests/test_gpt_teaching_agent.py` | GPT Teaching Agent test |
| `tests/test_llm_errors.py` | Empty response error test |
| `tests/test_learner_level.py` | Learner-level prompt regression test |
| `scripts/test_openai_connection.py` | Manual real-API connectivity check |
| `.env` | Local private configuration, excluded from Git |

## Current temporary limitations

The GPT Teaching Agent currently produces a teaching response but does not yet use retrieved PDF, web, or GitHub evidence in its prompt.

The PDF RAG, Web Research, and GitHub agents remain temporary stubs.

Citation verification has not yet been implemented.

The application still needs real PDF ingestion, embeddings, Qdrant indexing, source provenance, evidence normalization, and citation-aware answer composition.

The current OpenAI adapter uses the Chat Completions interface and a configurable completion budget. More advanced model routing, retries, provider fallback, and cost controls will be added later.

The temporary connectivity script should not be included in the normal automated test suite because it makes a real external API request.

## Phase 3 completion status

**Status:** Complete.

**Validated behavior:** OpenAI GPT configuration, centralized API access, usage tracking, structured output, test doubles, GPT Teaching Agent integration, empty-response handling, learner-level prompting, Streamlit integration, and fifteen passing automated tests.

**Next phase:** Implement local PDF ingestion, page-aware chunking, embeddings, and Qdrant-backed retrieval.


# Phase 4 Process Followed: PDF Ingestion, Qdrant RAG, and Active-Document Isolation

## Phase 4 objective

Phase 4 added local PDF ingestion, OpenAI embeddings, Qdrant vector retrieval, PDF-grounded teaching, Streamlit document upload, and active-document isolation.

### Step 1: Define document metadata

A document metadata model was created to track each PDF’s identifier, filename, path, SHA-256 hash, processing status, page count, chunk count, errors, and timestamps.

### Step 2: Extract PDF pages

A PDF extraction component was created using page-aware extraction. Each extracted page retains its one-based page number so future answers can cite the originating page.

### Step 3: Split pages into chunks

A page-aware chunking component was added. It splits page text into overlapping word-based chunks while preserving the original page number and chunk index.

### Step 4: Test PDF chunking

Automated tests were added to verify that chunks preserve page numbers, overlap correctly, and reject invalid chunking parameters.

### Step 5: Add a sample PDF

A sample PDF was placed in the local document directory for extraction, indexing, retrieval, and end-to-end testing.

### Step 6: Test PDF extraction

The extraction component was tested against the sample PDF to confirm that pages are returned with page numbers and text fields.

### Step 7: Create document hashing

A SHA-256 file-hashing utility was added. The hash provides a stable document identity and allows the system to detect changed files.

### Step 8: Test document hashing

Automated tests verified that hashing is stable for the same file and produces a valid SHA-256-length value.

### Step 9: Create the ingestion manifest

A JSON-based ingestion manifest was created to persist document records and indexing status between application runs.

### Step 10: Test manifest persistence

Automated tests verified that document records can be saved and loaded with their metadata preserved.

### Step 11: Create the PDF ingestion pipeline

The ingestion pipeline connected file hashing, PDF extraction, page-aware chunking, document metadata, and manifest persistence.

### Step 12: Test the ingestion pipeline

The pipeline was tested against the sample PDF to confirm successful extraction and persistent document recording.

### Step 13: Create the embedding interface

An interchangeable embedding-provider interface was created so the system can use OpenAI embeddings initially and support local embedding models later without changing the rest of the RAG architecture.

### Step 14: Test the embedding interface

A fake embedding provider was used to verify that one vector is produced for each input text without making external API calls.

### Step 15: Configure the embedding model

A separate configurable embedding-model setting was added. This keeps the teaching GPT model and document-embedding model independent.

### Step 16: Implement the OpenAI embedding provider

An OpenAI embedding provider was added. It sends document or query text to the configured embedding model and returns vectors.

### Step 17: Test the OpenAI embedding provider

Automated tests used a fake OpenAI client to verify model selection, input handling, and vector extraction without calling the external API.

### Step 18: Verify real OpenAI embeddings

A manual connectivity check successfully generated two embeddings with 1,536 dimensions each.

### Step 19: Create the local Qdrant service

Qdrant was added through Docker Compose with persistent local storage mounted under the project data directory.

### Step 20: Create the Qdrant store

A Qdrant store abstraction was implemented to create the document collection with cosine similarity and the configured vector size.

### Step 21: Test Qdrant collection creation

Automated tests verified that the collection is created when absent and is not recreated when it already exists.

### Step 22: Verify the real Qdrant connection

A manual connectivity check created or loaded the configured collection and confirmed that the local Qdrant service was reachable.

### Step 23: Add vector upsert support

The Qdrant store was extended to persist vectors together with document, file, page, chunk, and text metadata.

### Step 24: Test vector upsert

Automated tests verified vector and payload length validation and confirmed that metadata is stored with vectors.

### Step 25: Add vector search

Vector search was added to retrieve the most similar payloads from Qdrant for a query embedding.

### Step 26: Test vector search

Automated tests verified query handling, result conversion, similarity scores, and payload extraction.

### Step 27: Create the document indexer

A document indexer was created to connect PDF extraction, chunking, OpenAI embeddings, Qdrant upsert, and manifest updates.

### Step 28: Test document indexing

The indexer was tested using fake embeddings and a fake vector store to confirm that each chunk produces a vector and page-aware metadata payload.

### Step 29: Index the sample PDF for real

The sample PDF was embedded and indexed into the local Qdrant collection using the real OpenAI embedding provider.

### Step 30: Create the real PDF RAG Agent

A PDF RAG Agent was added. It embeds the user query, searches Qdrant, formats retrieved PDF evidence, and communicates findings only through the Coordinator.

### Step 31: Allow PDF-agent injection

The Coordinator was updated so the real PDF RAG Agent can be injected while retaining a temporary stub for tests and compatibility.

### Step 32: Connect PDF RAG to Streamlit

The Streamlit application was updated to use the real PDF RAG Agent together with the GPT Teaching Agent.

### Step 33: Create the PDF evidence model

A typed PDF evidence model was introduced for document identifiers, filenames, page numbers, excerpts, similarity scores, and citation labels.

### Step 34: Use typed evidence in the PDF RAG Agent

The PDF RAG Agent was updated to validate retrieved results through the PDF evidence model before submitting findings to the Coordinator.

### Step 35: Test PDF evidence validation

Automated tests verified citation labels and rejected invalid page numbers and similarity scores.

### Step 36: Add a retrieval threshold

A configurable minimum similarity threshold was added so weak matches can be rejected instead of being passed to GPT.

### Step 37: Apply the threshold

The PDF RAG Agent was updated to filter Qdrant results using the configured threshold and report when no sufficiently relevant evidence exists.

### Step 38: Test weak-match rejection

Automated tests verified that matches below the threshold are rejected and reported as partial retrieval results.

### Step 39: Create the document upload helper

A safe upload helper was created to accept PDF files, normalize their filenames, and save them inside the configured document directory.

### Step 40: Test safe PDF upload

Automated tests verified PDF-only validation and safe filename handling.

### Step 41: Add PDF upload and indexing to Streamlit

Streamlit was updated with a PDF uploader, save-and-index action, indexing status, and integration with the document indexer.

### Step 42: Add the active-document test

An end-to-end test was added to verify that the selected document identifier reaches the PDF agent and that its evidence reaches the GPT prompt.

### Step 43: Run full PDF workflow validation

The complete test suite and Streamlit workflow were run to verify upload, indexing, retrieval, Coordinator mediation, and GPT response generation.

### Step 44: Add a document-status helper

The ingestion manifest was extended with a document-listing operation for displaying tracked documents.

### Step 45: Display indexed-document status

Streamlit was updated to display indexed document names, statuses, page counts, and chunk counts.

### Step 46: Test document listing

Automated tests verified that manifest records can be listed with their metadata.

### Step 47: Validate the complete Phase 4 workflow

The final validation confirmed that uploaded PDFs can be indexed, the active document is tracked, retrieval is restricted to the active document, GPT receives approved evidence, and unrelated older content is not returned in the final answer.

## Phase 4 result

Phase 4 completed the local PDF RAG foundation. The application can now upload and index PDFs, create OpenAI embeddings, store vectors in Qdrant, retrieve page-aware evidence, pass approved evidence through the Coordinator, and generate a GPT teaching response based on the selected document.

## Remaining limitations

Web research, GitHub research, formal citation verification, advanced evidence normalization, production authentication, retry policies, parallel execution, backups, and deployment hardening remain future work.

## Next phase

The next phase will implement web research and source retrieval. Web findings will return to the Coordinator, which will decide what evidence can be passed to the Teaching Agent and Citation Agent.

**Phase 4 status:** Complete.
