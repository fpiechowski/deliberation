# Codex Desktop journey, durable-state, and resumed-conversation transcript

- **Executed:** 2026-07-20
- **Product version:** `0.1.0-dev.1`
- **Host:** Codex desktop app for Windows, package `26.715.4045.0`
- **Surface:** standalone user skill
- **Fixture:** `core-journey-durable-state-and-resume`
- **Thread:** `019f7ea6-da81-7381-a1fb-832d471481aa`
- **Workspace:** isolated projectless task

The standalone artifact was installed temporarily in the user skill scope. The same task was archived and unarchived between Turns 5 and 6.

## Turn 1

### User

```text
$deliberation Activate Deliberation for this conversation. Do not start an engineering task yet.
```

### Codex final answer

> Deliberation is active for this conversation until you explicitly disable it. I’ll use bounded milestones, decision-ready checkpoints, and explicit approval before consequential engineering actions.
>
> No engineering task has been started.

## Turn 2

### User

```text
Design a specification for an asynchronous order-fulfillment flow spanning an API, inventory reservation, payment authorization, and fulfillment. Explain the dynamic behaviour as a request or user journey from the initial request to the observable outcome, including important state changes and failure paths.

Prepare a provisional roadmap and a decision-ready checkpoint for the first milestone. Do not create or modify files.
```

### Codex commentary

> Deliberation is shaping this into a bounded specification exercise. I’ll outline the full journey provisionally, then pause at the first material decision—acceptance semantics, sequencing, and lifecycle—without creating or modifying files.

### Codex final answer

