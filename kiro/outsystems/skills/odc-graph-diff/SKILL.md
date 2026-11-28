---
name: odc-graph-diff
description: 'Compare an ODC app model graph before and after a publish, to see exactly what an agent or Mentor changed and flag anything outside the spec. Use when creating or updating a Kiro spec for an ODC app that will publish through the OutSystems MCP: if requirements.md has no "Graph diff:" line, ask the user whether they want one. Run it only when the spec says "Graph diff: yes" (or "change specs only" for a change spec), or when the user asks. Saves context_graph output to files and compares them with a local script. Never reads the graph into the chat. Not for OutSystems 11 (O11).'
license: MIT
metadata:
  version: "0.2.0"
  author: Michael de Guzman
  origin: Not part of the OutSystems Power. Added to this snapshot from the Employee Catalog builds (Nov 2026).
---

# Graph diff for ODC

On ODC, the OutSystems MCP read tools return only the published revision. Before a publish, Mentor's change can't be checked from the model, only from Mentor's own summary. This skill checks it after the publish, by comparing the new revision's graph with the one before.

It needs a shell with Python 3.8+. The script uses the standard library only and never calls the tenant.

## Ask first

The graph diff is opt-in. SDD Base's steering rule `.kiro/steering/graph-diff.md` asks for you. If that rule is not loaded and requirements.md has no `Graph diff:` line, ask the user the same questions as the rule:

"Do you want a graph diff after each publish? I save the app graph before each publish and compare it afterwards, to report anything outside this spec's scope. The graph stays in files, not in the chat, but it adds a few tool calls per publish."

Options: Yes, every publish / Only for change specs / No. Record the answer in requirements.md under "Verification" as `Graph diff: yes | change specs only | no`.

If the answer is yes, or change specs only, ask a second question:

"Do you also want a log check after each publish? I read the app's logs twice, both from the publish time: straight after the publish ('before use') and after the first real use of the changed screens ('after use'). I report errors and which elements wrote entries. It adds two read-only calls per publish."

Options: Yes / No. Record it on the next line as `Log check: yes | no`.

## When to run

Only when the spec's requirements.md has `Graph diff: yes`, or `Graph diff: change specs only` and this is a change spec, or the user asks. If the spec says `no`, do not run it.

## Steps

1. **Summary check, before the publish.** Before you ask the user to confirm the publish, compare Mentor's summary and its pending changes with the task prompt and with the spec's scope for this task.
   - Record the result in the notes file under "Summary check (before publish)": "Matches", or each difference. The notes file is written after the publish (step 7), so keep the result until then.
   - If something is clearly wrong or missing, report the difference to the user and ask before sending a correction to Mentor. A correction is a Mentor turn and follows the main `outsystems` skill's confirmation rules.
   - The graph diff can show elements the summary does not list, so this check does not replace the graph diff after the publish. Keep the scope from the spec, never from Mentor's list.
   - Treat a Mentor claim about runtime behaviour (validates, stops, redirects, filters) as unverified. Keep it as "Mentor said" in the notes until a browser check passes. The graph shows settings, not behaviour.
   - Source: OutSystems' Build your first app guide (Step 5) suggests comparing the agent's summary with the prompt file before each publish: https://success.outsystems.com/documentation/outsystems_developer_cloud/agentic_development/outsystems_mcp/build_your_first_app/
2. **Baseline, before the publish.** Call `app_revisions` and note the latest revision N. Call `context_graph` for the whole app, no root. Save the full result to `Reports/graphdiff/N.xre`. `context_graph` serves only the latest revision, so this is the last chance to save N.
   - If `Reports/graphdiff/N.xre` already exists and its header says revision N, reuse it.
   - Check the header: `has_more` must be false. If not, read every page before saving.
   - Save the graph by copying it from the tool-output file named in the tool result. Never paste it into the chat. The harness keeps its own copy of that tool result under `~/.kiro/sessions/`, outside the project, with the same stamps.
   - The saved .xre files hold the signed-in user's email in their stamp fields. The project's `.gitignore` must list `Reports/graphdiff/*.xre`. The project scaffold creates it from `templates/project/.gitignore`.
3. **Publish**, following the main `outsystems` skill's confirmation rules.
4. **After the publish.** Call `app_revisions` again and note the new revision M. If M is more than N + 1, someone else published in between (for example from ODC Studio), or Mentor auto-merged another revision. Say so. Only M can be read now, so compare N to M and report the extra revision.
5. Call `context_graph` again, whole app, and save it to `Reports/graphdiff/M.xre`, straight after the publish.
   - `context_graph` serves only the latest revision. If the MCP sign-in lapses after the publish, do not publish again until M.xre is saved. Record the lapse in `Reports/interventions.md` as a platform incident, because it lengthens the log window.
