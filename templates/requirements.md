# Requirements Document
## Introduction
<One paragraph: what the app is, who uses it, its size, and that it is <App> on the ODC tenant, built by Kiro through the OutSystems MCP.>
## Glossary
- **<Term>**: <Definition. For an entity, list attributes with type and length, and any foreign key.>
- **<Role>**: <Role name and the access it has.>
- **<Screen>**: <What the screen shows.>
## Requirements
### Requirement 1: <Name>
**User Story:** As a <role>, I want <goal>, so that <reason>.
#### Acceptance Criteria
1. AC-01 (<short label>): Given <state>, When <action>, Then <observable result>.
   - Check by hand: <steps and expected values, using made-up sample data only>. Browser: <yes | no>.
## Verification
Graph diff: <yes | change specs only | no>
<!-- Include the Log check line only when Graph diff is yes or change specs only. Delete it when Graph diff is no. -->
Log check: <yes | no>
## Notes
- Sample data is made up. No real people, phone numbers or addresses.
- The browser-checks file covers exactly the ACs marked "Browser: yes".
<!-- For an AC such as "deployed to Development only": on a Personal Edition tenant, check it with env_list (one environment) and env_app. env_deploy_history does not show publishes made through the MCP, so do not use it as evidence. -->
- Mobile apps and custom code (C#, External Logic) are out of scope unless the project steering says otherwise.