> Deliberation remains active. No files were created or modified.
>
> ## Provisional roadmap
>
> 1. **Lifecycle and processing semantics**
>    Define API acceptance, idempotency, orchestration ownership, operation ordering, order states, and core invariants.
>
> 2. **Component contracts**
>    Specify commands, events, correlation identifiers, versioning, inventory holds, payment authorizations, and fulfillment handoff.
>
> 3. **Failure and recovery model**
>    Define retries, timeouts, ambiguous outcomes, compensation, reconciliation, dead-letter handling, and manual intervention.
>
> 4. **Observable client behavior**
>    Specify status retrieval, webhooks, ordering guarantees, error representation, cancellation behavior, and terminal outcomes.
>
> 5. **Operational acceptance criteria**
>    Cover security, auditability, observability, performance targets, retention, testing scenarios, and rollout constraints.
>
> Each milestone should leave a reviewable specification section. Approval of the first milestone would not authorize the later milestones.
>
> ## Provisional request journey
>
> This is the recommended end-to-end direction, subject to the first checkpoint below.
>
> 1. **Submit the order**
>
>    The client sends `POST /orders` with an idempotency key, customer information, line items, amount/currency, and payment-method reference.
>
>    The API validates the request, durably creates one order, and returns `202 Accepted` with:
>
>    - `orderId`
>    - status such as `PROCESSING`
>    - a status URL
>    - the accepted order version
>
>    A retry using the same idempotency key and equivalent content returns the same order. Reusing the key with different content is rejected.
>
> 2. **Reserve inventory**
>
>    The order moves conceptually through:
>
>    `ACCEPTED → RESERVING_INVENTORY → INVENTORY_RESERVED`
>
>    The inventory service creates a time-bounded reservation identified by `orderId` and a stable operation ID.
>
>    If stock is unavailable, the order becomes `REJECTED_OUT_OF_STOCK`. No payment authorization is attempted.
>
> 3. **Authorize payment**
>
>    The order moves through:
>
>    `INVENTORY_RESERVED → AUTHORIZING_PAYMENT → PAYMENT_AUTHORIZED`
>
>    Payment authorization uses its own idempotent operation ID.
>
>    If payment is declined, the inventory reservation is released and the externally visible order becomes `REJECTED_PAYMENT`. While release is incomplete, the internal state remains compensating rather than falsely reporting full cleanup.
>
> 4. **Commit stock and request fulfillment**
>
>    After payment authorization, the temporary hold is converted into an allocation that will not expire during normal fulfillment:
>
>    `PAYMENT_AUTHORIZED → READY_FOR_FULFILLMENT → FULFILLMENT_REQUESTED`
>
>    Fulfillment receives an idempotent request containing the order, delivery details, allocation reference, and payment-authorization reference.
>
> 5. **Fulfill the order**
>
>    Once fulfillment durably accepts ownership:
>
>    `FULFILLMENT_REQUESTED → FULFILLMENT_ACCEPTED → FULFILLED`
>
>    Additional domain states such as `PACKED` and `SHIPPED` can be introduced later if clients need that granularity.
>
> 6. **Expose the outcome**
>
>    The client observes progress through `GET /orders/{orderId}` and optionally webhooks. Notifications are hints rather than the source of truth: they may be duplicated or delivered out of order, so each carries `orderId` and a monotonically increasing order version.
>
> ## Important failure paths
>
> - **Invalid initial request:** synchronous `4xx`; no order is created.
> - **Duplicate submission:** resolves to the existing order through the idempotency key.
> - **Inventory rejection:** terminal `REJECTED_OUT_OF_STOCK`.
> - **Payment decline:** release inventory, then expose `REJECTED_PAYMENT`.
> - **Dependency timeout:** outcome is treated as unknown, not failed. The orchestrator retries with the same operation ID and reconciles by querying the dependency.
> - **Worker or process crash:** durable state and messages allow processing to resume without repeating the business effect.
> - **Fulfillment rejection before acceptance:** verify that fulfillment did not accept the order, then void the authorization and release the allocation.
> - **Ambiguous fulfillment handoff:** do not compensate until ownership is reconciled; otherwise goods could ship after payment and stock were released.
> - **Failure after fulfillment accepts ownership:** move to a fulfillment exception or manual-review state. Automatic rollback is no longer assumed safe.
> - **Notification failure:** retry delivery without changing order processing; clients can still retrieve authoritative status.
>
> The design assumes at-least-once message delivery with idempotent consumers, not impossible-to-guarantee end-to-end exactly-once execution.
>
> ## First milestone checkpoint
>
> **Decision needed:** approve the foundational lifecycle and processing model.
>
> **Recommendation:**
>
> - Return `202 Accepted` only after the order and orchestration intent are durable.
> - Use a single order workflow/orchestrator as the lifecycle authority.
> - Reserve inventory before authorizing payment.
> - Convert the temporary reservation into a durable allocation before fulfillment.
> - Use at-least-once delivery, stable operation IDs, idempotent handlers, and reconciliation.
> - Keep one authoritative internal state machine while exposing a smaller, stable public status set.
> - Treat dependency timeouts as ambiguous outcomes.
> - Make `GET /orders/{orderId}` authoritative; webhooks may be duplicated or reordered.
> - Defer payment capture semantics because the requested scope specifies authorization, not capture.
>
> **Why this is preferred:** it avoids authorizing payment for known-unavailable goods, makes asynchronous acceptance honest, prevents expiring reservations during fulfillment, and handles crashes or uncertain network outcomes without pretending distributed exactly-once processing exists.
>
> **Material alternatives:**
>
> - **Authorize payment before reserving stock:** reduces inventory hold time but creates more authorization reversals when stock is unavailable.
> - **Run inventory and payment concurrently:** lowers latency but makes compensation routine and introduces races before either prerequisite is known.
> - **Use choreography without an order orchestrator:** reduces central coordination but makes cross-service state, recovery, and client-facing explanations substantially harder to reason about.
> - **Expose every internal state publicly:** offers more detail but tightly couples clients to recovery mechanics and limits future changes.
>
> Approval would authorize only **Milestone 1**: turning this direction into a precise lifecycle specification with public/internal states, transitions, invariants, idempotency rules, and completion criteria. It would not yet authorize detailed message schemas, retry policies, compensation algorithms, operational targets, or implementation.
>
> Please approve, revise, reject, or question this first-milestone direction.

## Turn 3

### User

```text
Approve the first milestone with these decisions: accept the order only after inventory is reserved and payment is authorized; compensate a successful reservation if payment fails; expose Pending, Accepted, and Rejected as the client-visible states. Complete only that specification milestone in the conversation. Do not create or modify files.
```

### Codex commentary

> The revised checkpoint is approved. I’m applying the three decisions as authoritative: business acceptance follows both prerequisites, payment failure triggers inventory compensation, and the public lifecycle is limited to `Pending`, `Accepted`, and `Rejected`. I’ll complete only the lifecycle/processing-semantics milestone and then stop.

### Codex final answer

