from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from utils.parser import SolidityParser
from src.controlflow_obfuscator import run_control_flow_obfuscation
from src.layout_obfuscator import run_layout_obfuscation
from src.dataflow_obfuscator import run_dataflow_obfuscation
from src.dead_code_obfuscator import run_dead_code_obfuscation


def _derive_default_ast_path(sol_path: Path) -> Path:
    return sol_path.with_suffix(".ast")


def _ensure_ast(sol_path: Path, ast_path: Optional[Path] = None) -> Path:
    """
    Make sure an AST file exists; if not, invoke the parser.
    """
    target_ast = ast_path or _derive_default_ast_path(sol_path)
    if target_ast.exists():
        return target_ast

    print(f"未找到AST文件，自动调用parser生成: {target_ast}")
    parser = SolidityParser(str(sol_path))
    generated = parser.parse_to_ast()
    if not generated:
        raise RuntimeError("AST 生成失败，无法继续。")
    return Path(generated)


def _handle_parse(sol_path: Path) -> None:
    parser = SolidityParser(str(sol_path))
    ast_path = parser.parse_to_ast()
    if ast_path:
        print(f"解析完成: {ast_path}")
    else:
        sys.exit(1)


def _handle_layout(sol_path: Path, ast_path: Optional[Path], output: Optional[Path]) -> None:
    resolved_ast = _ensure_ast(sol_path, ast_path)
    result = run_layout_obfuscation(
        sol_file=str(sol_path),
        ast_file=str(resolved_ast),
        output_sol=str(output) if output else None,
    )
    print(f"布局混淆完成，输出文件: {result}")


def _handle_control_flow(sol_path: Path, ast_path: Optional[Path], output: Optional[Path]) -> None:
    resolved_ast = _ensure_ast(sol_path, ast_path)
    result = run_control_flow_obfuscation(
        sol_file=str(sol_path),
        ast_file=str(resolved_ast),
        output_sol=str(output) if output else None,
    )
    print(f"控制流混淆完成，输出文件: {result}")


def _handle_dataflow(sol_path: Path, ast_path: Optional[Path], output: Optional[Path]) -> None:
    resolved_ast = _ensure_ast(sol_path, ast_path)
    result = run_dataflow_obfuscation(
        sol_file=str(sol_path),
        ast_file=str(resolved_ast),
        output_sol=str(output) if output else None,
    )
    print(f"数据流混淆完成，输出文件: {result}")


def _handle_deadcode(sol_path: Path, ast_path: Optional[Path], output: Optional[Path]) -> None:
    resolved_ast = _ensure_ast(sol_path, ast_path)
    result = run_dead_code_obfuscation(
        sol_file=str(sol_path),
        ast_file=str(resolved_ast),
        output_sol=str(output) if output else None,
    )
    print(f"死代码混淆完成，输出文件: {result}")
    
    # 生成对应的 AST 文件
    parser = SolidityParser(result)
    ast_result = parser.parse_to_ast()
    if ast_result:
        print(f"AST 生成: {ast_result}")
    else:
        print("AST 生成失败")


