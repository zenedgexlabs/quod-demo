# quod-demo

A small Python project (`tinyledger`, a double-entry bookkeeping library)
that shows [Quod](https://github.com/zenedgexlabs/quod) on GitHub Actions:
a pull request runs only the tests its change can affect, with a signed
certificate for every test it skips.

The suite has 59 tests and takes about 20 seconds on a laptop. Five "bulk"
tests do most of the work, one per module, so it matters which ones a change
needs.

## What to look at

Each pull request runs two jobs ([workflow](.github/workflows/tests.yml)):

| Job | What it runs |
|---|---|
| `pytest` | The whole suite, for comparison |
| `quod` | Only the tests the change obligates, then a signed Verdict |

Open a pull request's **Checks** tab, then the `quod` job's summary, for
the Verdict card. The `quod-verdict` artifact has the signed Verdict, the
plan (every test, run or skipped, with its reason) and the results.

- **[#1](https://github.com/zenedgexlabs/quod-demo/pull/1), a change to
  one function.** It changes the body of `read_csv` and adds a test. Quod
  runs the 4 tests that reach `read_csv`, plus the new one, and skips the
  other 55. The test files it skips entirely aren't even collected.
- **[#2](https://github.com/zenedgexlabs/quod-demo/pull/2), a bug.** It
  changes how `Money.allocate` rounds, and hands out cents that don't
  exist. Quod runs the 36 tests that reach `allocate`, 7 fail, and the
  Verdict blocks the merge. The slow tests of the other modules are
  skipped.

Neither pull request will be merged: they stay open as examples.

[Open pull requests](https://github.com/zenedgexlabs/quod-demo/pulls)

## How it's set up

Pushes to `main` record what every test depends on (functions, modules,
packages, environment). A pull request is compared with the map of its
merge base. That's the whole setup: one step in the workflow,

```yaml
      - uses: zenedgexlabs/quod-action@v0.1.0-alpha.4
        with:
          mode: ${{ github.event_name == 'push' && 'record' || 'enforce' }}
          test-command: python -m pytest -q
          python: python
          signing-key: ${{ secrets.QUOD_SIGNING_KEY }}
```

On your own project, start with `mode: shadow`: it still runs every test
and only reports what Quod would skip.

## Checking a Verdict yourself

Verdicts here are signed with the key
`ed25519:2135e1fbd5bdff9e06c89606fed863e012993f01e97faf826f6538f5da9b7f2c`.
Download a pull request's `quod-verdict` artifact and check it with
`quod-verify` from a [Quod release](https://github.com/zenedgexlabs/quod/releases):

```sh
quod-verify --verdict verdict.json --trusted-key ed25519:2135e1fbd5bdff9e06c89606fed863e012993f01e97faf826f6538f5da9b7f2c
```

Licensed under the Apache License 2.0.
