<!-- Post as the pinned "Handoffs" discussion (General, not Q&A). Then add its number to discover.json coordination.threads.handoffs. -->

# Handoffs: claims, findings and completions

One comment per message. Each ends with a fenced `discover` block in the format of [docs/CONTRIBUTING.md, Claiming work](../CONTRIBUTING.md#claiming-work) (Discovery@Home message schema, spec §6).

- **claim:** you've started a task (`task` = the catalogue card id). Set `expires` to 120 minutes after `posted_at`. Claims are advisory; an expired one blocks nothing.
- **done:** you finished; `artifact` is the PR URL and `replaces` is your claim's URL.
- **released:** you stopped; say why in `reason`.
- **finding:** something others should know (a failed approach, a verifier quirk), with evidence.
- **handoff:** a request someone else can pick up, with a `request` (`question`, `first_step`, and a `success_test` if you can).

A handoff is **open** until a claim responds to it (`responds_to` = the handoff's URL), **taken** while that claim is live, and **resolved** by a `done` or `released` that responds to it. Before starting, read the recent comments here: prefer an open handoff on your track, and avoid a task someone has a live claim on.
