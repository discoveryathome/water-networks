# Contributor workflow

1. Read the current round in rounds/index.json and docs/ROUND_RULES.md. Check installation with tools/check.py and tools/verify_active.py.
2. Choose a design or challenge task. Run tools/contribute.py with an explicit seed, budget and fresh output directory, or implement a different method using the same verifier.
3. Submit one JSON certificate under submissions/, together with the complete attempt trace, seed, evaluation budget and method description. Use tools/verify_submission.py locally.
4. A design should show cost relative to the accepted design for that round. A challenge should identify its registered target and reproduce the pressure violation. Neither changes the round automatically.
5. Maintainer acceptance follows computational verification; scientific claims need separate review. Do not alter models, catalogs, inputs or validators in a candidate-only PR.

CI includes a candidate-only workflow which reads submitted JSON but runs the base revision's checker. Separate build CI checks code changes. Both run on GitHub. Pinned discussion drafts are under docs/discussions/ and have not been posted.

Useful first issues: improve challenge diversity screening; test another search method under equal evaluation budgets; independently review units and hydraulic tolerances; audit the synthetic demand envelope. A bounded null result with its complete trace is useful.

After accepting a new round or frontier, preserve existing catalogs and trial evidence. Update standings and append the new evidence hashes to research/distribution-prep/manifest.json; never overwrite earlier certificates or delete their hash entries. Run both tools/check.py and tools/verify_active.py.
