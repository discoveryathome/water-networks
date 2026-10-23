# Public source and research-results package

This repository imports the complete prepared source and project-authored evidence from local main commit `cb8b46ee0b08149170a34fe72ef0c280b2d5a003`. The original local repository and its complete historical input bundle are preserved separately. Public history begins with this source-and-results snapshot so omitted third-party assets cannot be recovered from old public commits.

All algorithms, validators, synthetic inputs, trial traces, result certificates, accepted rounds/frontiers and historical evidence manifests are included. Externally sourced input files are downloaded directly from their original hosts by `tools/fetch_inputs.py`, invoked by setup. SHA-256 hashes must match before use; derived inputs must reproduce the original bytes. They remain ignored by Git. No candidate score or feasibility rule is relaxed.

Downloaded archival reference pages, the unused published Pareto file and article snapshots, where applicable, are omitted. Their hashes remain in the original manifests and are explicitly accounted for by external-inputs.json; they are not needed for scientific checks. `tools/check.py` reports these omissions separately and continues verifying every required input and result.

Run `sh tools/setup.sh`, `.venv/bin/python tools/check.py`, and `.venv/bin/python tools/verify_active.py`. Setup requires network access to the listed original sources. CI does the same on Ubuntu.

Historical assessments describe their execution-time state. Current release status is in STATUS.md. Contributions are open while independent domain review remains pending; publication does not establish global novelty or practical deployment suitability.
