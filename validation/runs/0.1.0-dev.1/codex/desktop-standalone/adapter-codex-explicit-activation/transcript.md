# Codex Desktop standalone activation transcript

- **Executed:** 2026-07-19
- **Product version:** `0.1.0-dev.1`
- **Host:** Codex desktop app for Windows, package `26.715.4045.0`
- **Surface:** standalone user skill
- **Fixture:** `adapter-codex-explicit-activation`
- **Thread:** `019f7c3e-62ed-7732-9474-8125b8ab8c25`
- **Workspace:** isolated projectless task

The installed artifact was copied from
`build/standalone/codex/deliberation` to the user skill scope. The temporary
installation and all projectless workspace contents were removed after evidence
capture. Codex Desktop retained a handle to the empty workspace root after the
task was archived, so that empty directory could not be removed during the run.

## Turn 1 — ordinary request without activation

### User

> Help me refactor an authentication module. Do not create or modify any files
> yet; first explain how you would approach it.

### Codex commentary

> I’ll first orient myself to the repository structure and locate the
> authentication code, using read-only inspection only. Then I’ll outline a
> concrete refactoring strategy, risks, and verification plan—without changing
> any files.

### Codex final answer

> I’d refactor it in two phases, starting with read-only discovery.
>
> 1. Trace the existing authentication flow: entry points, credential/token
> validation, sessions, middleware, persistence, external identity providers,
> configuration, and public APIs.
> 2. Establish invariants: supported login methods, compatibility requirements,
> security properties, error behavior, and existing test expectations.
> 3. Identify concrete problems such as mixed responsibilities, duplicated
> validation, hidden dependencies, inconsistent errors, unsafe token handling,
> secret logging, or poor testability.
> 4. Propose a target structure separating transport/controllers,
> authentication orchestration, credential or token verification, user/session
> storage, and framework-specific adapters.
> 5. Plan small, behavior-preserving changes instead of a wholesale rewrite.
> 6. Define verification for successful login, invalid credentials, expiry,
> logout/revocation, authorization boundaries, and failure paths. I’d also check
> account enumeration, timing leaks, cookie security, token exposure, and secret
> handling.
> 7. Present the proposed boundaries, migration sequence, and tradeoffs for
> approval before implementation.
>
> Once approved, I’d implement incrementally and run focused tests and static
> checks after each meaningful step. No files have been created or modified.

No activation acknowledgement appeared.

## Turn 2 — explicit activation fixture

### User

> $deliberation Help me refactor the authentication module.

### Codex commentary

> Deliberation is active for this conversation until you explicitly disable it.
> I’ll work through bounded milestones with decision-ready checkpoints before
> consequential changes.
>
> I’m using the explicitly invoked `deliberation` skill now. The first milestone
> is discovery only: inspect the available workspace and locate the
> authentication implementation and tests; I will not modify files.

### Codex final answer

> Deliberation is active for this conversation until you explicitly disable it.
> We’ll use bounded milestones and decision-ready checkpoints before material
> changes.
>
> The discovery milestone found that this workspace contains only empty `work`
> and `outputs` directories. There is no Git repository, authentication module,
> or test suite to inspect. No files were modified.
>
> Provisional roadmap:
>
> 1. Inspect the authentication flow, public contracts, dependencies, tests,
> and security invariants.
> 2. Present a behavior-preserving refactor proposal with boundaries, tradeoffs,
> and verification criteria.
> 3. At a checkpoint, approve, revise, or reject the proposed implementation
> slice.
> 4. Implement and verify only the approved slice.
>
> Please provide the repository or absolute path containing the authentication
> module. The next milestone authorizes inspection and a proposal only—not code
> changes.

## Human evaluation

The ordinary request did not activate Deliberation. Explicit `$deliberation`
invocation was recognized. Codex stated the conversation-wide lifetime through
explicit exit, committed to bounded milestones and decision-ready checkpoints,
gathered available context, and stopped before implementation.

C-01 and A-01 pass. No critical failure case occurred.