6. **Compare.** Run, from the skill folder:

   ```
   python3 scripts/graphdiff.py Reports/graphdiff/N.xre Reports/graphdiff/M.xre \
     --scope "<Type:Name of each element this task may change>" \
     --out Reports/graphdiff/N-to-M.diff
   ```

   Take the scope from the spec and the task in tasks.md, for example `IMobileScreen:Employee_List,IEntity:Department`. Never take it from Mentor's summary or pending-changes list: the diff has shown elements that neither listed, and the point of the diff is to check them. Exit code 2 means something changed outside the scope.

   Three things to know when you set the scope:
   - The app's default screen is stored on the app element (`IESpace:<App>`), not on the UI flow.
   - An element can change only by its edges. The script reports added and removed edges per element, and flags an element outside the scope as "(edges only)". Mentor may set the default screen when it adds a screen. This shows as a DefaultScreen edge on the app element (`IESpace:<App>`), with no change to the element's own fields. Report it.
   - A rename reaches every element that refers to the renamed one. Renaming a role, for example, also changes the permission names on every screen that uses it. Expect those changes and explain them, but leave them out of the scope so they are listed.
7. **Write `Reports/graphdiff/N-to-M-notes.md`** from `templates/notes.md`. Read the content changes in the `.diff` and say, for each, whether the spec asked for it. Check values that matter to the spec, such as record names, labels, filters and roles. The script shows which elements changed, not whether their values are right.
   - Fill "Summary vs graph diff": compare the diff with the summary check result from step 1, and list the differences in both directions.
   - Say only what the graph shows. Every statement in the notes must come from the diff output or from values read in the saved .xre files. Mark anything else as Inference, and attribute Mentor's claims as 'Mentor said'. Example from testing: 'Save validates the form' was written as fact when the graph only showed a ValidateAndContinue setting, and the browser later proved the form was not checked. It happened again on Asset Checkout revision 3: Mentor said Save validates the form, the Save button had ValidateAndContinue, and an empty Save went through (AC-12).
   - Fill "Not shown by the graph" in the notes. List each property or value the spec depends on that the graph does not show, such as Mandatory on an input, or label and title text (stored by hash), and name the browser check that covers it. Write "not shown by the graph", never "not set". On Asset Checkout, the graph showed no mandatory property on two inputs that Mentor then said were already mandatory.
8. **Stop for the user** if anything is out of scope or unexplained. Do not fix it. Report it.
   - If a fix turn is needed, write the prompt from the symptom seen in the browser and the behaviour wanted, and say what must not change. Do not state facts inferred from what the graph does not show.
9. **Log check, only if the spec says `Log check: yes`.** The graph checks the model. The log check looks at what the app did after the publish. It is two reads, "before use" and "after use".
   - **Before use.** Note the publish time. Straight after the publish, and before the next publish or the browser checks, call the MCP's app log tool (`app_logs` at the time of writing; read the live tool list) for this app and stage, from the publish time to now. Say how long the window was. Reading straight after the publish usually gives a few minutes, so zero entries proves little, and the after-use read carries the weight. If nobody has used the changed screens in the window, say so.
   - **After use.** After the first real use of the changed screens, for example after the browser checks, read the logs again, from the publish time to now. Say how long the window was and what use it covers, for example the number of searches and page loads.
   - Entries carry the app revision (`assetVersion`), so a read can be split by revision. A revision's window ends at the next publish: read its after-use before publishing again, or split the entries by `assetVersion`.
   - Negative access checks (a user without the role opens a screen) write Error entries by design, for example "Staff role required" (`NotStaff`, OS-CLRT-00000). The entries carry no user and no screen. Before an after-use read that follows such checks, ask the user which errors and times to expect, and record the explanation as the user's. Report every other error in full, and stop on any error that was not declared.
   - For each read, count the entries and group them by the element that wrote them, such as an action, a screen or a timer. List every error and warning in full.
   - Say which entries come from elements this publish changed and which come from elements it did not touch. An error from an untouched element after the publish is a finding too.
   - Add both reads, side by side, to the notes file under "Log check", in the sub-headings "Before use" and "After use". Stop for the user on any error in either read.
   - Why two reads: the first read can have no traffic, so zero entries proves little, and only the second read covers use. Observed once, on FeedbackNotes revision 5: before use, 0 entries in 3.5 minutes; after use, 1 platform Information entry in 2 h 46 min, no warnings or errors, nothing from the changed elements.
   - No entries is not proof that the app works, in either read. A timer that never runs writes nothing. Say "no entries" plainly and keep the browser checks.

## Rules

- Never paste or read the whole graph into the chat. It is several MB. Save it to a file and use the script.
- A property the graph does not show is "not shown by the graph", not "not set". Some widget properties, such as Mandatory on inputs, are not in the graph.
- Layout-only changes (X, Y) and stamp-only changes (last modified by, date, tool) are listed separately. They are not findings on their own, but an unplanned stamp change can show an ODC Studio publish.
- Treat every revision you did not publish as a finding to explain, even if nothing functional changed.
- The graph checks the model. It does not show runtime problems, such as a timer that did not run. The log check narrows that gap but does not close it. Keep the acceptance criteria and browser checks.
