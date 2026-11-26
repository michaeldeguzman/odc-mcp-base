---
inclusion: always
---

Default rules for ODC projects built on SDD Base. Change them to suit your project, in your project's own steering if you'd rather not edit SDD Base.

- Target: OutSystems Developer Cloud (ODC). This is the default for everything below.
- OutSystems 11 (O11) is allowed only through an O11 MCP server running in Service Studio, and only when I ask for O11 work. Never switch to O11 or Service Studio on your own. Don't mix the two: ODC work uses the outsystems servers, O11 work uses the O11 server.
- Build Reactive Web apps and ODC agents only. The OutSystems MCP can't create or modify mobile apps, so don't plan or attempt mobile work.
- No custom code: no C#, and no External Logic libraries. Don't use the Power's outsystems-custom-code skill. All app logic is built in ODC Studio or by Mentor. The only code in this workspace is the Playwright tests in e2e/.
- Use only made-up sample data. No real people, real phone numbers or real addresses.
- Never put content from any confidential client brief or NDA-covered document into specs, prompts, Mentor, tests or the tenant. Ask me first if you're unsure whether something is confidential.
- Before writing any spec, check current capabilities with the outsystems-docs MCP (search_docs with source "odc"), and say how fresh the docs are using last_updated.
- To build from a written spec, use the Power's outsystems-spec-driven-build skill. Follow the main outsystems skill's rules: confirm before every tenant write, use one Mentor session per task, and poll long-running operations until they finish.
- Mentor builds the back-office web apps and the backend scaffold. Anonymous, safety-critical public screens are built by hand in ODC Studio, not by Mentor.
- Any REST endpoint exposed for testing is for the development stage only and must be protected with an API key.
