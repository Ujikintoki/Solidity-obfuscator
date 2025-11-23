import os
import string
import secrets
from typing import Optional, List

# Solidity 关键字列表（需避免作为标识符）
SOLIDITY_KEYWORDS = {
    "bool", "int", "uint", "address", "string", "bytes", "mapping", "struct", "enum",
    "function", "modifier", "event", "constructor", "fallback", "receive", "public",
    "private", "internal", "external", "view", "pure", "payable", "return", "returns",
    "if", "else", "for", "while", "do", "break", "continue", "require", "revert", "assert"
}

# 已生成的标识符缓存（用于去重）
_generated_identifiers = set()


def save_output(output_path: str, code: str) -> None:
    """将混淆后的代码写入输出文件"""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(code)
        print(f"File saved successfully: {output_path}")
    except Exception as e:
        raise IOError(f"Failed to save file at {output_path}: {e}")


def create_output_dir_if_not_exists(directory: str) -> None:
    """创建输出目录（若不存在）"""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Directory created: {directory}")
        except Exception as e:
            raise IOError(f"Failed to create directory {directory}: {e}")


def log_message(message: str, level: str = "INFO") -> None:
    """输出带级别的日志信息"""
    print(f"[{level}] {message}")


def generate_random_name(
    length: int = 0,
    min_length: int = 8,
    max_length: int = 16,
    allow_underscore: bool = False,
    prefix: str = "",
    suffix: str = ""
) -> str:
    """
    随机名称生成器（用于变量、函数重命名）
    :param length: 固定长度（0 则使用 min_length 和 max_length 范围）
    :param min_length: 最小长度（默认 8）
    :param max_length: 最大长度（默认 16）
    :param allow_underscore: 是否允许包含下划线（增加复杂度）
    :param prefix: 自定义前缀（可选）
    :param suffix: 自定义后缀（可选）
    :return: 符合 Solidity 规则的随机标识符
    """
    # 确定最终长度
    if length == 0:
        if min_length > max_length:
            raise ValueError("min_length must be <= max_length")
        length = secrets.randbelow(max_length - min_length + 1) + min_length
    
    # 定义字符集（首字符和后续字符分开处理）
    first_chars = string.ascii_lowercase + ("_" if allow_underscore else "")
    other_chars = string.ascii_letters + string.digits + ("_" if allow_underscore else "")
    
    # 生成随机部分
    random_part = []
    # 首字符：必须是小写字母或下划线（避免大写字母开头，符合常见命名习惯）
    random_part.append(secrets.choice(first_chars))
    # 后续字符：随机选择字符集
    for _ in range(length - 1):
        random_part.append(secrets.choice(other_chars))
    random_str = ''.join(random_part)
    
    # 拼接前缀和后缀
    full_str = f"{prefix}{random_str}{suffix}"
    
    # 校验是否为关键字或已生成过，若冲突则递归重试
    if full_str in SOLIDITY_KEYWORDS or full_str in _generated_identifiers:
        return generate_random_name(length, min_length, max_length, allow_underscore, prefix, suffix)
    
    # 加入缓存，避免重复
    _generated_identifiers.add(full_str)
    return full_str


def generate_random_identifier(
    length: int = 8,
    allow_uppercase: bool = True,
    allow_underscore: bool = False
) -> str:
    """
    随机标识符生成器
    :param length: 固定长度（默认 8）
    :param allow_uppercase: 是否允许大写字母
    :param allow_underscore: 是否允许下划线
    :return: 随机标识符
    """
    if length < 1:
        raise ValueError("Identifier length must be at least 1")
    
    # 定义字符集
    first_chars = string.ascii_lowercase + ("_" if allow_underscore else "")
    other_chars = string.digits
    if allow_uppercase:
        other_chars += string.ascii_uppercase
    other_chars += string.ascii_lowercase + ("_" if allow_underscore else "")
    
    # 生成标识符
    random_part = [secrets.choice(first_chars)]
    random_part.extend([secrets.choice(other_chars) for _ in range(length - 1)])
    identifier = ''.join(random_part)
    
    # 校验冲突
    if identifier in SOLIDITY_KEYWORDS or identifier in _generated_identifiers:
        return generate_random_identifier(length, allow_uppercase, allow_underscore)
    
    _generated_identifiers.add(identifier)
    return identifier


def clear_identifier_cache() -> None:
    """清空已生成的标识符缓存（用于批量生成新的标识符集合）"""
    global _generated_identifiers
    _generated_identifiers.clear()