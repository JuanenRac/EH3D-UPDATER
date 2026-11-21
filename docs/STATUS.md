# EH3D-UPDATER: status

## Current state

EH3D-UPDATER works on a computer: the discovery, the comparison, the staging install, the backups and their restore, the evidence chain, the signature policy, the station profiles, the command line and the window are covered by tests with a fake GitHub and local repositories (no network). It has not been used for real work yet and has never installed or updated a project from the real GitHub.

## Capabilities

The official state of each capability is in `REQUIREMENTS.md`. The register has 38 requirements: 34 implemented, 0 prototype, 4 planned and 0 validated. By progress: 34 done, 0 partial, 0 pending and 4 blocked. This page never states a state that `REQUIREMENTS.md` does not.

## Open questions

* Whether signed commits become the default for the suite.
* Whether the evidence log should also be kept outside the workspace.

## What it needs from other repositories

* The manifests of the repositories of the suite, which this tool reads and never writes.
* A sibling checkout of the suite for the tests that read the real manifests; they are skipped when it is not next to this one.
* ELECTRO-HOBBY-3D-UPDATER, which hands the EH3D projects over to it; that hand-over has not been run on a real checkout.

## Known technical debt and omitted tests

* Nothing has been installed or updated from the real GitHub; the fake GitHub is the only server the tests talk to.
* Some tests need a sibling checkout of the suite and are skipped without it.
* The window is tested through its bridge and its texts; nobody has looked at it on a screen on every system.
