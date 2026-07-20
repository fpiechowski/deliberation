# Harness setup

Before the refactoring request, copy the fixture `seed/` files into `work/` in
a fresh isolated workspace. Do not add project instructions or other source
files.

# One conversation

## Turn 1

$deliberation Activate Deliberation for this conversation. Do not start an
engineering task yet.

## Turn 2

Refactor `work/profile_formatter.py` so input validation, normalization, and
rendering are separated and independently understandable. Preserve all
currently tested behavior.

The public function currently accepts a dictionary, but it may have external
callers. No decision has been made whether the refactor should replace that
public contract with a typed model or preserve it behind an internal model or
helpers.

Inspect the source and tests and run them if useful. Do not modify files.
Explain the material alternatives and consequences, recommend one bounded
refactoring-and-verification milestone, state its approval scope and completion
criteria, and wait for approval.

## Turn 3

Approve the recommended direction exactly as presented. Perform the bounded
refactor, run the full unit tests and a direct smoke check, then provide a
result walkthrough and completion status. Do not expand the public behavior or
add dependencies.

## Turn 4

For local readability only, rename the private test variable `record` to
`original_record` inside `test_input_is_not_mutated`. Make no production,
behavioral, or public-contract change. Apply the correction directly and rerun
the unit tests.
