---
inclusion: always
---
# Graph diff (opt-in)

Applies to any spec that publishes an ODC app through the OutSystems MCP.

## Ask once, when creating requirements.md

Before writing requirements.md for a new spec, ask the user:

"Do you want a graph diff after each publish? I save the app graph before each publish and compare it afterwards, to report anything outside this spec's scope. The graph stays in files, not in the chat, but it adds a few tool calls per publish."

Options: Yes, every publish / Only for change specs / No.

For a change spec, ask again and suggest the parent spec's answer.

Record the answer in requirements.md under a "Verification" heading, as one line:

Graph diff: yes | change specs only | no

If the answer is yes, or change specs only, ask a second question:

"Do you also want a log check after each publish? Before the next publish or the browser checks, I read the app's logs since the publish, about 30 minutes, and report errors and which elements wrote entries. It adds one read-only call per publish."

Options: Yes / No.

Record it on the next line:

Log check: yes | no

Do not ask again for the same spec unless the user changes it.

## If yes

- design.md gets a short "Graph diff" section that names the odc-graph-diff skill and the scope of each publish.
- tasks.md: every publish task starts with "Save the baseline graph" and ends with "Graph diff against the previous revision", with the scope of that publish. Stop for review if anything is out of scope.
- If `Log check: yes`, add "Log check since the publish" before the next publish or the browser checks, whichever comes first.
- Follow the odc-graph-diff skill. Never read the graph into the chat.

## If no

- No graph diff tasks.
- design.md states: "Mentor changes are verified by the acceptance criteria and browser checks only. Changes outside this spec's scope may not be detected."
