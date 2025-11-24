from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from utils.parser import SolidityParser
from src.controlflow_obfuscator import run_control_flow_obfuscation
from src.layout_obfuscator import run_layout_obfuscation


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


def _handle_all(sol_path: Path, ast_path: Optional[Path], output: Optional[Path]) -> None:
    resolved_ast = _ensure_ast(sol_path, ast_path)

    temp_sol = sol_path.parent / "temp.sol"
    print(f"[ALL] 第一步: 控制流混淆 -> {temp_sol}")
    cf_output = run_control_flow_obfuscation(
        sol_file=str(sol_path),
        ast_file=str(resolved_ast),
        output_sol=str(temp_sol),
    )

    print(f"[ALL] 第二步: 解析中间文件 -> {cf_output}.ast")
    temp_parser = SolidityParser(cf_output)
    temp_ast_raw = temp_parser.parse_to_ast()
    if not temp_ast_raw:
        raise RuntimeError("中间AST生成失败，无法继续布局混淆。")
    temp_ast_path = Path(temp_ast_raw).resolve()

    final_output = output or sol_path.with_name(f"{sol_path.stem}_obfuscated_all{sol_path.suffix}")
    print(f"[ALL] 第三步: 布局混淆 -> {final_output}")
    result = run_layout_obfuscation(
        sol_file=cf_output,
        ast_file=str(temp_ast_path),
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
    action_group.add_argument("--all", action="store_true", help="按顺序执行控制流+布局混淆")

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
        elif args.all:
            _handle_all(sol_path, ast_path, output_path)
    except RuntimeError as exc:
        print(f"执行失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()

