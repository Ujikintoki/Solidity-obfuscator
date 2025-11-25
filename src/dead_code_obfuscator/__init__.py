from __future__ import annotations

from pathlib import Path
from typing import Optional

from .dead_code_obfuscator import run_dead_code_insertion

__all__ = [
    "run_dead_code_obfuscation",
    "run_dead_code_insertion",
]


def run_dead_code_obfuscation(
    sol_file: str | Path,
    ast_file: Optional[str | Path] = None,
    *,
    output_sol: Optional[str | Path] = None,
    insertion_prob: float = 1,
    max_per_function: int = 1,
    seed: Optional[int] = None,
    skip_constructors: bool = True,
    skip_fallback_receive: bool = True,
    skip_abstract_and_interface: bool = True,
) -> str:
    """
    对外统一入口，参数与 run_dead_code_insertion 完全一致。
    """

    return run_dead_code_insertion(
        sol_file=sol_file,
        ast_file=ast_file,
        output_sol=output_sol,
        insertion_prob=insertion_prob,
        max_per_function=max_per_function,
        seed=seed,
        skip_constructors=skip_constructors,
        skip_fallback_receive=skip_fallback_receive,
        skip_abstract_and_interface=skip_abstract_and_interface,
    )


