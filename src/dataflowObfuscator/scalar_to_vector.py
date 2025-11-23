"""
标量转向量（Scalar to Vector）模块
将单个标量变量转换为包含该标量的结构体
"""
import re
from utils.tools import generate_random_name
from .base import BaseObfuscator


class ScalarToVectorObfuscator(BaseObfuscator):
    """
    标量转向量混淆器
    """
    
    def obfuscate(self, code):
        """
        将单个标量变量转换为包含该标量的结构体
        :param code: Input code
        :return: Code with scalars converted to structs
        """
        # 查找合约定义
        contract_match = re.search(r'contract\s+(\w+)\s*\{', code)
        if not contract_match:
            return code

        contract_start = contract_match.end()
        contract_body = code[:contract_start]
        rest_code = code[contract_start:]

        # 查找标量变量声明（uint256, int, address 等）
        # 使用非捕获组避免组号混乱
        # 注意：排除 bool 类型，因为布尔变量应该由 split_boolean_variable 处理
        scalar_types = r'(?:u?int(?:8|16|32|64|128|256)?|address)'
        scalar_var_pattern = rf'\b({scalar_types})\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=\s*([^;]+))?;'

        struct_defs = []
        scalar_to_struct_map = {}

        def process_scalar_var(match):
            var_type = match.group(1)
            var_name = match.group(2)  # 修复：变量名是第2组
            var_init = match.group(3) if match.group(3) else None  # 修复：初始值是第3组

            # 检查变量名是否有效
            if not var_name:
                return match.group(0)

            # 跳过已经在映射中的变量
            if var_name in scalar_to_struct_map:
                return match.group(0)

            # 检查变量是否在函数内部（局部变量）
            # 查找变量声明之前的代码，看是否有未闭合的函数
            match_start = match.start()
            context_before = rest_code[:match_start]
            
            # 查找所有 function 关键字的位置
            is_local_var = False
            function_pattern = r'function\s+\w+\s*\([^)]*\)\s*(?:public|private|internal|external)?\s*(?:view|pure|payable)?\s*\{'
            function_matches = list(re.finditer(function_pattern, context_before))
            
            if function_matches:
                # 从最后一个 function 开始检查大括号平衡
                last_function = function_matches[-1]
                func_end = last_function.end()
                between_code = context_before[func_end:]
                
                # 计算大括号平衡
                brace_count = 1  # function 后面有一个 {
                for char in between_code:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count <= 0:
                            # 函数已结束
                            break
                
                # 如果大括号未平衡（brace_count > 0），说明变量在函数内部
                if brace_count > 0:
                    is_local_var = True

            # 生成结构体名和成员名
            struct_name = self.generate_struct_name()
            member_name = generate_random_name(prefix="val_")
            scalar_to_struct_map[var_name] = (struct_name, member_name)

            # 创建结构体定义
            struct_def = f"    struct {struct_name} {{\n        {var_type} {member_name};\n    }}\n"
            struct_defs.append(struct_def)

            # 创建结构体变量声明
            # 对于局部变量，需要添加 memory 关键字
            memory_keyword = " memory" if is_local_var else ""
            if var_init:
                return f"{struct_name}{memory_keyword} {var_name} = {struct_name}({var_init});"
            else:
                return f"{struct_name}{memory_keyword} {var_name};"

        rest_code = re.sub(scalar_var_pattern, process_scalar_var, rest_code)

        # 替换变量使用（将原变量替换为结构体成员访问）
        for orig_name, (struct_name, member_name) in scalar_to_struct_map.items():
            # 安全检查：确保变量名有效
            if not orig_name or orig_name is None:
                continue
            # 替换变量引用为结构体成员访问（但避免替换声明、event 参数等）
            # 使用简单的模式，在替换函数中检查上下文
            pattern = r'\b' + re.escape(orig_name) + r'\b(?!\s*[\.=;])'
            replacement = f'{orig_name}.{member_name}'
            
            def replace_with_context(match):
                # 检查是否在 event 声明中
                match_start = match.start()
                # 向前查找最近的 event 关键字
                before_match = rest_code[:match_start]
                # 查找所有 event 声明的位置
                event_matches = list(re.finditer(r'event\s+\w+\s*\(', before_match))
                
                if event_matches:
                    # 从最后一个 event 开始检查
                    last_event = event_matches[-1]
                    event_start = last_event.start()
                    event_end = last_event.end()
                    
                    # 检查从 event 开始到匹配位置之间的代码
                    between_code = rest_code[event_end:match_start]
                    
                    # 计算括号平衡，看是否在 event 参数列表中
                    paren_count = 1  # event 后面有一个 (
                    for char in between_code:
                        if char == '(':
                            paren_count += 1
                        elif char == ')':
                            paren_count -= 1
                            if paren_count == 0:
                                # event 参数列表已结束
                                break
                    
                    # 如果括号未平衡（paren_count > 0），说明在 event 参数列表中
                    if paren_count > 0:
                        # 在 event 声明中，不替换
                        return match.group(0)
                
                return replacement
            
            rest_code = re.sub(pattern, replace_with_context, rest_code)

        # 将结构体定义插入到合约体中
        if struct_defs:
            struct_defs_code = '\n'.join(struct_defs)
            contract_body = contract_body.rstrip() + '\n' + struct_defs_code

        return contract_body + rest_code

