"""
插入临时变量（Insert Temporary Variables）模块
在变量赋值过程中插入临时变量，将直接赋值拆分为多步间接赋值
"""
import re
from utils.tools import generate_random_name
from .base import BaseObfuscator


class InsertTempVariablesObfuscator(BaseObfuscator):
    """
    插入临时变量混淆器
    """
    
    def obfuscate(self, code):
        """
        在变量赋值过程中插入临时变量，将直接赋值拆分为多步间接赋值
        :param code: Input code
        :return: Code with temporary variables inserted
        """
        # 匹配变量声明和赋值: type var_name = value;
        # 更精确的模式，避免匹配常量声明
        # 使用正确的捕获组顺序（类型、变量名、初始值）
        pattern = r'(?<!constant\s)(?<!public\s)(?<!private\s)(?<!internal\s)(?<!external\s)\b(bool|u?int(?:8|16|32|64|128|256)?|address|string|bytes(?:32)?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^;]+);'

        def replace_assignment(match):
            var_type = match.group(1)
            var_name = match.group(2)  # 修复：变量名是第2组
            var_value = match.group(3).strip()  # 修复：初始值是第3组

            # 如果值太简单（只是一个字面量或单个变量），可能不需要插入临时变量
            if re.match(r'^[\d\w\s()]+$', var_value) and len(var_value.split()) <= 3:
                # 仍然插入，但使用更简单的形式
                temp_var = generate_random_name(prefix="tmp_")
                return f"{var_type} {temp_var} = {var_value};\n        {var_type} {var_name} = {temp_var};"
            else:
                # 插入临时变量
                temp_var = generate_random_name(prefix="tmp_")
                return f"{var_type} {temp_var} = {var_value};\n        {var_type} {var_name} = {temp_var};"

        return re.sub(pattern, replace_assignment, code)

