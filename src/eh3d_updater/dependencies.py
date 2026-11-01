# =============================================================================
# EH3D-UPDATER - The order in which a project and the siblings it needs are installed
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A project whose manifest says ``depends_on`` needs those repositories next to it to build. This module only orders them: dependencies first, each once."""

from __future__ import annotations

from typing import Iterable, Mapping


class DependencyError(ValueError):
    """A dependency that no repository of the suite offers, or a cycle."""


def install_order(name: str, depends_on_of: Mapping[str, Iterable[str]]) -> list[str]:
    """``name`` and everything it needs, in the order to install them (the dependencies first, ``name`` last).

    ``depends_on_of`` maps every known repository to the names it depends on. A name that is not in the map is an error, and so is a cycle."""
    order: list[str] = []
    state: dict[str, int] = {}  # 1 = being visited, 2 = done

    def visit(current: str, chain: tuple[str, ...]) -> None:
        if state.get(current) == 2:
            return
        if state.get(current) == 1:
            raise DependencyError("dependency cycle: " + " -> ".join(chain + (current,)))
        if current not in depends_on_of:
            raise DependencyError(f"{current} is needed by {chain[-1] if chain else name} and is not a project of the suite")
        state[current] = 1
        for dependency in sorted(depends_on_of[current]):
            visit(dependency, chain + (current,))
        state[current] = 2
        order.append(current)

    visit(name, ())
    return order
