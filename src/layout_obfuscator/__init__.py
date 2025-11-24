from __future__ import annotations

from pathlib import Path
from typing import Optional

from .layout_obfuscator import LayoutObfuscator


def run_layout_obfuscation(
    sol_file: str | Path,
    ast_file: str | Path,
    *,
    output_sol: Optional[str | Path] = None,
    replace_comments: bool = True,
    change_format: bool = True,
    replace_variables: bool = True,
    format_prob: float = 0.3,
    variable_prob: float = 0.8,
) -> str:
    """
    Helper to run layout/style obfuscation and persist the result.
    """

    sol_path = Path(sol_file)
    ast_path = Path(ast_file)
    output_path = Path(output_sol) if output_sol else None

    obfuscator = LayoutObfuscator(
        str(sol_path),
        str(ast_path),
        output_sol_path=str(output_path) if output_path else None,
    )

    return obfuscator.obfuscate(
        replace_comments=replace_comments,
        change_format=change_format,
        replace_variables=replace_variables,
        format_prob=format_prob,
        variable_prob=variable_prob,
    )