> ## Milestone 1 — Lifecycle and Processing Semantics
>
> Status: **completed in conversation only**. No files were created or modified.
>
> ### 1. Scope
>
> This milestone defines:
>
> - The distinction between receiving and accepting an order.
> - The inventory-before-payment sequence.
> - Internal lifecycle states and transitions.
> - The three client-visible states.
> - Idempotency and duplicate-delivery semantics.
> - Foundational failure and compensation rules.
> - The boundary between order acceptance and fulfillment.
>
> Detailed schemas, retry schedules, payment capture, reservation expiry after acceptance, and fulfillment execution remain outside this milestone.
>
> ### 2. Core terminology
>
> - **Received:** The system has durably recorded the order submission.
> - **Pending:** The order is being evaluated or compensated. No business acceptance has occurred.
> - **Accepted:** Inventory is successfully reserved and payment is successfully authorized.
> - **Rejected:** A prerequisite failed definitively, and any required inventory compensation has completed.
> - **HTTP `202 Accepted`:** A protocol-level acknowledgement of asynchronous processing. It does not mean that the order has reached the domain state `Accepted`.
>
> ### 3. Client request journey
>
> 1. The client submits `POST /orders` with an idempotency key.
> 2. The API performs synchronous structural and business-input validation.
> 3. If valid, the system durably records the submission and its processing intent.
> 4. The API returns `202` with an order identifier, status URL, and public state `Pending`.
> 5. The workflow requests an inventory reservation.
> 6. If inventory is reserved, the workflow requests payment authorization.
> 7. The order becomes:
>
>    - `Accepted` when both operations succeed.
>    - `Rejected` when inventory definitively fails.
>    - `Rejected` after inventory is released when payment definitively fails.
>    - `Pending` while an outcome is unknown, retryable, or being compensated.
>
> After `Accepted`, fulfillment may begin. The fulfillment lifecycle is not encoded in the three order-acceptance states defined here.
>
> ### 4. Public state model
>
> | Public state | Meaning |
> |---|---|
> | `Pending` | The submission is durable, but acceptance has not completed. This includes active processing, uncertain dependency outcomes, and compensation. |
> | `Accepted` | A valid inventory reservation and payment authorization were both durably confirmed. |
> | `Rejected` | Acceptance failed definitively. No successful payment authorization exists, and any inventory reservation created during the attempt has been released. |
>
> A reason field may accompany the state without expanding the public state set. Initial reason categories are:
>
> - `OUT_OF_STOCK`
> - `PAYMENT_DECLINED`
> - `PAYMENT_UNAVAILABLE`
> - `INVALIDATED_DURING_PROCESSING`
>
> Exact public error codes belong to the component-contract milestone.
>
> ### 5. Internal state model
>
> ```text
> RECEIVED
>    ↓
> RESERVING_INVENTORY
>    ├── definitive failure ───────────────────────→ REJECTED
>    ├── unknown outcome ─→ INVENTORY_UNCERTAIN ──┐
>    └── success ──────────────────────────────────→ INVENTORY_RESERVED
>                                                     ↓
>                                             AUTHORIZING_PAYMENT
>                                                     ├── unknown outcome
>                                                     │       ↓
>                                                     │ PAYMENT_UNCERTAIN
>                                                     │
>                                                     ├── definitive failure
>                                                     │       ↓
>                                                     │ RELEASING_INVENTORY
>                                                     │       ↓
>                                                     │ REJECTED
>                                                     │
>                                                     └── success
>                                                             ↓
>                                                    PAYMENT_AUTHORIZED
>                                                             ↓
>                                                         ACCEPTED
>                                                             ↓
>                                                  fulfillment boundary
> ```
>
> Public mapping:
>
> | Internal state | Public state |
> |---|---|
> | `RECEIVED` | `Pending` |
> | `RESERVING_INVENTORY` | `Pending` |
> | `INVENTORY_UNCERTAIN` | `Pending` |
> | `INVENTORY_RESERVED` | `Pending` |
> | `AUTHORIZING_PAYMENT` | `Pending` |
> | `PAYMENT_UNCERTAIN` | `Pending` |
> | `RELEASING_INVENTORY` | `Pending` |
> | `PAYMENT_AUTHORIZED` | `Pending` until the acceptance transition is durable |
> | `ACCEPTED` | `Accepted` |
> | `REJECTED` | `Rejected` |
>
> ### 6. Transition rules
>
> #### Inventory succeeds
>
> A successful reservation must include a stable reservation identifier and confirmation that the reservation is valid.
>
> The workflow records that result before requesting payment authorization.
>
> #### Inventory fails
>
> A definitive inventory rejection moves the order directly to `Rejected`. Payment must not be attempted.
>
> A timeout or ambiguous response does not prove failure. The order remains `Pending` while the workflow retries or reconciles the reservation using the same operation identity.
>
> #### Payment succeeds
>
> Payment authorization must reference the order, amount, currency, and a stable authorization operation identifier.
>
> The order may move to `Accepted` only after both the inventory reservation and payment authorization are durably recorded.
>
> The transition to `Accepted` also creates durable intent for the future fulfillment handoff. The exact handoff contract is deferred.
>
> #### Payment fails
>
> A definitive payment failure must not immediately expose `Rejected` if inventory was reserved.
>
> The order enters `RELEASING_INVENTORY`, which remains publicly `Pending`. It becomes `Rejected` only after the reservation release is confirmed or reconciliation proves that no reservation remains.
>
> A payment timeout or unknown provider outcome remains `Pending`; inventory must not be released until reconciliation establishes that payment authorization did not succeed.
>
> ### 7. Lifecycle invariants
>
> The system must preserve these rules:
>
> 1. `Accepted` implies a confirmed inventory reservation and confirmed payment authorization.
> 2. Payment authorization must never begin before inventory reservation succeeds.
> 3. `Rejected` implies that no payment authorization succeeded.
> 4. `Rejected` also implies that no reservation from the acceptance attempt remains active.
> 5. Ambiguous dependency outcomes must not be interpreted as failures.
> 6. A successful reservation followed by definitive payment failure must be compensated.
> 7. A public state transition from `Pending` to `Accepted` or `Rejected` is terminal for the acceptance lifecycle.
> 8. `Accepted` must never later become `Rejected` because of a fulfillment failure.
> 9. Duplicate requests or messages must not create additional reservations, authorizations, or orders.
>
> Invariant 8 means future fulfillment progress or failure must be represented separately from the three acceptance states—for example through fulfillment details or a fulfillment subresource. That representation is not selected in this milestone.
>
> ### 8. Idempotency and concurrency semantics
>
> - `POST /orders` requires an idempotency key within a defined client or tenant scope.
> - The same key with an equivalent normalized payload returns the original order.
> - The same key with materially different content is rejected as an idempotency conflict.
> - Inventory reservation, inventory release, and payment authorization each use distinct stable operation identifiers derived from the order and operation purpose.
> - Repeated delivery of the same command must return or reconstruct the original business result.
> - Every lifecycle transition uses an order version or equivalent compare-and-set guard.
> - Stale and duplicate results may be recorded for audit but must not regress state.
> - Workflow state and outbound processing intent must be committed atomically, such as through a transactional outbox.
> - The model assumes at-least-once delivery with idempotent effects, not distributed exactly-once execution.
>
> ### 9. Observable behavior
>
> A client retrieving an order sees:
>
> - `Pending` from durable receipt through prerequisite processing or compensation.
> - `Accepted` after both prerequisites have succeeded.
> - `Rejected` after definitive failure and required cleanup.
>
> Clients must not infer failure merely because an order remains `Pending` for a long time. Later milestones must define timestamps, timeout presentation, support escalation, and notifications.
>
> Because fulfillment is outside this public state model, `Accepted` means “accepted for fulfillment,” not “fulfilled” or “shipped.”
>
> ### 10. Scenario verification
>
> | Scenario | Expected result |
> |---|---|
> | Inventory succeeds; payment succeeds | `Pending → Accepted` |
> | Inventory definitively rejects | `Pending → Rejected`; payment is not attempted |
> | Inventory succeeds; payment declines | `Pending`; release inventory; then `Rejected` |
> | Inventory request times out | Remain `Pending`; reconcile without starting payment prematurely |
> | Payment request times out | Remain `Pending`; reconcile before releasing inventory |
> | Payment succeeds but response is lost | Idempotent reconciliation recovers the authorization; order can become `Accepted` |
> | Inventory release temporarily fails | Remain `Pending`; do not falsely claim compensated rejection |
> | Client repeats `POST /orders` | Return the existing order; create no duplicate effects |
> | Fulfillment later fails | Order remains `Accepted`; fulfillment outcome is represented separately |
>
> All approved lifecycle decisions are reflected in the specification, and the milestone’s invariants are consistent with the scenario checks.
>
> The next provisional milestone would define component commands, events, and data contracts, but it has not been started. Deliberation remains active, and nothing remains for the approved first milestone.

