# EH3D-UPDATER: scope

Status: **host-test**. EH3D-UPDATER is a command line and a window that find the repositories of the EH3D ecosystem through their manifests, compare each local checkout with GitHub and install or update one project at a time after a confirmation. It is tried on a computer with a fake GitHub and local repositories; it has not installed or updated a project from the real GitHub. This page says what it is for, what it will not do and where it sits among the other programs of the suite.

## Purpose

The way to get the suite and keep it current on the computers of the people who develop it: it lists the projects, says which are installed, up to date, outdated or have new commits, and replaces one project at a time through a staging clone, keeping the previous installation as a backup that can be restored.

## What it does

* Finds the projects by their manifests: a public repository is a project only when its root `eh3d.project.json` validates and declares the ecosystem; a folder name alone is never enough.
* Compares the version of each local checkout with the one on GitHub and notices new commits at the same version.
* Installs and updates one project at a time after a confirmation: the update is cloned, merged without force, built and checked in a staging clone before the live installation is touched, and the previous installation is kept.
* Installs the sibling repositories that a manifest lists first, in dependency order, and stops with an error on a missing sibling or a cycle.
* Keeps an evidence log whose lines are chained, so that an edited, removed or reordered line is found, and applies an optional policy on signed commits.
* Follows a station profile that lists the projects a machine works with, and shows the same in a window in eight languages and in a command line that needs only the standard library.

## What it will not do

* No update in the background and no unconfirmed batch: a batch is a sequence of single updates through the same safety path.
* No update of the CM5 of the workshop: that one is updated by releases, with the deploy script of the server.
* No signature required by default: the policy is a switch and its default only warns.
* No change of the ecosystem it does not belong to: a manifest that declares another ecosystem is not a project here.

## Where it sits

* **It reads:** the manifests of the local checkouts, the public repositories and manifests of the owner on GitHub, its settings file and the evidence log.
* **It writes:** the checkouts it installs or updates, the backups it keeps, the evidence log, the settings file and the log of each command.
* **It is read by:** the person who runs it, and ELECTRO-HOBBY-3D-UPDATER, which hands the EH3D projects over to it.
* **It depends on:** `git` on the computer, the standard library for the command line and `PySide6` for the window only.

## What it never decides

Whether the code of a project is safe to run. The build script of an installed project runs with the rights of the person, so a project that was installed is not a project that was checked; the confirmation and the policy on signatures help the person to decide, and they do not decide for them.

The requirements of the program, with the state of each and the test that shows it, are in `REQUIREMENTS.md`; the state in a paragraph is in `STATUS.md`.
