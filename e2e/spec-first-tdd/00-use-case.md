# Project: [Your Project Name]

## Project Context

**Description**: Tests for an ODC Reactive Web app for a trauma-informed support service. There's no custom code: all app logic is built in ODC. Tests run against the published app in two ways: UI tests through the screens, and API tests against REST endpoints the app exposes in its development stage.

**Tech Stack**:
- Playwright with TypeScript, using @playwright/test for both UI tests and API tests (the request fixture).

**Configuration**:
- The base URL and any API key come from environment variables, never hard-coded or committed. A `.env.example` in `e2e/` lists placeholder names only, and a `.gitignore` in `e2e/` ignores `.env`.

**Test Data**:
- Made-up details and phrases only.

**Session Settings**:
- **Learning Mode**: OFF (toggle ON to add `# AI:` teaching comments to all code and tests)
- **Observability**: OFF (toggle ON to include telemetry contracts — traces, metrics, events — in BDD scenarios; requires `00-observability-conventions.md`)
- **Collaboration Mode**: Human-in-the-loop (default) or Autopilot

---

## Use Cases

### 1. [First Use Case Title]
**Description**: [Brief description of what this use case should accomplish. Example: User should be able to authenticate with email and password.]

<!-- AI adds all metadata below. Do not edit manually. -->
<!--
**Scenarios (GWT)**:
- Given [context], When [action], Then [expected outcome]
- Given [context], When [action], Then [expected outcome]

**Status**: Pending
**Priority**: [High / Medium / Low]
**Last Phase Completed**: None
**Current Phase**: None
**Test Coverage**: 0 tests
**Comprehension**: Gates passed: 0/3 | Last gap: None (Learning Mode only)
**Last Updated**: YYYY-MM-DD HH:MM
-->

---

## Tips

- **Keep use cases atomic**: Each use case should be small enough to fit in a single function or class
- **One at a time**: Process use cases sequentially, not in parallel
- **Spec-first**: Always start with the SPEC phase — decompose the use case into Given/When/Then scenarios and get them approved before writing any test
- **Observability-first**: If the project needs telemetry, set up observability infrastructure as the first use case before feature use cases include telemetry contracts
- **Human-in-the-loop**: Review and approve each phase before moving to the next
- **Abort / Skip**: Tell AI to "Skip to Refactor" or "Abandon this use case" at any point