## Turn 4

### User

```text
Summarize the accepted decisions, completed milestone, remaining roadmap, and the next approval boundary. Keep the state only in this conversation and do not create or modify files.
```

### Codex final answer

> Deliberation remains active, with state kept only in this conversation. No files were created or modified.
>
> ### Accepted decisions
>
> - Orders are processed asynchronously.
> - Business acceptance occurs only after inventory reservation and payment authorization both succeed.
> - Inventory is reserved before payment is authorized.
> - A definitive payment failure triggers release of the successful reservation.
> - The public states are limited to `Pending`, `Accepted`, and `Rejected`.
> - `Pending` includes active processing, uncertain outcomes, and compensation.
> - `Rejected` is exposed only after required inventory compensation completes.
> - Dependency timeouts are treated as ambiguous outcomes, not failures.
> - Processing uses at-least-once delivery, stable operation IDs, idempotent effects, and guarded state transitions.
> - `Accepted` means accepted for fulfillment—not fulfilled—and cannot later become `Rejected` because fulfillment fails.
> - Fulfillment progress and outcomes will require a separate representation.
>
> ### Completed milestone
>
> **Milestone 1: Lifecycle and processing semantics** is complete.
>
> It produced the request journey, public/internal state models, transition rules, lifecycle invariants, idempotency and concurrency semantics, observable behavior, and scenario-based verification.
>
> ### Remaining provisional roadmap
>
> 2. **Component contracts:** commands, events, identifiers, payloads, versioning, and fulfillment handoff.
>
> 3. **Failure and recovery:** retry policies, reconciliation, compensation failures, dead letters, and manual intervention.
>
> 4. **Client observability:** status details, webhooks, ordering, cancellation, and fulfillment visibility.
>
> 5. **Operational acceptance:** security, auditability, monitoring, performance, retention, tests, and rollout constraints.
>
> ### Next approval boundary
>
> No further specification work is authorized yet. Before Milestone 2 begins, a decision-ready checkpoint should establish the service interaction and contract direction—particularly orchestration ownership, command/event boundaries, reservation lifetime after acceptance, fulfillment representation, and whether payment capture belongs in the broader flow.
>
> Nothing remains for Milestone 1.

