<!--
Thanks for contributing to DSAG! Please read CONTRIBUTING.md first.
Keep PRs focused — ideally one topic (or one fix) per PR.
-->

## What does this PR do?

<!-- One or two sentences. Which topic / area does it touch? -->

## Type of change

- [ ] New topic (exercise)
- [ ] Fix to an existing solution / test
- [ ] Docs only (concise and/or deep)
- [ ] Tooling / infra (Makefile, harness, drill, bench, CI)
- [ ] Other:

## New-topic checklist

<!-- Delete this section if your PR doesn't add a topic. -->

- [ ] `stubs/<name>.py` — blank: signature + type hints + docstring (with
      complexity) + `raise NotImplementedError`
- [ ] `solutions/<name>.py` — correct, readable reference
- [ ] `tests/test_<name>.py` — imports via `harness.load`, covers edge cases
- [ ] `docs/<category>/<name>.md` — concise explainer
- [ ] `docs/<category>/<name>.deep.md` — in-depth companion, cross-linked
- [ ] Prefilled `src/topics/<category>/<name>.py` from the stub
- [ ] Registered in `README.md` topic table and `docs/progress.md`
- [ ] Any shared/given types added to `common/types.py`

## Verification

<!-- Paste the output or just confirm each. -->

- [ ] `make test-solutions` — all green
- [ ] `make test` on the blank stub fails with `NotImplementedError` (expected)
- [ ] `make lint` — clean

## Notes for the reviewer

<!-- Anything non-obvious: design choices, trade-offs, follow-ups. -->
