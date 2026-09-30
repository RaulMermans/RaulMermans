### Raúl Mermans

**Applied AI & Software Engineer.** I build analytical runtimes, AI agents, agent infrastructure and local-first AI tooling — and I measure whether they work.

[Portfolio](https://www.raulmermans.com/en/) · [LinkedIn](https://www.linkedin.com/in/raulmermans/)

---

#### Selected work

| Project | What it is | Strongest proof |
| --- | --- | --- |
| **[BI Notebook Lab](https://github.com/RaulMermans/bi-notebook-lab)** | Browser-based analytical runtime: DAX engine, filter context, semantic models | 1,024 tests · 82/83 DAX conformance cases pass |
| **[OpsTwin](https://github.com/RaulMermans/OpsTwin)** | Operational simulation lab comparing workflow changes with paired simulation | 430 tests (247 backend, 183 frontend) · live demo |
| **[DataBrief AI](https://github.com/RaulMermans/DataBrief-AI)** | Bounded CSV/XLSX analysis pipeline producing grounded, source-cited reports | 176 backend tests · every finding cites its artifact |
| **[Open VS Code Agent](https://github.com/RaulMermans/Open-VS-Code-Agent)** | Coding agent built and benchmarked for a local 7B open-weight model | 37.5% → 75.0% task success on a 24-task benchmark |
| **[IRIS OS](https://github.com/RaulMermans/IRIS-OS)** | Personal AI OS: evidence-backed attention, governed agents, human approval | Architecture, contracts and synthetic traces |
| **[HALO Control](https://github.com/RaulMermans/AMD-HALO-Control)** | Local AI infrastructure control plane: model routing, telemetry, authorization | Architecture, contracts and a runnable routing demo |

<sub>BI Notebook Lab, OpsTwin and DataBrief AI are open source (MIT). IRIS OS, Open VS Code Agent and HALO Control are public architecture editions of active private systems.</sub>

**Progression:** analytical systems (BI Notebook Lab, OpsTwin) → applied AI (DataBrief AI) → AI agents (Open VS Code Agent) → agent systems (IRIS OS) → local AI infrastructure (HALO Control).

#### External open source

- **[Lemonade: reject invalid backend-specific config keys](https://github.com/lemonade-sdk/lemonade/pull/3684)** (merged). Replaced a substring match in backend config validation with checks against each backend's declared variants, so misspelled keys such as `flm.flm_bin` fail instead of being silently ignored. Closes [#3678](https://github.com/lemonade-sdk/lemonade/issues/3678).
- **[OpenLIT: LangGraph memory connector](https://github.com/openlit/openlit/pull/1667)** (open pull request). A LangGraph Store memory connector with memory CRUD/search, namespace mapping, authentication, safe content handling, docs and integration tests.
- **[OpenJudge: reject degenerate empty-string matches](https://github.com/agentscope-ai/OpenJudge/pull/200)** (open pull request). A grader fix for degenerate empty-string matches.

#### Stack

| | |
| --- | --- |
| **AI systems** | Agent orchestration (CrewAI), MCP, tool calling, memory, human-in-the-loop approval, Ollama and open-weight models |
| **Evaluation** | Benchmark harnesses, conformance suites, failure taxonomies, Vitest, Pytest, Playwright |
| **Backend** | TypeScript, Node.js, Fastify, Python, FastAPI, SimPy |
| **Frontend** | React, Next.js, Vite, React Flow, Recharts |
| **Data** | PostgreSQL, SQLite, IndexedDB, DAX and semantic modelling, Power BI concepts |
| **Infrastructure** | Local inference, Vercel, GitHub Actions |

#### Current focus

- Extending the Open VS Code Agent benchmark to BUILD and DEBUG tasks on local models.
- Governed execution and memory in IRIS OS.
- Bringing HALO Control up on the AMD Halo target hardware.
