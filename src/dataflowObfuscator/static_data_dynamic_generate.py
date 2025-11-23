"""
静态数据动态生成（Static Data Dynamic Generate）模块
将合约中固定的常量转换为通过动态计算生成的形式
"""
import re
import random
from utils.tools import generate_random_name
from .base import BaseObfuscator


class StaticDataDynamicGenerateObfuscator(BaseObfuscator):
    """
    静态数据动态生成混淆器
    """
    
    def obfuscate(self, code):
        """
        将合约中固定的常量转换为通过动态计算生成的形式
        :param code: Input code
        :return: Code with static data converted to dynamic generation
        """
        # 处理地址常量 (0x...)
        def replace_address(match):
            addr = match.group(0)
            # 将地址转换为计算形式
            # 例如: 0x1234... -> address(uint160(uint256(keccak256(abi.encodePacked("seed"))) % (2**160)))
            seed = generate_random_name(length=6)
            return f'address(uint160(uint256(keccak256(abi.encodePacked("{seed}"))) % (2**160)))'

        address_pattern = r'0x[a-fA-F0-9]{40}'
        code = re.sub(address_pattern, replace_address, code)

        # 处理大整数常量（大于某个阈值）
        def replace_large_int(match):
            value = int(match.group(0))
            if value > 1000:  # 只处理较大的整数
                # 拆分为多个部分进行计算
                parts = []
                remaining = value
                num_parts = random.randint(2, 4)
                for i in range(num_parts - 1):
                    part = random.randint(1, remaining // 2)
                    parts.append(str(part))
                    remaining -= part
                parts.append(str(remaining))
                ops = ['+', '*', '-']
                op = random.choice(ops)
                if op == '+':
                    return '(' + ' + '.join(parts) + ')'
                elif op == '*':
                    # 对于乘法，需要分解因子
                    factors = []
                    temp = value
                    for _ in range(2):
                        if temp > 1:
                            factor = random.randint(2, int(temp ** 0.5) + 1)
                            factors.append(str(factor))
                            temp = temp // factor
                    if temp > 1:
                        factors.append(str(temp))
                    return '(' + ' * '.join(factors) + ')'
                else:  # '-'
                    larger = value + random.randint(1, value // 2)
                    return f'({larger} - {larger - value})'
            return match.group(0)

        int_pattern = r'\b\d{4,}\b'  # 4位或更多位的整数
        code = re.sub(int_pattern, replace_large_int, code)

        # 处理字符串常量（转换为动态生成）
        def replace_string(match):
            str_content = match.group(1)
            # 将字符串转换为通过 keccak256 哈希后解码的形式（简化处理）
            # 实际应用中可能需要更复杂的处理
            seed = generate_random_name(length=6)
            return f'string(abi.encodePacked(keccak256(abi.encodePacked("{seed}"))))'

        # 注意：字符串替换需要更谨慎，避免替换函数名等
        # string_pattern = r'"([^"]*)"'
        # code = re.sub(string_pattern, replace_string, code)

        # 处理布尔常量
        def replace_bool(match):
            bool_val = match.group(0)
            if bool_val == 'true':
                return '(1 == 1)'
            else:
                return '(1 == 0)'

        bool_pattern = r'\b(true|false)\b'
        code = re.sub(bool_pattern, replace_bool, code)

        return code

