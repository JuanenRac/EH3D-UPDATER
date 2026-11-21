# EH3D-UPDATER: requirements

This register is the single source of the state of each capability: `STATUS.md` and the README files cite it and never state a state that it does not. A state is one of `planned`, `prototype`, `implemented` and `validated`. `validated` means that a person has run the capability on a real machine and the evidence of the manifest says `bench` or `field`; nothing here is validated, because it has never installed or updated a project from the real GitHub: everything is tried with a fake GitHub and local repositories.

The register has 38 requirements: 34 implemented, 0 prototype, 4 planned and 0 validated. By progress: 34 done, 0 partial, 0 pending and 4 blocked. High coverage is not proof of correctness, so each row says how it is checked: the test that names it, and what it shows.

## How to read the register

* **ID:** `EUPD-NNN`, never reused and never renumbered; a new capability takes the next number.
* **State:** `implemented` is code that is complete and tested on a computer, `prototype` is part of the capability, `planned` is not written.
* **Progress:** `done`, `partial`, `pending` (can be written without hardware) or `blocked` (waits for hardware or for another program of the suite).
* **Evidence:** `simulator` when the test runs against a fake GitHub and local repositories, `host-test` when it checks a calculation, a reader or a screen-less piece, `none` when nothing is written yet.
* **Test:** the acceptance criterion: `file::name` is the test `name` of `tests/file.py`; a name with a slash, such as `tools/file::name`, is the path from the root without the extension. The test must exist. For a capability that is not written the cell says `planned:` and the name of the test that will show it; the day that test exists, the row must change.
* **Limits:** what is not done or not proven; a row that is `partial` or `blocked` always says it.

The check is `tests/test_requirements.py`: it reads this table, finds each test and fails when a state, a test or a count does not agree.

## Finding the projects

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EUPD-001 | A project is found by a valid manifest of its own repository, and a manifest of another project is rejected. | implemented | done | host-test | `test_github_fetch_errors::test_a_manifest_that_names_another_project_is_rejected` | Against a fake GitHub. |
| EUPD-002 | A malformed or missing manifest isolates that one repository and does not stop the scan. | implemented | done | host-test | `test_github_client::test_discover_remote_projects_isolates_one_malformed_manifest_from_the_rest` | - |
| EUPD-003 | Forks and archived repositories are not asked for a manifest. | implemented | done | host-test | `test_github_client::test_discover_remote_projects_does_not_ask_forks_or_archived_repositories_for_a_manifest` | - |
| EUPD-004 | The manifest accepts the fields of the schema and refuses a misspelled field. | implemented | done | host-test | `test_project_manifest::test_rejects_unknown_fields_to_prevent_silent_dashboard_drift` | - |
| EUPD-005 | The manifest of this repository and the manifests of the suite next to it are accepted. | implemented | done | host-test | `test_suite_manifests::test_every_manifest_of_the_suite_next_to_this_repository_is_accepted` | Skipped when no sibling checkout is next to the repository. |
| EUPD-006 | Kept backups and hidden staging folders are not taken for projects. | implemented | done | host-test | `test_workspace_safety::test_discovery_ignores_kept_backups_and_hidden_staging_folders` | - |

## Comparing with GitHub

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EUPD-007 | New commits at the same version are noticed, and unpushed local commits are ahead, not new. | implemented | done | host-test | `test_commits::test_unpushed_local_commits_are_ahead_not_new` | - |
| EUPD-008 | An unreachable remote or a plain folder is unknown, not outdated. | implemented | done | host-test | `test_commits::test_an_unreachable_remote_or_a_plain_folder_is_unknown` | - |
| EUPD-009 | A version has three or four numbers and the fourth counts. | implemented | done | host-test | `test_version_parse::test_ordering_follows_the_fourth_component` | - |
| EUPD-010 | The offline status never contacts the remote. | implemented | done | host-test | `test_commits::test_offline_status_never_contacts_the_remote` | - |
| EUPD-011 | A transient failure is retried, a definitive HTTP error never, and the reset time of a rate limit is named. | implemented | done | host-test | `test_github_client::test_urlopen_with_retries_never_retries_a_definitive_http_error` | Against a fake server. |
| EUPD-012 | An answer bigger than the limit is refused. | implemented | done | host-test | `test_limits_and_links::test_an_answer_bigger_than_the_limit_is_refused` | - |

