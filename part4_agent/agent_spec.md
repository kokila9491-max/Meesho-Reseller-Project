# Part 4 Monitoring Agent Specification

## Goal

Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.

## Tools

- `validate_feed` from Part 2 checks each monthly revenue feed before processing.
- `mom_growth` from Part 2 computes month-on-month percentage movement.
- `is_flagged` from Part 2 classifies movement as `flagged`, `not_flagged`, or `escalate_exact_boundary`.
- The Part 3 prompt-pack template fill drafts a Context -> Insight -> Implication message from supplied values only.

## Memory / State

Between runs, the agent must retain the previous month's validated revenue by category and the month associated with that feed. This state is required to compute the next run's month-on-month movement; the current implementation receives both feed paths explicitly so the state boundary is deterministic and repeatable.

## Planner

The ordered subtasks are defined in [Ordered Subtasks](#ordered-subtasks) and are executed by `mock_agent_runner.run`.

## Feedback Loop

Drafted messages are held for human approval. The runner records this state as `action_taken = "drafted_and_held_for_approval"`; it does not send email or call Gmail, SMTP, or any other external service.

## Guardrails

- **Input guardrail:** `validate_feed` must return `(True, [])` for the current and previous feeds before any revenue is loaded or MoM calculation runs.
- **Action guardrail:** no message is ever auto-sent; messages are only drafted and held for approval.
- **Output guardrail:** every number in a drafted message must trace back to a Part 1 or Part 2 value; invented figures are prohibited.

## Success and Error Stopping Conditions

Success means drafts are produced for flagged categories, or correctly zero drafts are produced when no category crosses the threshold, with every number traceable to Part 1 or Part 2. The run emits one structured JSON object.

Error means `validate_feed` returns `False`. The run is then a **Hard Stop**: validation errors are surfaced, no MoM computation is attempted, no messages are drafted, and `action_taken` is `"hard_stop"`.

## Given-When-Then Agent Specifications

### Ethnic Wear growth is flagged

**Given** April -> May Ethnic Wear revenue moves from `104520.77` to `185107.61`, **when** `mom_growth` then `is_flagged` run on it, **then** `mom_growth` returns `77.1` and `is_flagged` returns `"flagged"`.

### Beauty & Personal Care growth is not flagged

**Given** May -> June Beauty & Personal Care revenue moves from `35542.11` to `37559.07`, **when** evaluated, **then** `mom_growth` returns `5.67` and `is_flagged` returns `"not_flagged"`.

### Exact threshold is escalated

**Given** a synthetic pair `previous=100000`, `current=108000` chosen so the growth is exactly on the threshold boundary, **when** evaluated, **then** `mom_growth` returns exactly `8.0` and `is_flagged` returns `"escalate_exact_boundary"`, not `"flagged"` and not `"not_flagged"`.

### Corrupted feed hard-stops

**Given** the corrupted feed fixture, **when** `validate_feed` runs on it, **then** it returns `(False, errors)` where `errors` has exactly three entries matching, in order, the negative-revenue row, the missing-category row, and the missing-revenue row.

## Ordered Subtasks

1. Load the monthly revenue feed and run `validate_feed`.
2. If invalid, Hard Stop and report the validation errors.
3. If valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a Part 3 template message for at most the top three flagged categories by magnitude, preventing notification flooding.
7. Log any remaining flagged categories beyond the cap as `suppressed, review manually` without drafting a message.
7b. Log every `escalate_exact_boundary` category into `escalated_categories` without drafting a message; it must not be treated as either flagged or not flagged.
8. Emit one structured JSON object per run.

## Structured JSON Output

Every run emits exactly these top-level keys:

```text
run_month
validation_status
validation_errors
flagged_categories
suppressed_categories
escalated_categories
action_taken
```

`validation_status` is `"valid"` or `"invalid"`. Each drafted item in `flagged_categories` contains `category`, `mom_pct`, `previous_revenue`, `current_revenue`, `drafted`, and `message`. `suppressed_categories` contains category names beyond the draft cap. `escalated_categories` contains exact-boundary category names. `action_taken` is either `"drafted_and_held_for_approval"` or `"hard_stop"`.
