"""
布尔变量拆分（Split Boolean Variable）模块
将单个布尔变量的逻辑拆分到多个布尔变量的组合中
"""
import re
import random
from utils.tools import generate_random_name
from .base import BaseObfuscator


class SplitBooleanVariableObfuscator(BaseObfuscator):
    """
    布尔变量拆分混淆器
    """
    
    def obfuscate(self, code):
        """
        将单个布尔变量的逻辑拆分到多个布尔变量的组合中
        :param code: Input code
        :return: Code with boolean variables split
        """
        # 查找布尔变量声明
        bool_var_pattern = r'\b(bool\s+)([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*([^;]+))?;'
        
        split_map = {}  # 原变量名 -> (新变量1, 新变量2)

        def process_bool_var(match):
            var_type = match.group(1)
            var_name = match.group(2)
            var_init = match.group(3) if match.group(3) else None

            # 跳过已经在映射中的变量
            if var_name in split_map:
                return match.group(0)

            # 生成两个新的布尔变量名
            bool_var1 = generate_random_name(prefix="bool_")
            bool_var2 = generate_random_name(prefix="bool_")
            split_map[var_name] = (bool_var1, bool_var2)

            # 创建拆分后的变量声明
            if var_init:
                # 如果初始化值为 true，则两个变量都为 true
                # 如果为 false，则两个变量都为 false
                # 使用 XOR 或其他逻辑组合
                if 'true' in var_init or '1' in var_init:
                    init1 = 'true'
                    init2 = 'true'
                elif 'false' in var_init or '0' in var_init:
                    init1 = 'false'
                    init2 = 'false'
                else:
                    init1 = var_init
                    init2 = 'false'
                
                return f"{var_type}{bool_var1} = {init1};\n    {var_type}{bool_var2} = {init2};\n    // Original: {var_name} = {bool_var1} && {bool_var2};"
            else:
                return f"{var_type}{bool_var1};\n    {var_type}{bool_var2};\n    // Original: {var_name} = {bool_var1} && {bool_var2};"

        code = re.sub(bool_var_pattern, process_bool_var, code)

        # 替换变量使用（将原变量替换为两个变量的逻辑组合）
        for orig_name, (var1, var2) in split_map.items():
            # 使用 && 或 || 组合（根据原始值决定）
            # 如果原始值为 true，使用 &&；如果为 false，使用 ||
            logic_op = random.choice(['&&', '||'])
            replacement = f'({var1} {logic_op} {var2})'
            
            # 替换变量引用（但避免替换声明、赋值和结构体成员访问）
            # 避免匹配已经转换为结构体成员的变量（如 flag.val_xxx）
            pattern = r'(?<!\.)\b' + re.escape(orig_name) + r'\b(?!\s*[=;\.])'
            code = re.sub(pattern, replacement, code)

        return code

