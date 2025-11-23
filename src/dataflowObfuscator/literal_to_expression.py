"""
字面量转表达式（Literal to Expression）模块
将整数、布尔值等字面量转换为等价的算术或逻辑表达式
"""
import re
import random
from .base import BaseObfuscator


class LiteralToExpressionObfuscator(BaseObfuscator):
    """
    字面量转表达式混淆器
    """
    
    def obfuscate(self, code):
        """
        将整数、布尔值等字面量转换为等价的算术或逻辑表达式
        :param code: Input code
        :return: Code with literals converted to expressions
        """
        # 处理整数字面量
        def replace_int_literal(match):
            # 检查是否在 pragma 行中
            line_start = match.string.rfind('\n', 0, match.start())
            line_end = match.string.find('\n', match.end())
            if line_start == -1:
                line_start = 0
            if line_end == -1:
                line_end = len(match.string)
            line = match.string[line_start:line_end]
            
            # 如果是在 pragma solidity 行中，不替换
            if 'pragma solidity' in line:
                return match.group(0)
            
            value = int(match.group(0))
            if value == 0:
                return '(1 - 1)'
            elif value == 1:
                return '(2 - 1)'
            elif value > 1:
                # 生成等价表达式
                ops = [
                    lambda v: f'({v-1} + 1)',
                    lambda v: f'({v+1} - 1)',
                    lambda v: f'({v*2} / 2)',
                    lambda v: f'({v//2} * 2 + {v%2})' if v > 2 else f'({v-1} + 1)',
                ]
                op = random.choice(ops)
                return op(value)
            return match.group(0)

        # 避免替换地址中的十六进制数字
        int_pattern = r'(?<!0x)\b\d+\b(?!\w)'
        code = re.sub(int_pattern, replace_int_literal, code)

        # 处理布尔字面量（如果还没有被处理）
        def replace_bool_literal(match):
            bool_val = match.group(0)
            if bool_val == 'true':
                expressions = ['(1 == 1)', '(2 > 1)', '(1 != 0)', '(1 >= 1)']
                return random.choice(expressions)
            else:
                expressions = ['(1 == 0)', '(2 < 1)', '(1 != 1)', '(1 <= 0)']
                return random.choice(expressions)

        bool_pattern = r'\b(true|false)\b'
        code = re.sub(bool_pattern, replace_bool_literal, code)

        return code

