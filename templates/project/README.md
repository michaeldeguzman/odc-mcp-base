# <Project>

<One paragraph: what <App> does and who uses it.>

- ODC app: <App>
- Stage: Development
- Built with Kiro through the OutSystems MCP, using SDD Base.

## Where things are

- `.kiro/specs/`: requirements, design and tasks for each spec. Each change gets its own spec.
- `Prompts/`: every prompt sent to Mentor, numbered in the order sent.
- `Reports/`: checks against the acceptance criteria and `interventions.md`.
  - `Reports/build/`: the spec-driven-build skill's working files.
  - `Reports/screenshots/`: browser-check screenshots, in `<date>-<check>/` folders.
  - `Reports/graphdiff/`, if the graph diff is on: the saved graphs (`.xre`, ignored by `.gitignore` because they hold the signed-in user's email) and the notes for each publish.