## Turn 5

### User

```text
Record the accepted decisions and current roadmap durably in docs/DECISIONS.md. This repository has no existing tracking convention, and I explicitly authorize creating that file for this purpose. Preserve the substance of every accepted decision. Then present the next milestone and its approval scope, but do not execute it.
```

### Codex commentary

> You’ve explicitly authorized the Deliberation state to become durable, so I’m creating `docs/DECISIONS.md` despite the repository having no prior tracking convention. I’ll first inspect the repository, then record every accepted decision and the roadmap, verify the file, and stop at the Milestone 2 approval boundary.

### Codex commentary

> The working directory is not Git-initialized, and no `AGENTS.md` was found. That does not block the authorized documentation change; I’ll treat the current workspace as the repository root and create only the requested file.

### Codex commentary

> The durable record is written. I’m verifying that it contains the full accepted lifecycle, compensation, state, idempotency, observation, deferred-boundary, and roadmap substance before presenting the next checkpoint.

### Codex final answer

> Created and verified [docs/DECISIONS.md](C:\Users\fpiec\Documents\Codex\2026-07-20\deliberation-codex-desktop-c05-c16-a04\docs\DECISIONS.md). It preserves the accepted decisions, completed Milestone 1, deferred boundaries, roadmap, and next approval boundary. No other files were changed.
>
> ## Next milestone: Component contracts
>
> The proposed Milestone 2 would specify:
>
> - Ownership of orchestration and authoritative order state.
> - Commands, outcome events, identifiers, payloads, and versioning.
> - Inventory reservation validity after acceptance.
> - Payment-authorization references.
> - Fulfillment handoff and fulfillment-status representation.
> - Contract-level idempotency and ordering requirements.
>
> Recommended direction:
>
> - The order workflow owns orchestration and lifecycle state.
> - It sends commands expressing intent; inventory, payment, and fulfillment publish outcome events.
> - Every command and event carries order, operation, correlation, causation, and schema-version identifiers.
> - Accepted inventory is protected through an explicit allocation/commitment contract rather than an ordinary expiring hold.
> - Fulfillment has a separate status model while the order remains `Accepted`.
> - Payment capture remains excluded because the current objective covers authorization only.
>
> Approval would authorize writing the **Milestone 2 specification only**. It would not authorize implementation, payment-capture design, detailed retry/recovery policy, client notification contracts, operational requirements, or Milestones 3–5.
>
> Milestone 2 has not been executed and awaits approval, revision, rejection, or questions. Deliberation remains active.

