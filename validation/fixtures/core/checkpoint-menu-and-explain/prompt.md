# Harness setup

Before Turn 1, copy the fixture `seed/` files into `work/` in a fresh
isolated workspace. The seed contains the existing configuration module
`work/timeout_config.py` and its focused tests
`work/test_timeout_config.py`. Use Python's standard-library test runner with
`python -m unittest discover -s work -p "test_*.py"`; do not assume pytest or
any project configuration is installed. Do not add project instructions or
other source files.

# One conversation

## Turn 1

Activate Deliberation and prepare a checkpoint for adding a private
`normalize_timeout` helper to an existing Python configuration module. It should
normalize `None` to the default and reject negative values. Do not create or
modify files before approval.

Show a light milestone brief, an initial solution proposal, the key code and
test snippets I would be approving, alternatives only if material, the approval
boundary, and contextual suggestions under a localized heading meaning
"Suggested next step". Explicitly say I may choose a suggestion or reply in my
own words. Do not give the full Explain model or a journey unless I request an
explanation.

## Turn 2

Explain the current proposal. I want to understand it before deciding.

## Turn 3

I want something different: keep the helper private, but use a `ValueError`
whose message names the invalid value. Update the proposal and snippets; do not
edit.

## Turn 4

Explore alternatives. Show a materially different design and its tradeoffs. Do not
assume that asking for it is approval. Again show the suggested-next-step
heading and say I may reply in my own words.

## Turn 5

Accept the revised private-helper proposal, not the alternative. Implement
only that approved scope and run the proposed focused tests.
