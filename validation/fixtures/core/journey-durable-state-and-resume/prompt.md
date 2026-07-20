# One conversation, resumed after Turn 5

Use a fresh isolated workspace with no project instructions, decision log, or
state-tracking convention.

## Turn 1

$deliberation Activate Deliberation for this conversation. Do not start an
engineering task yet.

## Turn 2

Design a specification for an asynchronous order-fulfillment flow spanning an
API, inventory reservation, payment authorization, and fulfillment. Explain
the dynamic behaviour as a request or user journey from the initial request to
the observable outcome, including important state changes and failure paths.

Prepare a provisional roadmap and a decision-ready checkpoint for the first
milestone. Do not create or modify files.

## Turn 3

Approve the first milestone with these decisions: accept the order only after
inventory is reserved and payment is authorized; compensate a successful
reservation if payment fails; expose Pending, Accepted, and Rejected as the
client-visible states. Complete only that specification milestone in the
conversation. Do not create or modify files.

## Turn 4

Summarize the accepted decisions, completed milestone, remaining roadmap, and
the next approval boundary. Keep the state only in this conversation and do
not create or modify files.

## Turn 5

Record the accepted decisions and current roadmap durably in
docs/DECISIONS.md. This repository has no existing tracking convention, and I
explicitly authorize creating that file for this purpose. Preserve the
substance of every accepted decision. Then present the next milestone and its
approval scope, but do not execute it.

# Host action

Archive or otherwise leave the task, then later reopen the same Codex Desktop
conversation. Do not send another activation command.

## Turn 6 after resume

Continue from where we left off. State whether Deliberation is active, recap
the accepted decisions and current roadmap, and identify exactly what is and
is not approved. Do not execute the pending milestone and do not modify files.
