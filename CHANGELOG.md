# Changelog

All notable changes to this project are documented here.

## [0.0.1] - The updater of the EH3D ecosystem

- **Finds the EH3D repositories** through their `eh3d.project.json` manifests (ecosystem `EH3D`) on GitHub, with no token, and the local checkouts that sit next to each other in the workspace.
- **Installs and updates one project at a time, after a confirmation:** the replacement is cloned, merged without force and built and checked in a staging clone first; the live installation is only touched when that succeeds, and the previous one is kept as a backup that can be restored from the window.
- **Install all missing / Update all outdated** are separate, confirmed, sequential batch actions through the same safety path; nothing updates by itself.
- **An evidence log** of every attempt, checkable later for edited, removed or reordered lines, and an optional policy on signed commits.
- **A Qt Quick window in eight languages** (English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese) and a command line (`--cli`) that needs nothing but the standard library.
- 317 tests, run on Linux and Windows in CI, and a repository check of the manifest, the versions, the changelog and the eight README files.