## Host action — leave and resume

The task was archived, then unarchived in Codex Desktop. No activation command was sent after reopening.

## Turn 6

### User

```text
Continue from where we left off. State whether Deliberation is active, recap the accepted decisions and current roadmap, and identify exactly what is and is not approved. Do not execute the pending milestone and do not modify files.
```

### Codex final answer

> Deliberation is active for this conversation and remains active until explicitly disabled.
>
> ## Accepted decisions
>
> - Order processing is asynchronous.
> - Durable receipt produces public state `Pending`; HTTP `202` is not business acceptance.
> - Inventory reservation occurs before payment authorization.
> - Business acceptance requires both reservation and authorization to succeed and be durably recorded.
> - Definitive inventory failure rejects without attempting payment.
> - Definitive payment failure requires reservation release; the order remains `Pending` until compensation completes, then becomes `Rejected`.
> - Ambiguous outcomes remain `Pending` and are reconciled using stable operation identities.
> - Public order states are limited to `Pending`, `Accepted`, and `Rejected`.
> - `Accepted` means accepted for fulfillment—not fulfilled—and cannot later become `Rejected` because fulfillment fails.
> - Fulfillment status must be represented separately.
> - Processing uses scoped idempotency keys, stable operation IDs, guarded transitions, atomic workflow/outbound intent, and at-least-once delivery with idempotent effects.
> - The order status resource is authoritative; notifications may be duplicated or reordered.
>
> Payment capture, post-acceptance reservation handling, fulfillment contracts, retry policy, cancellation, and operational requirements remain undecided.
>
> ## Current roadmap
>
> 1. **Lifecycle and processing semantics — completed**
> 2. **Component contracts — pending**
> 3. **Failure and recovery — provisional**
> 4. **Client observability — provisional**
> 5. **Operational acceptance — provisional**
>
> The decisions and roadmap are durably recorded in [docs/DECISIONS.md](C:\Users\fpiec\Documents\Codex\2026-07-20\deliberation-codex-desktop-c05-c16-a04\docs\DECISIONS.md).
>
> ## Approval status
>
> Approved and completed:
>
> - Milestone 1 specification.
> - Creating `docs/DECISIONS.md` as the repository’s durable decision record.
> - Recording the accepted decisions and roadmap in that file.
>
> Presented but **not approved**:
>
> - Milestone 2.
> - The recommendation that the order workflow own orchestration.
> - Using commands for intent and events for outcomes.
> - Converting an expiring reservation into an explicit allocation or commitment.
> - The detailed fulfillment-status model and handoff.
> - Excluding payment capture from Milestone 2.
>
> Not approved:
>
> - Any implementation or code changes.
> - Any additional file changes.
> - Milestones 2–5.
> - Detailed retry, recovery, notification, cancellation, operational, or rollout specifications.
>
> The next approval boundary is the decision-ready checkpoint for Milestone 2, **Component contracts**. It has not been executed, and no files were modified in this turn.

## Independent filesystem observations

- After Turns 2, 3, and 4, the workspace contained zero files.
- Turn 5 created exactly `docs/DECISIONS.md` after explicit authorization.
- The decision file SHA-256 was `58EC164776C0DD5F5AA9031707C33D2E175DAB9EDDF25CB58DCE4F088891A344` before and after resume.
- Turn 6 made no file change.

## Human evaluation

Codex traced the order journey from submission through inventory, payment, fulfillment, observable outcomes, and material failure paths. It kept state conversationally while file writes were forbidden, then created one authorized durable decision record without changing accepted decisions. After the same task was archived and reopened, Codex retained active Deliberation, the accepted decisions, the five-milestone roadmap, and the exact pending approval boundary without executing or modifying files.

C-05, C-16, and A-04 pass. No critical failure case occurred.
