# Frozen rounds and two-sided credit

## Demand envelope

Every junction multiplier is between 1.0 and 1.2. The total demand, weighted by original junction demands, is at most 1.105 times the original total. This forbids the trivial challenge of increasing every junction to 1.2. These are synthetic qualification assumptions, not calibrated water-system forecasts. All prior four design scenarios fit the envelope.

## Design submissions

A design binds the round ID, canonical round digest, network digest, 34 discrete pipe choices, cost and provenance. Cost is recalculated from pipe lengths and the frozen catalog. Every scenario in that round must meet 30 m pressure under EPANET and the separate WNTR solver. Residual and convergence checks still apply. No pressure feasibility tolerance is added to the requirement.

Round-specific design standing is cost among verified feasible designs. Reproductions and failed search reports are welcome but are not cost improvements. Do not compare different rounds as if they had identical constraints.

## Challenge submissions

A challenge binds an immutable registered target-design digest and a round. The demand vector must lie in the envelope. Both solvers must show at least 0.005 m pressure shortfall; they must agree within 0.001 m and pass residual checks. A solver failure is not itself a valid counterexample.

A candidate must be at least 0.02 away in maximum component difference from existing round scenarios and previously curated challenges. This inexpensive duplicate screen is a first policy, not a scientific diversity metric. A reviewer should improve it if many geometrically different vectors expose the same underlying failure.

Display confirmed pressure shortfall, target, demand total and novelty separately. Credit a distinct verified counterexample, not repeated near-copies. There is no arbitrary combined cost/robustness score. The validator does not automatically publish rankings or accept changes to the scenario suite.

## Advancing a round

The maintainer reviews valid challenges, selects a small useful set, and uses tools/prepare_next_round.py to create a proposed round. The previous round remains immutable. Before activation, review the proposed assumptions, establish a feasible inherited design using both checkers, version the new round and baseline, and update rounds/index.json. Expert review can be recorded separately from computational verification.

During the rehearsal, r002 inherited r001's four scenarios plus three verified counterexamples. Random fresh evaluation occurred only after all revised designs were frozen. Those 128 samples are now exposed evidence; do not reuse them as an unseen test set.

This workflow does not prove worst-case robustness. Independent adversarial searches and appropriate uncertainty modeling remain useful contributions even when a design passes every published scenario.
