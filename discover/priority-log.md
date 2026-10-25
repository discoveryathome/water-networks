# Priority log

## Revision 1 — 2026-10-24

Catalogue revision 1 (`discover/catalog.json`), written when the project was prepared
for listing on the Discovery@Home hub.

| Track | Weight | Why |
|---|---:|---|
| design | 35 | The objective (r002 cost under seven frozen scenarios, both solvers) is well defined and exactly verified, and only the project's own two searches have tried it. Better search is the most direct way to move the frontier. |
| challenge | 25 | Each verified, distinct counterexample makes the next round's scenario suite harder to overfit. This is the project's second half, and it's cheap to check. |
| audit | 20 | Nothing has been reproduced off the author's machine and CI, and the hydraulic model has had no independent review. Audits filter work before it reaches the maintainer. |
| baselines | 10 | Without a strong published optimizer on r002, a cheaper design shows progress against this project's searches, not against the field. |
| envelope | 10 | The demand envelope and the duplicate screen are declared first policies. Better ones become a new round, so this work moves slower and needs maintainer review. |

Bottleneck: `search`. The project's claims are scoped to the stated benchmark, so the open
question of whether the synthetic envelope reflects real networks is tracked as the
`demand-envelope` assumption and the envelope track, not as the bottleneck.

Next review: after the first ten contributions, when a challenge against r002 is verified
(which may call for round r003), or by 2026-11-07, whichever comes first.
