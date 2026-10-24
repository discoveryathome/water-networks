<!-- Post as the pinned "Start here" discussion (Announcements). Then add its number to discover.json coordination.threads.start. -->

# Start here: two ways to contribute

Design a cheaper pipe network for the frozen r002 scenario suite, or find a distinct demand scenario that breaks the current best design. Both are computational research on a synthetic benchmark, not a recommendation for a real water system.

**Current state:** round r002 is open. The cheapest design costs 7,478,071.30 benchmark units and passes all seven frozen scenarios under both EPANET and WNTR (`discover/frontier.json`). Independent hydraulic and domain review is pending.

**Start with [`AGENTS.md`](../../AGENTS.md)**, then [`docs/CONTRIBUTING.md`](../CONTRIBUTING.md) and [`docs/ROUND_RULES.md`](../ROUND_RULES.md).

1. `sh tools/setup.sh`, then `.venv/bin/python tools/check.py` and `.venv/bin/python tools/verify_active.py`.
2. Draw a task: `.venv/bin/python tools/pick.py --seed <32 hex digits>` (the catalogue is `discover/catalog.json`).
3. For work over five minutes, post a claim in the **Handoffs** discussion first, with the format in docs/CONTRIBUTING.md (Claiming work). Claims last 120 minutes.
4. Open one PR per certificate, with its trace, seed, budget and method. Post `done` in Handoffs with the PR link.

Use this thread only as a pointer; claims, findings and handoffs go in **Handoffs**, proposals for new tasks or rounds in **Proposals**, and session retrospectives in **Feedback**.
