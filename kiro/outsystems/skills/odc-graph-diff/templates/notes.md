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

## Result

<Copy the node and edge lines from the .diff.>

## In scope

<Each content change the task asked for, and whether its values match the spec.>

## Out of scope

<Each change the task did not ask for, or "None.">

## Decision

<Pending the user, or what the user decided.>
