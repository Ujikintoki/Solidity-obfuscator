from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import List, Optional, Tuple


def _parse_src(src: Optional[str]) -> Optional[Tuple[int, int, int]]:
    """
    解析 AST 节点的 src 描述 "offset:length:fileId"。
    返回 (offset, length, file_index)，失败返回 None。
    """
    if not src or not isinstance(src, str):
        return None

    parts = src.split(":")
    if len(parts) < 2:
        return None

    try:
        offset = int(parts[0])
        length = int(parts[1])
        file_idx = int(parts[2]) if len(parts) > 2 else 0
        return offset, length, file_idx
    except Exception:
        return None


def _collect_function_nodes(ast_root: dict) -> List[dict]:
    """
    遍历 AST 树，收集所有 FunctionDefinition 节点。
    """

    results: List[dict] = []

    def _walk(node):
        if isinstance(node, dict):
            if node.get("nodeType") == "FunctionDefinition":
                results.append(node)
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(ast_root)
    return results


def _find_insertion_offset(source: str, fn_node: dict) -> Optional[int]:
    """
    给定源码与 FunctionDefinition 节点，返回应插入死代码的偏移。
    插入在函数体 '{' 后。
    """

    body = fn_node.get("body")
    if not body:
        return None

    body_src = body.get("src")
    parsed_body = _parse_src(body_src)
    if parsed_body:
        start, length, _ = parsed_body
        open_idx = source.find("{", start, start + length)
        if open_idx != -1:
            return open_idx + 1

    return None


def _fallback_function_blocks(source: str) -> List[Tuple[int, int, int]]:
    """
    当缺少 AST 时，使用正则粗略查找函数体。
    返回 (header_start, body_start_after_brace, body_end_idx) 列表。
    """

    pattern = re.compile(
        r"\b(function|constructor|fallback|receive)\b[\s\S]*?\{", flags=re.MULTILINE
    )
    blocks: List[Tuple[int, int, int]] = []

    for match in pattern.finditer(source):
        header_start = match.start()
        body_open_idx = source.find("{", header_start)
        if body_open_idx == -1:
            continue

        depth = 0
        idx = body_open_idx
        body_end = None
        while idx < len(source):
            ch = source[idx]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    body_end = idx
                    break
            idx += 1

        if body_end is not None:
            blocks.append((header_start, body_open_idx + 1, body_end))

    return blocks


def _determine_indent(source: str, offset: int) -> str:
    """
    根据给定 offset 所在行推断缩进。
    """

    if offset <= 0:
        return "    "

    line_start = source.rfind("\n", 0, offset)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    prefix = source[line_start:offset]
    match = re.match(r"(\s*)", prefix)
    return match.group(1) if match else "    "


def _generate_dead_snippet(name_seed: int, indent: str) -> str:
    """
    生成仅依赖局部变量的安全死代码片段。
    """

    varname = f"__dead_{name_seed}"
    mode = name_seed % 3
    snippet = [f"{indent}uint256 {varname} = 0;\n"]

    if mode == 0:
        snippet.append(f"{indent}if (false) {{ {varname} = {varname} + 1; }}\n")
    elif mode == 1:
        snippet.append(
            f"{indent}for (uint256 __i_{name_seed} = 0; __i_{name_seed} < 0; __i_{name_seed}++) {{}}\n"
        )
    else:
        snippet.append(
            f"{indent}if (false) {{ uint256 __tmp_{name_seed} = {varname}; __tmp_{name_seed}++; }}\n"
        )

    return "".join(snippet)


def run_dead_code_insertion(
    sol_file: str | Path,
    ast_file: Optional[str | Path] = None,
    *,
    output_sol: Optional[str | Path] = None,
    insertion_prob: float = 0.6,
    max_per_function: int = 1,
    seed: Optional[int] = None,
    skip_constructors: bool = True,
    skip_fallback_receive: bool = True,
    skip_abstract_and_interface: bool = True,
) -> str:
    """
    AST 优先的死代码插入器，对 main.py 友好的 run_* 接口。
    """

    if seed is not None:
        random.seed(seed)

    sol_path = Path(sol_file)
    if not sol_path.exists():
        raise FileNotFoundError(f"Solidity 文件不存在: {sol_path}")

    source = sol_path.read_text(encoding="utf-8")

    ast_json: Optional[dict] = None
    ast_path: Optional[Path] = None
    if ast_file:
        ast_path = Path(ast_file)
        if ast_path.exists():
            try:
                ast_json = json.loads(ast_path.read_text(encoding="utf-8"))
            except Exception:
                ast_json = None

    insertion_offsets: List[int] = []

    if ast_json:
        ast_root = ast_json.get("ast") or ast_json.get("sources") or ast_json
        func_nodes = _collect_function_nodes(ast_root)

        for fn in func_nodes:
            body = fn.get("body")
            if not body and skip_abstract_and_interface:
                continue

            kind = fn.get("kind") or ""
            if skip_constructors and kind == "constructor":
                continue
            if skip_fallback_receive and kind in ("fallback", "receive"):
                continue

            offset = _find_insertion_offset(source, fn)
            if offset is not None and random.random() <= insertion_prob:
                insertion_offsets.append(offset)

    if not insertion_offsets:
        blocks = _fallback_function_blocks(source)
        for _, body_start, _ in blocks:
            if random.random() <= insertion_prob:
                insertion_offsets.append(body_start)

    if not insertion_offsets:
        out_path = Path(output_sol) if output_sol else sol_path.with_name(
            f"{sol_path.stem}_dead{sol_path.suffix}"
        )
        out_path.write_text(source, encoding="utf-8")
        return str(out_path)

    insertion_offsets = sorted(set(insertion_offsets), reverse=True)
    updated = source

    for offset in insertion_offsets:
        if offset < 0 or offset > len(updated):
            continue

        indent = _determine_indent(updated, offset)
        snippet_count = random.randint(1, max(1, max_per_function))

        snippets: List[str] = ["\n"]
        for idx in range(snippet_count):
            name_seed = abs(hash((offset, idx, random.randint(0, 1 << 16)))) % 1_000_000
            snippets.append(_generate_dead_snippet(name_seed, indent))

        updated = updated[:offset] + "".join(snippets) + updated[offset:]

    out_path = Path(output_sol) if output_sol else sol_path.with_name(
        f"{sol_path.stem}_dead{sol_path.suffix}"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(updated, encoding="utf-8")
    return str(out_path)


