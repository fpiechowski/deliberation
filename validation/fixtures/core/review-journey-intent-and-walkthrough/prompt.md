# Harness setup

Before the review request, copy the fixture `seed/` files into `work/` in a
fresh isolated workspace. Do not add project instructions or other files.

# One conversation

## Turn 1

$deliberation Activate Deliberation for this conversation. Do not start an
engineering task yet.

## Turn 2

Review `work/auth_gateway.py` and `work/test_auth_gateway.py` for an upcoming
change from an internal service to an internet-facing gateway.

Explain the implemented behavior as a request journey from the incoming
Authorization header through credential parsing, session lookup, revocation and
scope decisions, to the observable status code. Identify material findings and
tradeoffs around the currently supported bare-token compatibility path.

Run tests or inspect files as needed, but do not modify anything. Treat the
final release recommendation as consequential. Prepare a decision-ready
checkpoint for a bounded milestone that would record the approved review in
`work/review.md`, including what it would and would not authorize. Wait for
approval before creating the artifact.

## Turn 3

Sounds good, but before I approve: why should accepting a bare token be
release-blocking if the token still has to match a live, scoped session? Do not
modify files.

## Turn 4

Yes, but revise the recommendation: make release conditional on a 30-day
legacy bare-token migration with telemetry, client notification, a fixed
cutoff, and immediate rejection of malformed explicit schemes. Update the
checkpoint and approval scope. Do not modify files yet.

## Turn 5

Approve the revised review recommendation. Write only `work/review.md`; do not
modify the source or tests. Verify the seeded tests and source/test hashes, then
provide the final review walkthrough and completion status.
