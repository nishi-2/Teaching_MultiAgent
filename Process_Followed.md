# AI Teaching Tutor — Phase 1 Process Followed

## Phase 1 objective

The objective of Phase 1 was to create a working Python and Streamlit project skeleton with a deterministic teaching workflow. The initial workflow was intentionally kept small so that the project could be validated before adding OpenAI GPT, PDF RAG, web research, GitHub research, and advanced multiagent orchestration.

The completed Phase 1 workflow is:

```
Streamlit interface → Coordinator → Teaching Agent → Coordinator → Streamlit response
```

The Teaching Agent used in this phase is a deterministic mock. It does not yet call an AI model.

## Step 1: Create the project folder

A dedicated project folder named `ai-teaching-tutor` was created. This folder is the root directory for the application, source code, tests, configuration, data, and documentation.

## Step 2: Create the Python virtual environment

A project-specific Python virtual environment was created using the available Windows Python 3.10.8 installation. The environment isolates this project’s dependencies from other Python projects on the computer.

The project was configured to support Python 3.10 and later.

## Step 3: Create the dependency file

A dependency file named `requirements.txt` was created. It lists the libraries that will be used throughout the project, including Streamlit, Pydantic Settings, OpenAI integration, Qdrant support, PDF processing, HTTP communication, testing, formatting, and type checking.

The dependencies were installed inside the project virtual environment.

## Step 4: Create the Git ignore file

A `.gitignore` file was created. It prevents virtual-environment files, Python caches, local secrets, generated document data, vector database storage, logs, and temporary database files from being committed to Git.

## Step 5: Create the environment template

An `.env.example` file was created. It documents the configuration variables that will eventually control the OpenAI model, Qdrant connection, document directory, collection name, and logging level.

No real API key was placed in the project source code or environment template.

## Step 6: Create the initial project directories

The initial application, test, and data directories were created. These directories establish the foundation for configuration, domain models, Coordinator logic, agents, LLM integration, user interface components, tests, documents, extracted text, manifests, and logs.

## Step 7: Create Python package files

Python package initialization files were added to the application folders. This allows the application modules to be imported consistently as Python packages.

## Step 8: Create the project configuration file

A `pyproject.toml` file was created. It defines the project metadata, build configuration, Python version requirement, pytest configuration, formatting line length, and package configuration.

The Python requirement was adjusted from Python 3.11 to Python 3.10 because the project is being developed with Python 3.10.8.

## Step 9: Create the settings module

A centralized settings module was created at `app/config/settings.py`. It loads configuration values from the environment and provides safe defaults for development.

This establishes one place for application configuration instead of scattering configuration values across the codebase.

## Step 10: Create the initial domain models

The first domain models were created at `app/domain/messages.py`. These models represent a tutor request, tutor response, Coordinator task, and subagent result.

Using typed models establishes a consistent structure for communication between the Streamlit interface, Coordinator, and agents.

## Step 11: Create the restricted subagent interface

A base subagent interface was created at `app/agents/base.py`. It defines the common behavior expected from a subagent: receiving an assigned Coordinator task and returning a structured result.

The interface does not provide direct subagent-to-subagent communication.

## Step 12: Create the mock Teaching Agent

A deterministic Teaching Agent was created at `app/agents/teaching_agent.py`. It receives a task from the Coordinator and returns a simple teaching-plan finding based on the user’s question.

This mock agent allows the orchestration flow to be tested without depending on an external model or API key.

## Step 13: Create the initial Coordinator

A Coordinator was created at `app/coordinator/coordinator.py`. It receives a tutor request, creates a task, delegates the task to the Teaching Agent, receives the result, handles a failed result, and converts a successful result into a tutor response.

The Coordinator is the central workflow component.

A future refinement will add a restricted Coordinator interaction interface. This will allow subagents to submit findings, request approved context from the Coordinator, and request follow-up work through the Coordinator without directly contacting other subagents.

## Step 14: Create the Streamlit application

The Streamlit entrypoint was created at `streamlit_app.py`. It provides a page title, learner-level selector, question input, Ask Tutor button, Coordinator initialization, and tutor response display.

The Streamlit application was successfully launched in the browser and tested with a sample question.

## Step 15: Add the first automated test

A smoke test was created at `tests/test_smoke.py`. It verifies that the Coordinator can receive a tutor request, delegate to the Teaching Agent, return a successful response, and include the requested topic in the response.

The test was corrected so that the expected text matches the actual test question and is checked without depending on capitalization.

## Step 16: Add application logging

A logging configuration module was created at `app/config/logging_config.py`. It establishes a consistent log format and allows the logging level to be controlled through configuration.

## Step 17: Connect logging to Streamlit

The Streamlit entrypoint was updated to initialize logging and record when a tutor question is received.

The application was restarted and verified after the logging integration.

## Step 18: Create the project README

A `README.md` file was created. It documents the project’s current status, the Phase 1 workflow, local setup, application startup command, and test command.

## Step 19: Run complete Phase 1 validation

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

## Step 1: Upgrade the communication models

The shared communication models were expanded to support the growing multiagent workflow.

The models now represent agent names, task statuses, tutor requests, tutor responses, Coordinator tasks, approved context, subagent findings, requested context, follow-up objectives, and metadata.

