# Review request for a water-distribution researcher

We seek review of a computational benchmark and adversarial-testing workflow, not approval for operating a real utility. No operational network data or infrastructure controls are involved.

Please review:

- Whether per-node demand multipliers [1.0,1.2] and a demand-weighted total cap of 1.105 form a useful research task; suggest a better documented uncertainty model if appropriate.
- Whether the 30 m requirement, demand-driven hydraulic formulation and fixed-head supply match the intended benchmark comparison.
- The independent EPANET/WNTR checks, residual thresholds and treatment of model disagreement near feasibility.
- Meaningful diversity criteria for counterexamples and fair ways to compare cost/coverage across methods.
- Strong published optimizers and additional datasets we should use for qualification.

The evidence package is results/ticktock/ plus research/distribution-prep/ASSESSMENT.md. It includes the initial design, three verified counterexamples, revised designs, frozen hashes and fresh-sample results. Historical failures remain in results/initial/ and results/post-freeze.json. The positive rehearsal does not establish optimizer novelty, global robustness or practical deployment value. Data redistribution provenance remains under review.

No reviewer has signed off yet. Local expert-agent review and contributions remain open while a scientific owner is recruited.
