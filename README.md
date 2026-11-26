# odc-mcp-base

A personal base setup for building [OutSystems Developer Cloud (ODC)](https://www.outsystems.com) apps with an AI coding agent, mainly **Kiro**, through the OutSystems MCP server.

It is a snapshot of OutSystems' distribution repo, [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp). The OutSystems skills and the Kiro Power in it are the starting point for every new ODC project. This repo is not an official OutSystems repo and is not kept in sync automatically.

## What you get

The Kiro Power at [`kiro/outsystems`](kiro/outsystems) carries the skills the agent needs to work on ODC. The MCP server itself is hosted by OutSystems on your tenant at `https://<your-tenant>/mcp`, so this repo holds only the rules and helpers, not the server.

| Skill | What it does |
|---|---|
| `outsystems` | Main skill. Rules for using the MCP safely: confirm before changing tenant state, poll long operations until they finish, decide retries from the error category, prefer asset keys over names. Not for OutSystems 11 (O11). |
| `outsystems-spec-driven-build` | Builds a draft app through Mentor from a text spec, in two published parts: data model, then screens. |
| `outsystems-design-to-app` | Builds a draft app through Mentor from a Figma URL, screenshot, HTML mockup or front-end code. |
| `outsystems-app-architecture` | Interactive HTML graph of one app: screens, actions, entities, roles, dependencies, deployments. |
| `outsystems-tenant-architecture` | Interactive HTML graph of every asset in the tenant, with a traffic and error overlay and an AI governance view. |
| `outsystems-dependency-impact` | HTML explorer of who depends on a library, agent or connection. Read-only. |
| `outsystems-custom-code` | Build, test and deploy a C# External Logic library for ODC. |
| `odc-graph-diff` | **Added in this repo, not from OutSystems.** Opt-in graph diff: saves the app model graph before each publish and compares it after, to report anything outside the spec. See [GRAPH-DIFF.md](GRAPH-DIFF.md). |

All skills except `outsystems` are Beta features. See [OutSystems' README](https://github.com/OutSystems/outsystems-mcp#readme) for their notes on what each one needs, such as a shell with Python 3.8+ or the .NET 10 SDK.

[`kiro/agents/status-watcher.json`](kiro/agents/status-watcher.json) is an optional read-only agent on a cheaper model. It waits on long Mentor runs, publishes and deployments so the main conversation doesn't re-read its whole context on every poll.

## Using it as a Kiro base

1. **Install the Power.** In Kiro, open the Powers panel, choose **Add Custom Power**, then **Import power from GitHub**, and paste:
   ```
   https://github.com/michaeldeguzman/odc-mcp-base/tree/main/kiro/outsystems
   ```
2. **Point it at your tenant.** Ask Kiro Chat to finish setup, or add this yourself to `~/.kiro/settings/mcp.json` under the top-level `mcpServers` (not under `powers.mcpServers`, which Kiro rewrites on every Power change):
   ```json
   {
     "mcpServers": {
       "outsystems": { "type": "http", "url": "https://<your-tenant>/mcp" }
     }
   }
   ```
   Use the bare hostname, such as `mycompany.outsystems.dev`, with no scheme or path.
3. **Sign in.** The OAuth sign-in opens in your browser on the first OutSystems tool call.
4. **Optional: add the status watcher** to a workspace by copying [`kiro/agents/status-watcher.json`](kiro/agents/status-watcher.json) to `.kiro/agents/status-watcher.json` and starting a new chat. Don't edit its `tools` list or its `sleep`-only shell setting, since those keep it read-only.

**Optional: graph diff.** When Kiro creates `requirements.md` for a new spec, the steering rule [`.kiro/steering/graph-diff.md`](.kiro/steering/graph-diff.md) asks whether you want a graph diff after each publish. It is opt-in because it adds a few tool calls per publish. To get the question, use this repo as SDD Base (below), or copy that file into your project's `.kiro/steering`. Details in [GRAPH-DIFF.md](GRAPH-DIFF.md).

Then start a project the way the [Employee Catalog builds](https://github.com/michaeldeguzman/employee-catalog-builds) did: write requirements as a Kiro spec, convert them to a spec for `outsystems-spec-driven-build`, confirm before every tenant write and publish, and verify each published revision against the requirements.

## Using it as SDD Base

This repo is also SDD Base, my shared base for spec-driven development (SDD) with Kiro on ODC. Open it as one root of a multi-root Kiro workspace, with your project as the other root.

1. Clone it into a folder named exactly `SDD Base`. The steering files read their references by that folder name, because Kiro does not resolve relative file links across workspace roots.

   ```
   git clone https://github.com/michaeldeguzman/odc-mcp-base.git "SDD Base"
   ```

2. Install the Kiro Power as above, from this repo.
3. In Kiro, add `SDD Base` and your project folder to one workspace.

What SDD Base adds:

| File | Loads | What it does |
| --- | --- | --- |
| `.kiro/steering/workspace-layout.md` | Always | Keeps project files in the project root and SDD Base read-only |
| `.kiro/steering/project.md` | Always | Default rules for ODC work: Reactive Web only, no custom code, made-up data, confirm every tenant write. Change them to suit your project |
| `.kiro/steering/graph-diff.md` | Always | Asks whether you want a graph diff after each publish. See [GRAPH-DIFF.md](GRAPH-DIFF.md) |
| `.kiro/steering/outsystems-ui.md` | Manual (`#outsystems-ui`) | Points Kiro at the OutSystems UI references in `vendor/outsystems-ui/docs-ai/` |
| `.kiro/steering/sftdd.md` | Manual (`#sftdd`) | Spec-First TDD workflow for the Playwright tests in `e2e/` |
| `.kiro/steering/mentor-standards.md` | Manual (`#mentor-standards`) | Mentor BRD standards. Needs `vendor/mentor-brd/`, which is not included yet, see [Sources](#sources) |
| `.kiro/agents/status-watcher.json` | Agent | The read-only status watcher, already in place |
| `e2e/` | | Spec-First TDD guides and `.env.example` for Playwright tests |
| `vendor/` | | Read-only copies of OutSystems UI and spec-first-tdd, with their licences |

## Other harnesses

The repo still carries the setups for the other tools OutSystems supports: [`claude/`](claude) (Claude Code and Claude Desktop plugin), [`cursor/`](cursor), [`copilot/`](copilot), and a generic [`SKILL.md`](SKILL.md) for other assistants. They are unchanged from upstream and I only use the Kiro setup day to day. The install recipes for all of them are in [OutSystems' README](https://github.com/OutSystems/outsystems-mcp#readme).

## Repository layout

```
kiro/outsystems/       Kiro Power: plugin.json, icon, skills/
kiro/agents/           optional status-watcher agent
kiro/outsystems/skills/odc-graph-diff/   graph diff skill and script (added here, not from OutSystems)
.kiro/steering/        SDD Base steering files, including graph-diff.md
.kiro/agents/          status-watcher agent, installed for the SDD Base root
e2e/                   Spec-First TDD guides for Playwright tests
vendor/                read-only copies of OutSystems UI and spec-first-tdd
GRAPH-DIFF.md          how the graph diff works and how to set it up
claude/  cursor/  copilot/   other harness packages
tests/                 upstream tests that keep the harness copies of the skill in sync
AGENTS.md              upstream contributor guidance for coding agents
```

## Keeping it current

This snapshot is one commit and doesn't track upstream. To refresh it, compare it with the latest `main` of [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp), check `version` in [`kiro/outsystems/plugin.json`](kiro/outsystems/plugin.json) against upstream, and copy over the `kiro/` folder. OutSystems publishes no release notes, so the upstream commit history is where changes show up.

When you copy over the `kiro/` folder, keep `kiro/outsystems/skills/odc-graph-diff/`. It is not in the upstream repo, so a copy that replaces the whole folder removes it.

## Sources

Where each part of this repo comes from. The copies are read-only here. Refresh them from their source, don't edit them in place.

| Part | Source | Licence |
| --- | --- | --- |
| Kiro Power, skills and harness packages (`kiro/outsystems/`, `kiro/agents/`, `claude/`, `cursor/`, `copilot/`, `SKILL.md`, `tests/`, `.github/`) | [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp), a snapshot, not kept in sync | MIT, OutSystems |
| `vendor/outsystems-ui/` (only `docs-ai/` and `LICENSE`) | [OutSystems/outsystems-ui](https://github.com/OutSystems/outsystems-ui), commit eafabd8 | BSD 3-Clause, OutSystems |
| `vendor/spec-first-tdd/` and `e2e/spec-first-tdd/` | [donnieprakoso/spec-first-tdd](https://github.com/donnieprakoso/spec-first-tdd), commit cf77f24 | MIT, Donnie Prakoso |
| `.kiro/steering/`, `kiro/outsystems/skills/odc-graph-diff/`, `GRAPH-DIFF.md`, `e2e/.env.example`, this README | Written by me | MIT |

Not included: `vendor/mentor-brd/`, which `mentor-standards.md` expects. It comes from a community outsystems-docs skill whose source and licence I still need to confirm.

## License and attribution

The contents are from OutSystems and are MIT licensed, except the files I added: the graph diff (`kiro/outsystems/skills/odc-graph-diff/`, `GRAPH-DIFF.md`) and the SDD Base steering in `.kiro/steering/`, which I also release under MIT. The copies in `vendor/` and `e2e/spec-first-tdd/` keep their own licences, listed under [Sources](#sources). See [LICENSE](LICENSE), which carries OutSystems' copyright notice. OutSystems and ODC are trademarks of their owner. For product support and the privacy policy, follow the links in [OutSystems' README](https://github.com/OutSystems/outsystems-mcp#readme).
