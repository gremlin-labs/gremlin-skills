# Forward evaluation receipts

Each JSON receipt in this directory records one independently reviewable routing run from `forward-plan.json`. Every job runs in a fresh context with only a disposable fixture repository, the complete installed Gremlin skill payload, the host-native invocation named by the job, and the user-style prompt. The executing agent never receives the expected result.

Validate the queue and any accumulated receipts with:

```bash
python3 scripts/run_forward_evals.py --check-plan
```

Before invocation metadata is promoted, require the complete corpus:

```bash
python3 scripts/run_forward_evals.py --check-plan --require-complete
```

No receipt may claim `PASS` unless the fresh-context selection matches the hidden expected winner and respects the near-miss exclusions. Raw model output is retained only under ignored `dist/` storage; missing or timed-out runs remain explicit failures rather than synthetic successes.
