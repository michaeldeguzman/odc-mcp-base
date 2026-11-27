---
inclusion: always
---
# New project scaffold

When I start the first spec in a project root that has no `Prompts/` and no `Reports/` folder, propose this structure before writing any spec file. Create nothing until I confirm.

```
<Project>/
  .kiro/steering/project-<name>.md   this project's rules: app name, app key, scope
  .kiro/specs/                       Kiro's specs
  Prompts/                           numbered prompts sent to Mentor: 001-create-app.md, 002-...
  Reports/                           checks, interventions.md, build/ for the spec-driven-build skill's
                                     working files, and graphdiff/ if the graph diff is on
  README.md                          what the app is and which tenant stage it uses
```

- Show the tree with the real project and app names, then ask: "Create this structure? Yes / No / Change it".
- On yes, create the folders and fill the files from the templates in `SDD Base/templates/project/` (read them with your file tools). Replace `<App>`, `<Project>` and `<name>`. Leave the app key as `<pending>` until the app exists.
- Add `Reports/graphdiff/` only after the graph diff answer is yes, or change specs only for a change spec.
- On no, create nothing and don't ask again in this project.
- Never overwrite an existing file.
- Ask this before the graph diff question.

When writing `requirements.md`, follow `SDD Base/templates/requirements.md`. For a change spec, follow `SDD Base/templates/change-requirements.md`.
