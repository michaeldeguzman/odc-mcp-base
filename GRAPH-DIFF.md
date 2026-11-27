# Graph diff (opt-in)

SDD Base can check what Mentor changed after every publish. It saves the app's model graph before each publish, reads it again after, and compares the two by element. It reports anything the spec did not ask for.

It is opt-in. When Kiro creates `requirements.md` for a new spec, it asks:

> Do you want a graph diff after each publish?

Answer **Yes, every publish**, **Only for change specs** or **No**. Kiro records the answer in `requirements.md` under "Verification", and `design.md` and `tasks.md` follow it.

If you answer yes, Kiro asks one more question: whether to add a log check after each publish. Kiro records that answer on the next line, `Log check: yes | no`.

## Log check (optional)

The graph diff checks the model. It can't see what the app does when it runs. The log check reads the app's logs for about 30 minutes after each publish, groups the entries by the element that wrote them, and lists every error and warning. It says which entries come from elements the publish changed. No entries is not proof the app works: a timer that never runs writes nothing. Keep the browser checks.

The idea comes from a fellow ODC developer who pairs his graph diff with a 30-minute log window after each publish.

## Why

On ODC, the OutSystems MCP read tools return only the published revision. Before a publish, Mentor's change can be checked only from Mentor's own summary. The graph diff checks it after the publish, against the revision before. In the Employee Catalog builds, it caught Department record names that did not match their Labels, which the browser could not show.

## Cost

The graph is several MB, so it never goes into the chat. Kiro saves it to a file and a local script compares it. Each publish adds a few tool calls and a short report. That is why it is opt-in.

## What is in SDD Base

| File | What it does |
|---|---|
| `.kiro/steering/graph-diff.md` | Always loaded. Asks the question and makes the spec follow the answer |
| `kiro/outsystems/skills/odc-graph-diff/SKILL.md` | The method: baseline, publish, compare, report |
| `kiro/outsystems/skills/odc-graph-diff/scripts/graphdiff.py` | The comparison. Python 3.8+, standard library only, read-only |
| `kiro/outsystems/skills/odc-graph-diff/templates/notes.md` | The notes file for each publish |

## Setup

- **Multi-root workspace (recommended).** Add SDD Base as one root and your project as another. Kiro loads the steering rule from SDD Base for every project.
- **Power only.** If you only import the Power from GitHub, you get the skill but not the steering rule. The skill still asks the question when Kiro creates a spec. To make it reliable, copy `.kiro/steering/graph-diff.md` into your project's `.kiro/steering`.

## Limits

- It runs after the publish, so an unverified change reaches Development first.
- It shows which elements changed, not whether their values are right. Kiro still checks values against the spec.
- It checks the model, not the running app. The log check narrows that gap but doesn't close it. Keep the acceptance criteria and browser checks.
- Don't take the scope from Mentor's summary or pending-changes list. In testing, both were incomplete.
- It runs only when Kiro publishes. A publish from ODC Studio shows up at the next Kiro check.

The graph diff is not part of OutSystems' Power. It was added to this snapshot after the Employee Catalog builds, November 2026.
