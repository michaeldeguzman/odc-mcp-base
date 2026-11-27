---
inclusion: always
---

- This project builds the ODC app <App>. App key: <pending>. Stage: Development.
- Only touch <App>. Never change any other app on the tenant.
- Save every prompt sent to Mentor as a numbered file in `Prompts/` (001-create-app.md, 002-..., in the order sent), with the exact text sent.
- Write checks and reports in `Reports/`. Log every fix after the first build, and any manual work in ODC Studio, in `Reports/interventions.md`.

## Browser checks

- Read a result only after loading has settled. An empty table and a table still loading can look the same.
- To test a user without a role, use a separate account and sign in with its own login. "Continue with OutSystems Community" reuses the account already signed in to outsystems.com.
- Do not write test users' emails or other personal details in reports.
- Save screenshots in `Reports/screenshots/<date>-<check>/`, numbered in the order taken.
