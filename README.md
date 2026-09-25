### Raúl Mermans

**Applied AI & Software Engineer.** I build analytical runtimes, AI agents, agent infrastructure and local-first AI tooling, and I measure whether they work.

[Portfolio](https://www.raulmermans.com/en/) · [LinkedIn](https://www.linkedin.com/in/raulmermans/)

---

#### Selected work

| Project | What it is | Strongest evidence |
| --- | --- | --- |
| **[BI Notebook Lab](https://github.com/RaulMermans/bi-notebook-lab)** | Browser-based analytical runtime that teaches how BI semantic models compute: DAX lexer → parser → binder → evaluator, filter context, relationships, Power Query | 1,024 tests · 83-case DAX conformance suite with documented divergences · 100k-row benchmark |
| **[OpsTwin](https://github.com/RaulMermans/OpsTwin)** | Operational simulation lab for testing service-workflow changes with paired simulation, sensitivity and uncertainty ranges | 247 backend + 172 frontend tests · strict typing · live deployment |
| **[DataBrief AI](https://github.com/RaulMermans/DataBrief-AI)** | Bounded analytics workflow: CSV/XLSX → profiling → routed plan → sandboxed execution → grounded report | 176 backend tests · every finding cites the artifact it came from |
| **[Open VS Code Agent](https://github.com/RaulMermans/Open-VS-Code-Agent)** | Coding agent designed and benchmarked for a local 7B open-weight model, with explicit tools, verification and crash-safe mutation | 24-task benchmark: 37.5% → 75.0% grounded success after evidence-driven orchestration |
| **[JARVIS OS](https://github.com/RaulMermans/JARVIS-OS)** | Personal AI operating system built around one question, *what needs my attention today?*, with specialist agents, governed actions and human approval | Evidence-required attention · autonomy ladder · verified execution and recovery |
| **[HALO Control](https://github.com/RaulMermans/AMD-HALO-Control)** | Control plane for a local AI workstation: model registry, capability routing, telemetry, workload authorization | Deterministic routing · metadata-only activity log · explicit mocked/real evidence classes |

<sub>JARVIS OS, Open VS Code Agent and HALO Control are public architecture editions of private systems. BI Notebook Lab, OpsTwin and DataBrief AI are open source.</sub>

**Progression:** analytical systems (BI Notebook Lab, OpsTwin) → applied AI (DataBrief AI) → AI agents (Open VS Code Agent) → agent systems (JARVIS OS) → local AI infrastructure (HALO Control).

#### Open source

**[OpenLIT: LangGraph memory connector](https://github.com/openlit/openlit/pull/1667)** (open pull request). A LangGraph Store memory connector with memory CRUD/search, namespace mapping, authentication, safe content handling, docs and integration tests.

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

Agent systems on local and open-weight models, with an emphasis on reliability, memory, evaluation and orchestration, and on analytical runtimes that explain their own results.
