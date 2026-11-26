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

All skills except `outsystems` are Beta features. See [README.upstream.md](README.upstream.md) for OutSystems' notes on what each one needs, such as a shell with Python 3.8+ or the .NET 10 SDK.

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

Then start a project the way the [Employee Catalog builds](https://github.com/michaeldeguzman/employee-catalog-builds) did: write requirements as a Kiro spec, convert them to a spec for `outsystems-spec-driven-build`, confirm before every tenant write and publish, and verify each published revision against the requirements.

## Other harnesses

The repo still carries the setups for the other tools OutSystems supports: [`claude/`](claude) (Claude Code and Claude Desktop plugin), [`cursor/`](cursor), [`copilot/`](copilot), and a generic [`SKILL.md`](SKILL.md) for other assistants. They are unchanged from upstream and I only use the Kiro setup day to day. The install recipes for all of them are in [README.upstream.md](README.upstream.md).

## Repository layout

```
kiro/outsystems/       Kiro Power: plugin.json, icon, skills/
kiro/agents/           optional status-watcher agent
claude/  cursor/  copilot/   other harness packages
tests/                 upstream tests that keep the harness copies of the skill in sync
AGENTS.md              upstream contributor guidance for coding agents
README.upstream.md     original README with every install recipe and troubleshooting
```

## Keeping it current

This snapshot is one commit and doesn't track upstream. To refresh it, compare it with the latest `main` of [OutSystems/outsystems-mcp](https://github.com/OutSystems/outsystems-mcp), check `version` in [`kiro/outsystems/plugin.json`](kiro/outsystems/plugin.json) against upstream, and copy over the `kiro/` folder. OutSystems publishes no release notes, so the upstream commit history is where changes show up.

## License and attribution

The contents are from OutSystems and are MIT licensed. See [LICENSE](LICENSE), which carries OutSystems' copyright notice. OutSystems and ODC are trademarks of their owner. For product support and the privacy policy, follow the links in [README.upstream.md](README.upstream.md).
