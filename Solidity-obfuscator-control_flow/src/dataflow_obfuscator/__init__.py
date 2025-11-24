from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .dataflow import dataflowObfuscation


def run_dataflow_obfuscation(
    sol_file: str | Path,
    ast_file: str | Path,
    *,
    output_sol: Optional[str | Path] = None,
) -> str:
    """
    Helper to run the data-flow obfuscator with file I/O handling.
    """

    sol_path = Path(sol_file)
    ast_path = Path(ast_file)
    
    # 如果没有指定输出路径，使用默认命名规则
    if output_sol:
        output_path = Path(output_sol)
    else:
        output_path = sol_path.with_name(f"{sol_path.stem}_dfo{sol_path.suffix}")

    # 创建临时的dataflowObfuscation实例来执行混淆
    # 由于dataflowObfuscation会自己生成输出文件名，我们需要稍作调整
    obfuscator = dataflowObfuscation(str(sol_path), str(ast_path))
    
    # 覆盖默认的输出文件名
    obfuscator.outputFileName = str(output_path)
    
    # 执行数据流混淆
    obfuscator.run()

    return str(output_path)

