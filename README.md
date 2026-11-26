# odc-mcp-base

SDD Base: a Kiro base for building [OutSystems Developer Cloud (ODC)](https://www.outsystems.com) apps through the OutSystems MCP server, with spec-driven development (SDD).

It is built on a snapshot of the Kiro Power from OutSystems' distribution repo, [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp), trimmed to Kiro only. It adds my steering files, an opt-in graph diff check and a few read-only references. This is not an official OutSystems repo and is not kept in sync automatically.

## What you get

The MCP server itself is hosted by OutSystems on your tenant at `https://<your-tenant>/mcp`. This repo holds the rules and helpers, not the server.

**The Kiro Power** at [`kiro/outsystems`](kiro/outsystems):

| Skill | What it does |
| --- | --- |
| `outsystems` | Main skill. Rules for using the MCP safely: confirm before changing tenant state, poll long operations until they finish, decide retries from the error category, prefer asset keys over names. Not for OutSystems 11 (O11). |
| `outsystems-spec-driven-build` | Builds a draft app through Mentor from a text spec, in two published parts: data model, then screens. |
| `outsystems-design-to-app` | Builds a draft app through Mentor from a Figma URL, screenshot, HTML mockup or front-end code. |
| `outsystems-app-architecture` | Interactive HTML graph of one app: screens, actions, entities, roles, dependencies, deployments. |
| `outsystems-tenant-architecture` | Interactive HTML graph of every asset in the tenant, with a traffic and error overlay and an AI governance view. |
| `outsystems-dependency-impact` | HTML explorer of who depends on a library, agent or connection. Read-only. |
| `outsystems-custom-code` | Build, test and deploy a C# External Logic library for ODC. The default `project.md` rules don't use it. |
| `odc-graph-diff` | **Added here, not from OutSystems.** Opt-in graph diff: saves the app model graph before each publish and compares it after, to report anything outside the spec. See [GRAPH-DIFF.md](GRAPH-DIFF.md). |

All OutSystems skills except `outsystems` are Beta features. See [OutSystems' README](https://github.com/OutSystems/outsystems-mcp#readme) for what each one needs, such as a shell with Python 3.8+ or the .NET 10 SDK.

**The SDD Base files:**

| File | Loads | What it does |
| --- | --- | --- |
| `.kiro/steering/workspace-layout.md` | Always | Keeps project files in the project root and SDD Base read-only |
| `.kiro/steering/project.md` | Always | Default rules for ODC work: Reactive Web only, no custom code, made-up data, confirm every tenant write. Change them to suit your project |
| `.kiro/steering/graph-diff.md` | Always | Asks whether you want a graph diff after each publish. See [GRAPH-DIFF.md](GRAPH-DIFF.md) |
| `.kiro/steering/outsystems-ui.md` | Manual (`#outsystems-ui`) | Points Kiro at the OutSystems UI references in `vendor/outsystems-ui/docs-ai/` |
| `.kiro/steering/sftdd.md` | Manual (`#sftdd`) | Spec-First TDD workflow, for Playwright tests in `e2e/` |
| `.kiro/agents/status-watcher.json` | Agent | Read-only agent on a cheaper model. It waits on long Mentor runs, publishes and deployments, so the main chat doesn't re-read its whole context on every poll |
| `e2e/` | | Place for Playwright tests, with `.env.example` and a `.gitignore` for `.env` |
| `vendor/` | | Read-only copies of OutSystems UI `docs-ai` and spec-first-tdd, with their licences |

## Setup

Use it as one root of a multi-root Kiro workspace, with your project as the other root.

1. **Clone it into a folder named exactly `SDD Base`.** The steering files read their references by that folder name, because Kiro does not resolve relative file links across workspace roots.
   ```
   git clone https://github.com/michaeldeguzman/odc-mcp-base.git "SDD Base"
   ```
2. **Install the Power.** In Kiro, open the Powers panel, choose **Add Custom Power**, then **Import power from GitHub**, and paste:
   ```
   https://github.com/michaeldeguzman/odc-mcp-base/tree/main/kiro/outsystems
   ```
3. **Point it at your tenant.** Ask Kiro Chat to finish setup, or add this to `~/.kiro/settings/mcp.json` under the top-level `mcpServers` (not under `powers.mcpServers`, which Kiro rewrites on every Power change):
   ```json
   {
     "mcpServers": {
       "outsystems": { "type": "http", "url": "https://<your-tenant>/mcp" }
     }
   }
   ```
   Use the bare hostname, such as `mycompany.outsystems.dev`, with no scheme or path.
4. **Sign in.** The OAuth sign-in opens in your browser on the first OutSystems tool call.
5. **Open the workspace.** Add `SDD Base` and your project folder to one Kiro workspace. The steering files and the status watcher load from SDD Base. Don't edit the status watcher's `tools` list or its `sleep`-only shell setting, since those keep it read-only.

Then start a project the way the [Employee Catalog builds](https://github.com/michaeldeguzman/employee-catalog-builds) did: write requirements as a Kiro spec, answer the graph diff question, convert the spec for `outsystems-spec-driven-build`, confirm before every tenant write and publish, and check each published revision against the requirements.

If you only want the Power in a single-root project, step 2 is enough. Copy `.kiro/steering/graph-diff.md` and `.kiro/agents/status-watcher.json` into your project's `.kiro` folder to get the graph diff question and the status watcher.

## Repository layout

```
kiro/outsystems/                         Kiro Power: plugin.json, icon, skills/
kiro/outsystems/skills/odc-graph-diff/   graph diff skill and script (added here)
.kiro/steering/                          SDD Base steering files
.kiro/agents/                            status-watcher agent
e2e/                                     place for Playwright tests
vendor/                                  read-only copies of OutSystems UI docs-ai and spec-first-tdd
GRAPH-DIFF.md                            how the graph diff works and how to set it up
```

## Keeping it current

To refresh the Power, compare `version` in [`kiro/outsystems/plugin.json`](kiro/outsystems/plugin.json) with the latest `main` of [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp). Then copy over upstream's `kiro/outsystems/` folder, and upstream's `kiro/agents/status-watcher.json` to `.kiro/agents/`. OutSystems publishes no release notes, so the upstream commit history is where changes show up.

Keep `kiro/outsystems/skills/odc-graph-diff/` when you copy. It is not in the upstream repo, so a copy that replaces the whole folder removes it.

## Sources

Where each part of this repo comes from. The copies are read-only here. Refresh them from their source, don't edit them in place.

| Part | Source | Licence |
| --- | --- | --- |
| `kiro/outsystems/` (except `odc-graph-diff`) and `.kiro/agents/status-watcher.json` | [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp), a snapshot, trimmed to Kiro only | MIT, OutSystems |
| `vendor/outsystems-ui/` (only `docs-ai/` and `LICENSE`) | [OutSystems/outsystems-ui](https://github.com/OutSystems/outsystems-ui), commit eafabd8 | BSD 3-Clause, OutSystems |
| `vendor/spec-first-tdd/` | [donnieprakoso/spec-first-tdd](https://github.com/donnieprakoso/spec-first-tdd), commit cf77f24 | MIT, Donnie Prakoso |
| `.kiro/steering/`, `kiro/outsystems/skills/odc-graph-diff/`, `GRAPH-DIFF.md`, `e2e/`, this README | Written by me | MIT |

Removed from the upstream snapshot: the Claude Code, Cursor and Copilot packages, the generic `SKILL.md`, OutSystems' tests and CI workflows, and their contributor files. If you use one of those tools, use [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp) directly.

## License and attribution

The OutSystems files are MIT licensed. See [LICENSE](LICENSE), which carries OutSystems' copyright notice. The files I added are also MIT. The copies in `vendor/` keep their own licences, listed under [Sources](#sources). OutSystems and ODC are trademarks of their owner. For product support and the privacy policy, follow the links in [OutSystems' README](https://github.com/OutSystems/outsystems-mcp#readme).