Coordinator tasks now contain a task ID, parent request ID, assigned agent, objective, user question, approved context, maximum step limit, and timeout value.

## Step 2: Create the Coordinator Gateway

A restricted Coordinator Gateway was introduced as the communication interface available to subagents.

The Gateway defines operations for submitting a finding, requesting approved context, and requesting follow-up work. It does not expose the full Coordinator internals or direct access to the agent registry.

This establishes the intended communication boundary between the Coordinator and its subagents.

## Step 3: Create the Coordinator context store

A central context store was created to keep subagent findings associated with their parent request.

The store supports adding findings, retrieving findings, searching findings by topic, and clearing all findings for a request.

The context store ensures that findings from one user request do not leak into another user request.

## Step 4: Connect the context store to the Coordinator

The Coordinator was updated to own the context store and maintain the relationship between individual task IDs and parent request IDs.

When a subagent submits a finding, the Coordinator identifies the related parent request and stores the finding centrally.

When a subagent requests context, the Coordinator returns approved findings from the relevant parent request.

## Step 5: Update the subagent interface

The base subagent interface was updated so every subagent receives a restricted Coordinator Gateway when it runs.

This allows a subagent to interact with the Coordinator without receiving unrestricted access to other agents or the complete workflow state.

## Step 6: Update the Teaching Agent

The deterministic Teaching Agent was updated to receive the Coordinator Gateway.

Instead of returning its finding directly as the final response, the Teaching Agent submits its finding through the Coordinator Gateway and returns a structured task result.

This demonstrates that subagents can communicate with the Coordinator through the approved interface.

## Step 7: Pass the Coordinator Gateway during dispatch

The Coordinator was updated to pass itself through the Gateway interface when invoking the Teaching Agent.

The Teaching Agent can now submit findings to the Coordinator while remaining unable to communicate directly with other agents.

## Step 8: Test mediated context exchange

A context-aware test agent was created for testing purposes.

The test agent submits a finding through the Coordinator, requests context through the Coordinator, and returns the approved context it received.

The test confirmed that a subagent can submit and request information through the Coordinator-mediated channel.

## Step 9: Create the Coordinator router

A deterministic Coordinator router was added.

The router examines the user question and selects relevant agent names. Teaching requests are routed to the Teaching Agent. Questions involving PDFs or uploaded documents are routed to the PDF RAG Agent. Current or documentation-related questions are routed to the Web Research Agent. Repository or code-example questions are routed to the GitHub Agent.

The router only makes a routing decision. It does not invoke agents itself.

## Step 10: Test the Coordinator router

Tests were added to confirm that the router always selects the Teaching Agent and selects the appropriate PDF, Web Research, and GitHub agents when relevant keywords appear in the question.

A test-discovery issue was corrected during this step to ensure that the new test file used the correct filename pattern and was collected by pytest.

## Step 11: Connect routing to the Coordinator

The Coordinator was updated to use the router before dispatching work.

The Coordinator now selects relevant registered agents, creates a separate task for each selected agent, tracks the tasks under the parent request, dispatches them, collects their results, and aggregates their findings.

Unregistered agents are skipped until their real implementations are added in later phases.

## Step 12: Create temporary research-agent stubs

Temporary stub versions of the PDF RAG Agent, Web Research Agent, and GitHub Agent were created.

The stubs do not yet search documents, access the web, or inspect GitHub repositories. They only submit confirmation findings to the Coordinator so the routing and dispatch architecture can be tested independently from retrieval implementation.

## Step 13: Register the temporary research agents

The temporary PDF, Web Research, and GitHub agents were registered in the Coordinator’s agent registry.

The Coordinator can now dispatch to all four current agent types: Teaching, PDF RAG, Web Research, and GitHub.

## Step 14: Test multiagent dispatch

A multiagent dispatch test was added.

The test submits a question involving the latest GitHub repository code example. The Coordinator routes the request to the Teaching Agent, Web Research Agent, and GitHub Agent, then combines their findings centrally.

The test confirmed that multiple agents can work on one request without communicating directly with one another.

## Step 15: Test PDF-agent dispatch

A PDF dispatch test was added.

The test submits a question involving an uploaded PDF document. The Coordinator routes the request to the Teaching Agent and PDF RAG Agent and combines both findings.

The PDF agent used at this stage is still a temporary stub. Real document ingestion and retrieval will be implemented in a later phase.

## Step 16: Test Coordinator failure handling

A failing mock Teaching Agent was created for testing purposes.

The test confirmed that when an assigned subagent returns a failed status, the Coordinator returns a controlled failed response rather than crashing or producing an invalid answer.

## Step 17: Test request-context isolation

A context isolation test was added.

The test confirmed that findings associated with one parent request are not returned for another parent request and that unknown requests return no findings.

This protects against cross-request context leakage.

## Step 18: Test context search and cleanup

A context search and cleanup test was added.

The test confirmed that the context store can find relevant findings by topic and remove all findings associated with a completed request.

A missing cleanup method was identified during testing and added to the context store implementation.

## Step 19: Run the complete Phase 2 test suite

The full automated test suite was executed after routing, dispatch, context, failure, and isolation behavior were implemented.

The final Phase 2 suite completed successfully with ten passing tests.

## Step 20: Verify the Streamlit application

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