from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .control_flow_obfuscator import ControlFlowObfuscator


def run_control_flow_obfuscation(
    sol_file: str | Path,
    ast_file: str | Path,
    *,
    output_sol: Optional[str | Path] = None,
) -> str:
    """
    Helper to run the control-flow obfuscator with file I/O handling.
    """

    sol_path = Path(sol_file)
    ast_path = Path(ast_file)
    output_path = Path(output_sol) if output_sol else sol_path.with_name(
        f"{sol_path.stem}_cfo{sol_path.suffix}"
    )

    with sol_path.open("r", encoding="utf-8") as sol_fp:
        sol_content = sol_fp.read()

    try:
        with ast_path.open("r", encoding="utf-8") as ast_fp:
            ast_data = json.load(ast_fp)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"警告: 无法解析AST文件 '{ast_path}': {exc}")
        ast_data = {}

    obfuscator = ControlFlowObfuscator(sol_content, ast_data)
    obfuscated_code = obfuscator.doObfuscate()

    with output_path.open("w", encoding="utf-8") as out_fp:
        out_fp.write(obfuscated_code)

    return str(output_path)

