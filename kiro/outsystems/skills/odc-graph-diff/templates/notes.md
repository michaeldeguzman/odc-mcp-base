# Graph diff: <app> revision <N> -> <M> (<spec>, <task>)

Recorded <date> after <publish name>. Read-only on the tenant: app_revisions, context_graph.

## Files

| File | What it is |
|---|---|
| N.xre | Baseline graph of revision N, saved before the publish |
| M.xre | Graph of revision M, saved after the publish |
| N-to-M.diff | Output of graphdiff.py |

## Revisions in between

<None, or the revisions published by someone else or auto-merged, and what they changed.>

## Summary check (before publish)

<Mentor's summary and pending changes, compared with the task prompt and the spec's scope for this task, before the publish was confirmed. "Matches", or each difference, with Mentor's claims attributed to Mentor. If something was clearly wrong or missing, what Mentor was asked to correct and what came back.>

## Result

<Copy the node and edge lines from the .diff.>

## In scope

<Each content change the task asked for, and whether its values match the spec.>

## Out of scope

<Each change the task did not ask for, or "None.">

## Summary vs graph diff

<"Matched element for element", or: each element the diff shows that Mentor's summary did not mention, and anything the summary claimed that the diff does not show. State only what the graph shows. Mark anything else as an inference.>

## Log check

<Only if the spec says Log check: yes. Two reads, side by side. Say only what the logs show, and mark any explanation as an inference.>

### Before use

<Window from <publish time> to <time>, <n> entries, grouped by the element that wrote them. Every error and warning in full. Which entries come from elements this publish changed. Say if nobody had used the changed screens in the window. Or "No entries", which is not proof the app works.>

### After use

<Window from <publish time> to <time>, and what use it covers (for example the browser checks: <n> searches, <n> page loads). Then the same as above: <n> entries, grouped by the element that wrote them, every error and warning in full, which entries come from elements this publish changed. Or "No entries", which is not proof the app works.>

## Decision

<Pending the user, or what the user decided.>
