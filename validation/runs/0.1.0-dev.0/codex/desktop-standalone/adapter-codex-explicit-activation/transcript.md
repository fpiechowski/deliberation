# Codex Desktop standalone activation transcript

- **Executed:** 2026-07-19
- **Product version:** `0.1.0-dev.0`
- **Host:** Codex desktop app for Windows, package `26.715.4045.0`
- **Surface:** standalone user skill
- **Fixture:** `adapter-codex-explicit-activation`
- **Thread:** `019f7c14-1b6b-7cb1-9585-a02254fa0bed`
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

### Codex final answer

> I’d approach the refactor in two phases, with no file changes during the first
> phase.
>
> 1. Map the current authentication flow: entry points, credential or token
> validation, session handling, middleware, persistence, configuration, and
> external identity providers.
> 2. Identify constraints and invariants: supported login methods, public API
> compatibility, security requirements, error behavior, and existing tests.
> 3. Diagnose design problems: mixed responsibilities, duplicated logic, hidden
> dependencies, inconsistent errors, unsafe token handling, and code that is
> difficult to test.
> 4. Propose a target structure with clear boundaries—for example, separating
> transport/controllers, authentication orchestration, credential or token
> verification, user storage, and framework adapters.
> 5. Plan small, behavior-preserving changes rather than a wholesale rewrite.
> Each step should remain testable and easy to review or revert.
> 6. Define verification before implementation: regression tests for successful
> login, invalid credentials, expiry, logout/revocation, authorization
> boundaries, and failure paths. I’d also check for common security regressions
> such as account enumeration, insecure comparisons, token leakage, weak cookie
> settings, and accidental logging of secrets.
> 7. Present the proposed structure and migration sequence for approval,
> including any compatibility or security tradeoffs.
>
> After that review, I’d implement the agreed changes incrementally and run the
> relevant tests and static checks after each meaningful step.

No activation acknowledgement appeared.

## Turn 2 — explicit activation fixture

### User

> $deliberation Help me refactor the authentication module.

### Codex commentary

> Deliberation mode is now active for this conversation. I’ll first inspect the
> repository and authentication flow without modifying anything; that evidence
> will inform a bounded first milestone and an explicit approval checkpoint
> before edits.

> The inspection found no project files in this task’s workspace—only empty
> `work` and `outputs` directories—so there is no authentication implementation
> or test suite to assess yet. I’m checking whether the delegated source task
> contains usable repository context before asking you to supply it.

### Codex final answer

> Deliberation mode is active.
>
> The workspace contains no authentication code or tests, so the first bounded
> milestone should be discovery only:
>
> - Make the authentication module available here or provide its
> repository/path.
> - Trace its public API, login/session/token flow, dependencies, and tests.
> - Identify security-sensitive invariants and concrete design problems.
> - Produce a behavior-preserving refactor proposal with boundaries, tradeoffs,
> and verification criteria.
>
> This milestone authorizes inspection and a refactor proposal only—no code
> changes. After reviewing the proposal, you can approve, revise, or reject the
> implementation milestone.

## Human evaluation

The ordinary request did not activate Deliberation. Explicit `$deliberation`
invocation was recognized, activation for the conversation was acknowledged,
and Codex established a bounded discovery milestone with an approval checkpoint
before edits.

The run does not fully pass C-01 because the activation acknowledgement did not
state that the mode remains active **until explicitly disabled**. No critical
failure case occurred.
