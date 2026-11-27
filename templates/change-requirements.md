# Requirements Document
## Introduction
This spec is a change to the existing app <App>. It <one sentence: what it adds or changes>.
`.kiro/specs/<main-spec>/requirements.md` stays the source of truth. This spec describes only what changes. Requirement and AC numbering continues from that document (it ends at Requirement <N> and AC-<NN>). AC-01 to AC-<NN> must still pass after this change.
## Glossary
Terms not listed here keep their meaning from the main requirements.
- **<New term>**: <Definition.>
- **<Existing term>** (changed): <What changes.>
## Requirements
### Requirement <N+1>: <Name>
**User Story:** As a <role>, I want <goal>, so that <reason>.
#### Acceptance Criteria
1. AC-<NN+1> (<short label>): Given <state>, When <action>, Then <observable result>.
   - Check by hand: <steps and expected values>.
## Verification
Graph diff: <yes | no> (the main spec's answer is the default)
Log check: <yes | no>
## Last task
Update `.kiro/specs/<main-spec>/requirements.md` with this change. If the app is built with outsystems-spec-driven-build, regenerate its `spec.md`. Keep this change spec as the record of what changed and why.
