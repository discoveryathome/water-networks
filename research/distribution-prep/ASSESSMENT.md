# Distribution preparation and complete rehearsal

The two-sided workflow is implemented and was exercised once. Round r001 registers the previous baseline and cheaper design against the original four scenarios. Challenge search evaluated 512 fixed random vectors inside a newly declared envelope: node multipliers [1,1.2], demand-weighted mean at most 1.105. Three distinct counterexamples were verified by both solvers, with confirmed pressure shortfalls about 0.605, 0.516 and 0.407 m.

Round r002 freezes the original scenarios plus those three challenges. Greedy repair/descent produced a 7,490,876.73-cost control. Two bounded 4,000-evaluation search runs both reached 7,478,071.30. Both revised outputs and their control passed all seven scenarios with both solvers.

On 128 new, post-freeze samples inside the same envelope:

| Design | Cost | Scenarios passed |
|---|---:|---:|
| Earlier baseline | 7,588,555.76 | 128/128 |
| Earlier cheaper design | 7,530,467.00 | 125/128 |
| Revised greedy control | 7,490,876.73 | 128/128 |
| Revised search designs | 7,478,071.30 | 128/128 |

The revised search design is about 0.70% cheaper than the earlier cheaper design and 1.46% cheaper than the earlier baseline. It improves the observed cost/coverage tradeoff in this rehearsal. The extra training scenarios and additional computation were both changed, so this does not isolate the causal effect of challenge selection or establish algorithmic superiority.

The new total-demand cap differs from the earlier uncapped [1,1.2] random stress test. Do not compare their pass rates as identical experiments. All new sampled results remain sampling evidence, not a worst-case certificate. The 128 samples are now exposed and should not be reused as unseen validation.

Pre-release workflow is ready for limited research sharing: frozen rounds, two certificate types, duplicate screening, separate standings, negative verifier tests, active-artifact checks, starter commands, contributor templates and unposted discussion drafts are included. Fresh macOS setup is checked. Linux automation is prepared but unexecuted locally because Docker is unavailable. Scientific assumption review and historical input redistribution terms remain open items before wider public packaging.

The candidate-PR verifier was also rehearsed in an isolated Git repository: a valid certificate passed despite a deliberately broken verifier on the candidate branch, while a forged metric failed. The trusted base checker handled both; candidate code was not executed. See pr-check-rehearsal.json.
