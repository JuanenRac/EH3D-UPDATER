# =============================================================================
# EH3D-UPDATER - Optional commit-signature policy: signature.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Commit-signature policy: warn by default, require on request.

By default the updater trusts whatever the GitHub remote serves (a
compromised account or repository could push a commit that this tool would
then build and run). The policy decides what happens with a revision that
carries no valid GPG or SSH signature (`git verify-commit`):

* `warn` (the default): the install or update goes ahead, and the window and
  the command line state in the steps that the revision is not signed.
* `require`: the candidate revision - the fresh clone's HEAD, or the fetched
  FETCH_HEAD of an update - must carry a valid signature BEFORE its manifest
  is read or anything in it is built. A refused candidate leaves the
  installed checkout untouched.

Require signatures in `~/.eh3d_updater_settings.json`:

    {"signature_policy": "require",
     "require_signed_commits": true,
     "allowed_signers_file": "/home/me/.config/eh3d/allowed_signers"}

A value that is not recognised (`"required"`, `"on"`, a text instead of
`true`) is treated as `require` and the install warns about it.

A signature that git can verify is accepted only when its status is `G`
(good and trusted). A good signature by a key whose trust is unknown (status
`U`, for example a GPG key that is in the keyring but was never certified) is
refused unless `"signature_accept_unknown_trust": true` is set. To bind the
signature to the owner of the repository, `"signature_expected_fingerprint"`
(or `EH3D_UPDATER_EXPECTED_FINGERPRINT`) names the fingerprint of the signing
key (or of its primary key); a commit signed by any other key is refused.
Without it every trusted key of the keyring or of the allowed-signers file
is accepted.

or with the environment variable `EH3D_UPDATER_REQUIRE_SIGNED=1` (and
`EH3D_UPDATER_ALLOWED_SIGNERS=<file>`). `allowed_signers_file` is the
OpenSSH allowed-signers file used for SSH-signed commits; GPG-signed
commits are checked against the user's own GPG keyring.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .messages import coded
from .settings import load_settings


@dataclass(frozen=True)
class SignaturePolicy:
    required: bool = False
    allowed_signers_file: str | None = None
    #: "setting=value" of a policy value that is not recognised; the policy then fails closed (`required` is True) and the install says so
    invalid: str | None = None
    #: fingerprint the signing key must have (spaces and case ignored); None accepts any trusted key
    expected_fingerprint: str | None = None
    #: accept a good signature whose key trust is unknown (git status U)
    accept_unknown_trust: bool = False

    @property
    def mode(self) -> str:
        """"require" refuses an unsigned revision, "warn" (the default) installs it and says so."""
        return "require" if self.required else "warn"


_ENV_ON = {"1", "true", "yes"}
_ENV_OFF = {"0", "false", "no"}


def current_policy() -> SignaturePolicy:
    """The policy in force: the environment variables win over the saved
    settings, so a CI job or a one-off run can require signatures without
    touching the user's settings file.

    A value that is not recognised ("required", "on", a text where a boolean
    belongs...) never switches the protection off: the policy fails closed
    (signatures required) and `invalid` names the setting so the install warns."""
    settings = load_settings()
    invalid: str | None = None
    env_raw = os.environ.get("EH3D_UPDATER_REQUIRE_SIGNED", "")
    env_required = env_raw.strip().lower()
    if env_required in _ENV_ON:
        required = True
    elif env_required in _ENV_OFF:
        required = False
    elif env_required:
        required, invalid = True, f"EH3D_UPDATER_REQUIRE_SIGNED={env_raw.strip()!r}"
    else:
        required = False
        mode = settings.get("signature_policy")
        if mode is not None:
            if isinstance(mode, str) and mode.strip().lower() in ("require", "warn"):
                required = mode.strip().lower() == "require"
            else:
                required, invalid = True, f"signature_policy={mode!r}"
        flag = settings.get("require_signed_commits")
        if flag is True:
            required = True
        elif flag is not None and flag is not False:
            required, invalid = True, invalid or f"require_signed_commits={flag!r}"
    signers = os.environ.get("EH3D_UPDATER_ALLOWED_SIGNERS") or settings.get("allowed_signers_file")
    fingerprint = os.environ.get("EH3D_UPDATER_EXPECTED_FINGERPRINT") or settings.get("signature_expected_fingerprint")
    expected = _normalize_fingerprint(fingerprint) if isinstance(fingerprint, str) else ""
    return SignaturePolicy(
        required,
        signers if isinstance(signers, str) and signers else None,
        invalid,
        expected or None,
        settings.get("signature_accept_unknown_trust") is True,
    )


def _normalize_fingerprint(value: str) -> str:
    """A fingerprint without spaces and in lower case (git prints GPG ones in upper case, SSH ones as `SHA256:...`)."""
    return "".join(value.split()).lower()


def unsigned_reason(repo: Path, revision: str, policy: SignaturePolicy) -> str | None:
    """None when `revision` carries a signature that verifies, otherwise why it does not (not signed, signed by a key that is not trusted, or git could not check).
    It does not depend on the policy mode: the warning of the default mode and the refusal of the strict one are built from it."""
    cmd = ["git"]
    if policy.allowed_signers_file:
        if not Path(policy.allowed_signers_file).is_file():
            return f"allowed signers file {policy.allowed_signers_file} does not exist"
        cmd += ["-c", f"gpg.ssh.allowedSignersFile={policy.allowed_signers_file}"]
    cmd += ["verify-commit", revision]
    try:
        result = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"could not run git verify-commit: {exc}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        return "candidate commit is not signed by a trusted key" + (f" ({detail[-1]})" if detail else "")
    return _trust_problem(repo, revision, policy)


def _trust_problem(repo: Path, revision: str, policy: SignaturePolicy) -> str | None:
    """`git verify-commit` succeeds for any good GPG signature, even by a key nobody certified, and says nothing about who owns the key. Ask git for the trust status
    (`%G?`) and the fingerprints (`%GF` of the signing key, `%GP` of its primary key): only status G passes (U only when the settings allow it), and when the policy names
    a fingerprint the signing key must be that one."""
    cmd = ["git"]
    if policy.allowed_signers_file:
        cmd += ["-c", f"gpg.ssh.allowedSignersFile={policy.allowed_signers_file}"]
    cmd += ["log", "-1", "--format=%G?%n%GF%n%GP", revision]
    try:
        result = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"could not run git log: {exc}"
    if result.returncode != 0:
        return f"could not read the signature status: {(result.stderr or result.stdout).strip()}"
    lines = result.stdout.splitlines() + ["", "", ""]
    status, signing_key, primary_key = lines[0].strip(), lines[1].strip(), lines[2].strip()
    if status != "G" and not (status == "U" and policy.accept_unknown_trust):
        return coded("sig_trust_unknown" if status == "U" else "sig_not_good", status=status or "?")
    if policy.expected_fingerprint:
        found = {_normalize_fingerprint(value) for value in (signing_key, primary_key) if value}
        if _normalize_fingerprint(policy.expected_fingerprint) not in found:
            return coded("sig_fingerprint_mismatch", expected=policy.expected_fingerprint, found=signing_key or primary_key or "?")
    return None


def verify_revision(repo: Path, revision: str, policy: SignaturePolicy) -> str | None:
    """None when `revision` is acceptable under `policy`, otherwise the reason it is refused. Only the strict mode refuses; the default mode accepts everything (the caller
    asks `unsigned_reason` to warn)."""
    if not policy.required:
        return None
    return unsigned_reason(repo, revision, policy)
