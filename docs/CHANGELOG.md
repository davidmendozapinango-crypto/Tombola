# Changelog

All notable changes to this project will be documented in this file.

## Unreleased (2026-07-18)

- Migrate figure generation API from mask-based functions to row-major numbered
  generators. Each family module now exposes two functions:
  - `generate_principal(n, seed=None)`
  - `generate_complementary(n, seed=None)`
  These return an `n x n` integer NumPy array where filled cells contain a
  deterministic (seeded) random permutation of `1..k` and empty cells are `0`.

- Breaking change: public `mask_main` / `mask_complement` functions were
  removed from family modules. Short-term deprecation shims exist but callers
  should migrate to the new generators.

- Migration notes:
  - To obtain the structural mask from a generator use:

    ```py
    from src.core.figures.families import familia_a
    arr = familia_a.generate_principal(5, seed=42)
    mask = (arr > 0).astype(int)
    ```

  - A codemod is provided to automate migration of calls to the old mask API:
    `tools/migrate_masks.py`. It rewrites `.mask_main(...)` and
    `.mask_complement(...)` calls to derived masks from the new generators.

- Tests: unit tests were updated to validate both the structural masks for
  `n=5` and the permutation property (values `1..k` assigned to filled cells).
  The full test suite passes locally.

- Recommendation: run a formatter / linter (e.g. `black .`, `flake8`) and
  include the changelog entry in your release notes. Remove the temporary
  deprecation shims in a follow-up release once external callers have migrated.
