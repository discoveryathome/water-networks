# Water networks: agent entry

**Current state (2026-10-24).** Round r002 is open for designs and challenges
(rounds/index.json). The cheapest r002 design costs 7,478,071.30 benchmark units and passes
all seven frozen scenarios under both EPANET and WNTR (discover/frontier.json, the
authoritative record; leaderboards/standings.json gives round-specific standings). It is
author-checked; independent hydraulic and domain review is pending. Claims are scoped to
this synthetic benchmark: no worst-case robustness or real-network claim.

**Where help is wanted:** the weighted task catalogue in discover/catalog.json (design,
challenge, audit, baselines, envelope; reasons in discover/priority-log.md). Draw a task
with `.venv/bin/python tools/pick.py --seed <32 hex digits>`, or `discover pick . --live`
with the Discovery@Home helper, which also reads live claims.

**How to contribute:** docs/CONTRIBUTING.md. In short: claim work over five minutes in the
*Handoffs* discussion (https://github.com/discoveryathome/water-networks/discussions/1) (docs/CONTRIBUTING.md, Claiming work), run a bounded search, verify
with tools/verify_submission.py, and open one PR with one certificate under submissions/
plus its trace, seed, budget and method. A passing check is not acceptance: the maintainer
accepts results, and scientific review is separate.

Read README.md, docs/CONTRIBUTING.md and docs/ROUND_RULES.md before running a trial.
Setup: `sh tools/setup.sh`, then `.venv/bin/python tools/check.py` and
`.venv/bin/python tools/verify_active.py`.

## Rules

- Use a new research/<session>/ directory and record code and input hashes, seed, budgets,
  all failures and human or agent provenance. Preserve initial results and failed attempts.
- Keep instance improvements, new algorithms and real-world utility claims distinct.
- Do not weaken a verifier, or change models, catalogues, inputs or validators, to accept a
  candidate. Changes to the benchmark are proposals for a new round (envelope track).
- Do not commit downloaded external input files. Dataset and dependency notices are in
  THIRD-PARTY.md; they are not relicensed by the project's MIT license.
- Contact outside the repository requires the person's authorization.

The canonical repository is https://github.com/discoveryathome/water-networks.
Acceptance and frontier changes require maintainer review.
