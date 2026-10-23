# Initial water-network qualification — 2026-10-23

A viable contribution harness and a modest gain on a precisely bounded scenario-design task, with an important generalization failure. Keep for another qualification round; do not call it a frontier result or a broadly robust design.

## Baseline reproduction

The historical Hanoi benchmark has 31 demand junctions,34 pipes, one fixed-head reservoir, and six discrete diameters. The Exeter input contains placeholder diameters. We preserve it and create a versioned design input with catalog diameters, demand-driven hydraulics, duration 0, tighter convergence settings and no topology changes. Costs use 1.1 D^1.5 per metre with D in inches; hydraulic diameters are converted to the toolkit's millimetres.

The published Table 8 diameter vector from Water 14(6),851(2022) is feasible under EPANET 2.2: minimum nominal pressure 30.006 m. Its exact-formula cost is 6,081,127.54; the paper reports 6,081,115.4 using rounded unit prices. This is a reproduced published reference, not a claim to current record authority. Six nominal search runs did not improve it.

## Two separately defined tasks

Nominal: all demand multipliers 1.0. Stress: nominal plus uniform 1.1 demand and two synthetic zone scenarios with 1.2 demand in one half of the junction IDs. All 31 junctions must have at least 30 mpressure in every task scenario. These zones/scenarios are synthetic benchmark choices, not calibrated forecasts. The stress objective has no direct literature-record comparison.

For the stress task, greedy repair/descent produced a feasible inherited cost 7,588,555.76. Each of two algorithms then received 4,000 design evaluations at each of three seeds. Multistart coordinate descent did not improve that baseline. Perturbation/repair improved it in two seeds:7,547,796.80 and 7,530,467.00. The best reduction is 0.7655%. Every evaluated design is logged; initialization cost is counted separately. This demonstrates limited local progress against our baseline, not superiority over current water-network optimization methods.

## Independent checking and counterevidence

All 12 search outputs and two task baselines passed independent WNTRSimulator checks in addition to EPANET. Checks cover catalog membership, input hashes, cost recomputation from input lengths, all task pressures, convergence, mass conservation and headloss residuals. Maximum pressure disagreement between engines was 0.000609 m. Code and hydraulic models still need human scientific review.

After freezing all candidates,20 additional random node-demand scenarios were drawn with multipliers in[1,1.2]. The stress baseline passed 19/20. The cheaper candidates passed 17/20 and 16/20 respectively, with worst pressures around 28 m. None is generally robust across this demand range. The nominal reference passed 0/20, as expected for this deliberately higher-demand test.

The savings trade away unmodeled demand coverage. Do not describe the cheaper design as dominating the baseline. Future work must treat cost and robustness together, and retain this failed holdout test as exposed evidence rather than reuse it as an unseen test set.

## Next round and outside help

1. Define a reproducible demand-uncertainty model and add counterexample search; distinguish sampled scenarios from a worst-case guarantee.
2. Compare a cost/coverage tradeoff against strong published optimization implementations under matched budgets. Our current greedy controls are insufficient for a frontier claim.
3. Add another licensed benchmark only after the first model's units and task definition are reviewed.
4. Ask a water-distribution optimization researcher to qualify demand assumptions, hydraulic tolerances, pressure requirements and baseline methods. A utility-specific deployment would need calibrated data and professional review; none is proposed here.

Local trials and expert-agent review are open. Public distribution remains pending dataset-rights review. No real infrastructure was operated and no external messages were sent.
