# Contributor workflow

1. Read the current round in rounds/index.json and docs/ROUND_RULES.md. Check installation with tools/check.py and tools/verify_active.py.
2. Choose a task (see Choosing work below), and claim it if it will take more than five minutes (Claiming work). Run tools/contribute.py with an explicit seed, budget and fresh output directory, or implement a different method using the same verifier.
3. Submit one JSON certificate under submissions/, together with the complete attempt trace, seed, evaluation budget and method description. Use tools/verify_submission.py locally.
4. A design should show cost relative to the accepted design for that round. A challenge should identify its registered target and reproduce the pressure violation. Neither changes the round automatically.
5. Maintainer acceptance follows computational verification; scientific claims need separate review. Do not alter models, catalogs, inputs or validators in a candidate-only PR.

CI includes a candidate-only workflow which reads submitted JSON but runs the base revision's checker. Separate build CI checks code changes. Both run on GitHub.

A bounded null result with its complete trace is useful.

## Choosing work

The task catalogue is discover/catalog.json: five weighted tracks (design, challenge, audit, baselines, envelope), each with task cards stating the question, a first step with its expected output, and what a finished contribution needs. Draw a task from a seed rather than picking the obvious one, so many contributors spread across the work:

```sh
.venv/bin/python tools/pick.py --seed <32 hex digits>
```

The Discovery@Home helper gives the same draw and also reads live claims: `discover pick . --live`. Prefer an open handoff on your track over a fresh card. The weights and the reasons for them are in discover/priority-log.md.

## Claiming work

Coordination happens in the repository's [Discussions](https://github.com/discoveryathome/water-networks/discussions): a pinned *Start here* thread, and a *Handoffs* thread for claims, findings, handoffs and completions, one comment each. Claims are advisory: they tell others what is taken, and an expired claim blocks nothing.

For work over five minutes, post a claim in *Handoffs* as soon as you've chosen a task: a line of prose ending with a fenced `discover` block. Set `task` to the card id, `base` to the commit of main you start from (`git rev-parse HEAD` in a fresh clone), and `expires` to `posted_at` plus 120 minutes (`claim_ttl_minutes` in discover.json). For example:

````markdown
Claiming challenge-r002: targeted search on the low-margin junctions against design-1301.

```discover
{"v": 0, "kind": "claim", "task": "challenge-r002", "scope": "r002 demand counterexample against design-1301; local search from the worst of 2,000 envelope samples, junctions with under 1 m margin; seed 4242, budget 4,000", "base": "3fa1fb079dd6505a215886028a861076fb50b5b4", "priority_revision": 1, "posted_at": "2026-10-24T18:00:00Z", "expires": "2026-10-24T20:00:00Z"}
```
````

End a claim with a new comment in the same thread, with the same `task` and `scope`:

- `done`: `"kind": "done"`, `"artifact"` set to the PR URL, and `"replaces"` set to the claim comment's URL.
- `released`: `"kind": "released"` and a `"reason"` saying why work stopped.

A handoff is a request someone else can pick up: `"kind": "handoff"` with a `request` (`question`, `first_step`, and optionally `success_test`, `track`, `est_minutes`). Its lifecycle is visible in the thread:

- **Open:** a handoff with no claim responding to it.
- **Taken:** a claim whose `"responds_to"` is the handoff comment's URL, until it expires.
- **Resolved:** a `done` whose `"responds_to"` is the handoff's URL, or a `released` with the reason.

For example, after a design run that found nothing cheaper:

````markdown
Handing off: perturb-repair at 8,000 evaluations didn't beat 7,478,071.30 at five seeds; a different move set is the next thing to try.

```discover
{"v": 0, "kind": "handoff", "task": "design-search", "scope": "r002 design search; perturb-repair exhausted at 8,000 evaluations x 5 seeds", "base": "3fa1fb079dd6505a215886028a861076fb50b5b4", "priority_revision": 1, "posted_at": "2026-10-24T21:00:00Z", "request": {"question": "Does a paired up/down diameter move find an r002 design below 7,478,071.30?", "first_step": ".venv/bin/python tools/contribute.py design --budget 64 --seed 1 --out research/first-step-design", "success_test": "tools/verify_submission.py passes with cost below 7478071.30", "track": "design", "est_minutes": 60}}
```
````

For work under five minutes, skip the claim and post only `done` or a `finding`. Without permission to post, save the same messages in your research/<session>/ folder and put them in the PR description. The message format is Discovery@Home's (spec §6, https://discoveryathome.org/schema/v0/message.schema.json); the hub's helper writes it with `discover post`.

## Credit

Credit goes to upstream methods and data and to every substantive contributor, with AI assistance disclosed. When a verified design or a distinct verified counterexample is accepted into a round, its author is credited by GitHub handle in that round's records and in leaderboards/standings.json. Near-copies of an existing challenge aren't credited separately (docs/ROUND_RULES.md).

## Useful work beyond the catalogue

Improve challenge diversity screening; test another search method under equal evaluation budgets; independently review units and hydraulic tolerances; audit the synthetic demand envelope. Each has a card in the catalogue; propose new cards in the Discussions *Proposals* thread or an issue.

## After accepting a round or frontier

After accepting a new round or frontier, preserve existing catalogs and trial evidence. Update standings and append the new evidence hashes to research/distribution-prep/manifest.json; never overwrite earlier certificates or delete their hash entries. Update discover/frontier.json, and record the change in discover/priority-log.md. Run both tools/check.py and tools/verify_active.py.
