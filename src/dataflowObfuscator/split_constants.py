"""
常量拆分（Split Constants）模块
将较大的整数常量拆分为多个小整数的算术组合
"""
import re
import random
from .base import BaseObfuscator


class SplitConstantsObfuscator(BaseObfuscator):
    """
    常量拆分混淆器
    """
    
    def obfuscate(self, code):
        """
        将较大的整数常量拆分为多个小整数的算术组合
        :param code: Input code
        :return: Code with constants split into expressions
        """
        def replace_constant(match):
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
            
            value_str = match.group(0)
            try:
                value = int(value_str)
            except ValueError:
                return value_str

            # 避免处理太小的值或已经在表达式中的值
            if value <= 10:
                return value_str

            # 随机选择拆分方式
            split_method = random.choice(['add', 'multiply', 'subtract', 'divide'])

            if split_method == 'add':
                # 加法拆分: 100 -> 50 + 50
                part1 = random.randint(1, value - 1)
                part2 = value - part1
                return f"({part1} + {part2})"
            elif split_method == 'multiply':
                # 乘法拆分: 100 -> 10 * 10 (需要是平方数或可分解)
                if value > 1:
                    # 尝试找到因子
                    factors = []
                    temp = value
                    for _ in range(2):
                        if temp > 1:
                            # 找到一个小因子
                            factor = 2
                            while factor * factor <= temp:
                                if temp % factor == 0:
                                    factors.append(str(factor))
                                    temp = temp // factor
                                    break
                                factor += 1
                            else:
                                factors.append(str(temp))
                                temp = 1
                    if len(factors) >= 2:
                        return '(' + ' * '.join(factors) + ')'
                    else:
                        # 回退到加法
                        part1 = random.randint(1, value - 1)
                        part2 = value - part1
                        return f"({part1} + {part2})"
            elif split_method == 'subtract':
                # 减法拆分: 100 -> 150 - 50
                larger = value + random.randint(1, value)
                return f"({larger} - {larger - value})"
            else:  # divide
                # 除法拆分: 100 -> 200 / 2
                if value > 0:
                    divisor = random.choice([2, 4, 8, 10])
                    dividend = value * divisor
                    return f"({dividend} / {divisor})"

            return value_str

        # 匹配整数，但避免匹配地址中的十六进制
        pattern = r'(?<!0x)\b\d{2,}\b(?!\w)'
        return re.sub(pattern, replace_constant, code)