## Installing and updating

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EUPD-013 | The build is verified in a staging clone before the promotion, and the previous installation is kept as a backup. | implemented | done | host-test | `test_install::test_update_verifies_build_in_staging_before_promoting_and_keeps_a_backup` | Against local repositories, not the real GitHub. |
| EUPD-014 | A build failure leaves the previous installation completely untouched. | implemented | done | host-test | `test_install::test_update_build_failure_leaves_the_previous_installation_completely_untouched` | - |
| EUPD-015 | A command that fails at any step never leaves a half-updated installation, and the next run finishes it. | implemented | done | host-test | `test_fault_campaign::test_a_command_that_fails_at_any_step_never_leaves_a_half_updated_installation` | A campaign with a fixed seed, not a continuous fuzzer. |
| EUPD-016 | An update is refused when a tracked file has an uncommitted edit, and a folder that is not a checkout is never touched. | implemented | done | host-test | `test_install::test_update_refuses_when_a_real_tracked_file_has_an_uncommitted_edit` | - |
| EUPD-017 | A remote manifest with a lower version than the installed one is refused. | implemented | done | host-test | `test_install::test_refuses_a_remote_manifest_version_lower_than_the_installed_version` | - |
| EUPD-018 | A failed health check puts the previous installation back. | implemented | done | host-test | `test_trust_origin_rollback::test_a_failed_health_check_puts_the_previous_installation_back` | - |
| EUPD-019 | A checkout whose origin is not the official repository is not updated. | implemented | done | host-test | `test_trust_origin_rollback::test_a_checkout_whose_origin_is_not_the_official_repository_is_not_updated` | - |
| EUPD-020 | The siblings that a manifest lists are installed first, once each, in order; a missing one or a cycle is an error. | implemented | done | host-test | `test_dependencies::test_a_missing_sibling_and_a_cycle_are_errors` | - |
| EUPD-021 | A command that runs past its limit is stopped with its children and the update is refused. | implemented | done | host-test | `test_run_limits::test_the_stopped_command_takes_its_children_with_it` | - |
| EUPD-022 | A workspace is held by one process at a time, and a busy one is a result, not a crash. | implemented | done | host-test | `test_workspace_safety::test_install_or_update_reports_a_busy_workspace_as_a_result` | - |
| EUPD-023 | The preview describes the candidate and changes nothing. | implemented | done | host-test | `test_backups::test_preview_describes_the_candidate_without_changing_the_checkout` | - |
| EUPD-024 | The backup is restored on request and the original is put back when the second rename fails. | implemented | done | host-test | `test_backups::test_restore_puts_the_original_back_when_the_second_rename_fails` | - |

## Trust, evidence and stations

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EUPD-025 | The policy on signed commits warns by default, and a required one refuses an unsigned revision. | implemented | done | host-test | `test_signature_warn::test_require_still_refuses_an_unsigned_revision` | Against a faked git; no real signing key has been used. |
| EUPD-026 | A signature by a key of unknown trust is refused unless the setting allows it. | implemented | done | host-test | `test_trust_origin_rollback::test_a_good_signature_by_a_key_of_unknown_trust_is_refused` | - |
| EUPD-027 | Each evidence line carries the hash of the one before, and an edited, removed or reordered line is found. | implemented | done | host-test | `test_station::test_an_edited_line_is_detected` | - |
| EUPD-028 | A damaged evidence line never stops the recording. | implemented | done | host-test | `test_evidence::test_a_damaged_last_line_never_stops_the_recording` | - |
| EUPD-029 | A station profile limits the projects, and an undefined profile is an error, not no restriction. | implemented | done | host-test | `test_station::test_an_undefined_profile_is_an_error_not_no_restriction` | - |
| EUPD-030 | The check command reports a newer version, sends a notification only when asked and changes nothing. | implemented | done | host-test | `test_station::test_check_lists_a_newer_version_and_changes_nothing` | The notification command is tested, not shown on a desktop. |

## Window and languages

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EUPD-031 | The window shows a failure and a checkpoint in its own language. | implemented | done | host-test | `test_qt_bridge::test_a_failure_is_shown_in_the_language_of_the_window` | Through the bridge of the window, without a screen. |
| EUPD-032 | A worker that fails does not leave the window busy. | implemented | done | host-test | `test_qt_bridge::test_a_refresh_whose_worker_fails_unexpectedly_does_not_leave_the_window_busy` | - |
| EUPD-033 | Every language has exactly the keys of English, and the Portuguese is that of Portugal. | implemented | done | host-test | `test_messages::test_portuguese_is_the_european_variant` | - |
| EUPD-034 | The picture of the window is asked for with checked options and written before the window opens. | implemented | done | host-test | `test_shot::test_the_output_is_checked_before_the_window_opens` | - |

## Not written yet

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EUPD-035 | A project is installed and updated end to end from the real GitHub. | planned | blocked | none | `planned:real_github::a_project_is_installed_and_updated_from_the_real_github` | Needs a published project and a person who accepts the confirmation. |
| EUPD-036 | The hand-over from ELECTRO-HOBBY-3D-UPDATER is run on a real checkout. | planned | blocked | none | `planned:handover::the_handover_runs_on_a_real_checkout` | Needs a real checkout and the other updater installed. |
| EUPD-037 | A real signing key is used to install a signed revision under the required policy. | planned | blocked | none | `planned:real_signature::a_signed_revision_is_installed_under_the_required_policy` | Needs a signed commit and an allowed-signers file. |
| EUPD-038 | The window is looked at on a screen on each system and matches its reference picture. | planned | blocked | none | `planned:window_screen::the_window_matches_the_reference_picture` | Needs a person at a screen on each system. |
