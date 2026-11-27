# Graph diff (opt-in)

SDD Base can check what Mentor changed after every publish. It saves the app's model graph before each publish, reads it again after, and compares the two by element. It reports anything the spec did not ask for.

It is opt-in. When Kiro creates `requirements.md` for a new spec, it asks:

> Do you want a graph diff after each publish?

Answer **Yes, every publish**, **Only for change specs** or **No**. Kiro records the answer in `requirements.md` under "Verification", and `design.md` and `tasks.md` follow it.

If you answer yes, Kiro asks one more question: whether to add a log check after each publish. Kiro records that answer on the next line, `Log check: yes | no`.

## Log check (optional)

The graph diff checks the model. It can't see what the app does when it runs. The log check reads the app's logs after each publish, groups the entries by the element that wrote them, and lists every error and warning. It says which entries come from elements the publish changed. It reads twice: straight after the publish, aiming at about 30 minutes ("before use"), and again from the publish time to after the first real use of the changed screens ("after use"), and it reports both side by side. The first read can have no traffic, so zero entries proves little: on FeedbackNotes revision 5 it found 0 entries in 3.5 minutes, and the second found 1 platform Information entry in 2 h 46 min, with no warnings or errors and nothing from the changed elements. No entries is not proof the app works: a timer that never runs writes nothing. Keep the browser checks.

The log check is adapted from a fellow ODC developer's 30-minute log window after each publish.

## Why

On ODC, the OutSystems MCP read tools return only the published revision. Before a publish, Mentor's change can be checked only from Mentor's own summary. The graph diff checks it after the publish, against the revision before. In the Employee Catalog builds, it caught Department record names that did not match their Labels, which the browser could not show.

## Cost

The graph is several MB, so it never goes into the chat. Kiro saves it to a file and a local script compares it. Each publish adds a few tool calls and a short report. That is why it is opt-in.

## Order of a publish task

Each publish task runs in this order: summary check against the prompt and spec, save the baseline graph, publish, then the graph diff against the previous revision, followed by the log check steps if `Log check: yes`. The summary check compares Mentor's summary and pending changes with the task prompt and the spec's scope before the publish is confirmed (an idea from OutSystems' Build your first app guide), and the notes file's "Summary vs graph diff" section then lists what the diff shows that Mentor's summary did not mention, and what the summary claimed that the diff does not show. The graph diff can show elements the summary does not list, so the summary check does not replace the graph diff, and the scope still comes from the spec.

## What is in SDD Base

| File | What it does |
|---|---|
| `.kiro/steering/graph-diff.md` | Always loaded. Asks the question and makes the spec follow the answer |
| `kiro/outsystems/skills/odc-graph-diff/SKILL.md` | The method: summary check, baseline, publish, compare, report |
| `kiro/outsystems/skills/odc-graph-diff/scripts/graphdiff.py` | The comparison. Python 3.8+, standard library only, read-only |
| `kiro/outsystems/skills/odc-graph-diff/templates/notes.md` | The notes file for each publish. It states only what the graph shows: anything else is marked as an inference, and Mentor's claims are attributed to Mentor |

## Setup

- **Multi-root workspace (recommended).** Add SDD Base as one root and your project as another. Kiro loads the steering rule from SDD Base for every project.
- **Power only.** If you only import the Power from GitHub, you get the skill but not the steering rule. The skill still asks the question when Kiro creates a spec. To make it reliable, copy `.kiro/steering/graph-diff.md` into your project's `.kiro/steering`.

## Limits

- It runs after the publish, so an unverified change reaches Development first.
- It shows which elements changed, not whether their values are right. Kiro still checks values against the spec.
- It checks the model, not the running app. The log check narrows that gap but doesn't close it. Keep the acceptance criteria and browser checks.
- Don't take the scope from Mentor's summary or pending-changes list. In testing, the graph diff showed elements that neither listed.
- It runs only when Kiro publishes. A publish from ODC Studio shows up at the next Kiro check.

The graph diff is not part of OutSystems' Power. It was added to this snapshot after the Employee Catalog builds, November 2026.

## Tested

- Run on a build (FeedbackNotes, 27 Nov 2026): the project scaffold (Yes), the graph diff question (yes, and change specs only), baseline, publish, `graphdiff.py`, scope and notes across four graph diffs across five publishes (the first publish, the untouched template, was the baseline), and the log check with both reads (the second read done by hand, then written into the skill).
- Not yet run on a build: the summary check and the "Summary vs graph diff" notes section, the two log steps generated by the steering, the "No" answer, and the scaffold's "Change it" path.

## Next step, not yet tested

A cumulative graph diff before promoting to another stage: compare the revision to be promoted with the last revision released to that stage, so that everything that would reach the stage is checked together, not only the last publish. This has not been tested. In particular, reading the graph of another stage with `context_graph` has not been tested: on 27 Nov 2026 the `context_graph` schema showed the arguments key, root, graphviz and cursor, with no stage, and nothing here shows whether it can read a revision deployed in another stage. A deployment started from the ODC Portal would skip the check, because the check runs only when Kiro starts the deployment.