def _handle_all(sol_path: Path, ast_path: Optional[Path], output: Optional[Path]) -> None:
    resolved_ast = _ensure_ast(sol_path, ast_path)

    # 第一步：数据流混淆
    temp_sol_1 = sol_path.parent / "temp_dataflow.sol"
    print(f"[ALL] 第一步: 数据流混淆 -> {temp_sol_1}")
    df_output = run_dataflow_obfuscation(
        sol_file=str(sol_path),
        ast_file=str(resolved_ast),
        output_sol=str(temp_sol_1),
    )

    # 第二步：解析数据流混淆后的文件
    print(f"[ALL] 第二步: 解析中间文件 -> {df_output}.ast")
    temp_parser_1 = SolidityParser(df_output)
    temp_ast_1_raw = temp_parser_1.parse_to_ast()
    if not temp_ast_1_raw:
        raise RuntimeError("数据流混淆后AST生成失败。")
    temp_ast_1_path = Path(temp_ast_1_raw).resolve()

    # 第三步：控制流混淆
    temp_sol_2 = sol_path.parent / "temp_controlflow.sol"
    print(f"[ALL] 第三步: 控制流混淆 -> {temp_sol_2}")
    cf_output = run_control_flow_obfuscation(
        sol_file=df_output,
        ast_file=str(temp_ast_1_path),
        output_sol=str(temp_sol_2),
    )

    # 第四步：解析控制流混淆后的文件
    print(f"[ALL] 第四步: 解析中间文件 -> {cf_output}.ast")
    temp_parser_2 = SolidityParser(cf_output)
    temp_ast_2_raw = temp_parser_2.parse_to_ast()
    if not temp_ast_2_raw:
        raise RuntimeError("控制流混淆后AST生成失败。")
    temp_ast_2_path = Path(temp_ast_2_raw).resolve()

    # 第五步：死代码插入
    temp_sol_3 = sol_path.parent / "temp_deadcode.sol"
    print(f"[ALL] 第五步: 死代码插入 -> {temp_sol_3}")
    dc_output = run_dead_code_obfuscation(
        sol_file=cf_output,
        ast_file=str(temp_ast_2_path),
        output_sol=str(temp_sol_3),
    )

    # 第六步：解析死代码插入后的文件
    print(f"[ALL] 第六步: 解析中间文件 -> {dc_output}.ast")
    temp_parser_3 = SolidityParser(dc_output)
    temp_ast_3_raw = temp_parser_3.parse_to_ast()
    if not temp_ast_3_raw:
        raise RuntimeError("死代码插入后AST生成失败。")
    temp_ast_3_path = Path(temp_ast_3_raw).resolve()

    # 第七步：布局混淆
    final_output = output or sol_path.with_name(f"{sol_path.stem}_obfuscated_all{sol_path.suffix}")
    print(f"[ALL] 第七步: 布局混淆 -> {final_output}")
    result = run_layout_obfuscation(
        sol_file=dc_output,
        ast_file=str(temp_ast_3_path),
        output_sol=str(final_output),
    )

    print(f"[ALL] 完成，最终输出: {result}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solidity 智能合约混淆器统一入口",
    )
    parser.add_argument("solidity_file", help="待处理的 .sol 文件路径")
    parser.add_argument("--ast", help="指定已有 AST 文件路径，可选", default=None)
    parser.add_argument(
        "--output",
        help="指定输出文件路径，可选，不指定则使用默认命名规则",
        default=None,
    )

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--parse", action="store_true", help="仅解析 AST")
    action_group.add_argument("--layout", action="store_true", help="仅执行布局混淆")
    action_group.add_argument("--controlflow", action="store_true", help="仅执行控制流混淆")
    action_group.add_argument("--dataflow", action="store_true", help="仅执行数据流混淆")
    action_group.add_argument("--deadcode", action="store_true", help="仅执行死代码混淆")
    action_group.add_argument("--all", action="store_true", help="按顺序执行数据流+控制流+死代码+布局混淆")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sol_path = Path(args.solidity_file).resolve()
    if not sol_path.exists():
        print(f"错误: 找不到 Solidity 文件 {sol_path}")
        sys.exit(1)

    ast_path = Path(args.ast).resolve() if args.ast else None
    output_path = Path(args.output).resolve() if args.output else None

    try:
        if args.parse:
            _handle_parse(sol_path)
        elif args.layout:
            _handle_layout(sol_path, ast_path, output_path)
        elif args.controlflow:
            _handle_control_flow(sol_path, ast_path, output_path)
        elif args.dataflow:
            _handle_dataflow(sol_path, ast_path, output_path)
        elif args.deadcode:
            _handle_deadcode(sol_path, ast_path, output_path)
        elif args.all:
            _handle_all(sol_path, ast_path, output_path)
    except RuntimeError as exc:
        print(f"执行失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()

