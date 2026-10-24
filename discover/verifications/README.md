# Independent verifications

One file per independent check of the current round's certificates or the frontier record: `<YYYY-MM-DD>-<handle>.json` with `verifier`, `verified_on`, `package_commit` (the commit checked), `method` (replayed / audited / reimplemented), `outcome` (confirmed / failed / partial), `scope`, `not_checked`, `evidence` and `independent` (Discovery@Home spec §9.1). The audit track's cards (discover/catalog.json) produce these. The maintainer records decisions in discover/ledger.jsonl.
