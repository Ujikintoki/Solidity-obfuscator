"""
本地变量转状态变量（Local to State）模块
将函数内的局部变量转换为合约的状态变量
"""
import re
from .base import BaseObfuscator


class LocalToStateObfuscator(BaseObfuscator):
    """
    本地变量转状态变量混淆器
    """
    
    def obfuscate(self, code):
        """
        将函数内的局部变量转换为合约的状态变量
        :param code: Input code
        :return: Code with local variables converted to state variables
        """
        # 找到合约定义的位置
        contract_match = re.search(r'contract\s+(\w+)\s*\{', code)
        if not contract_match:
            return code

        contract_start = contract_match.end()
        
        # 找到第一个函数定义的位置（作为状态变量和函数的边界）
        function_pattern = r'(function\s+\w+\s*\([^)]*\)\s*(?:public|private|internal|external)?\s*(?:view|pure|payable)?\s*\{)'
        function_match = re.search(function_pattern, code[contract_start:])
        if not function_match:
            return code

        # 提取合约体（在第一个函数之前的部分）
        contract_body_end = contract_start + function_match.start()
        contract_body = code[contract_start:contract_body_end]
        functions_code = code[contract_body_end:]
        
        # 确保 contract_body 不包含闭合大括号（应该只是状态变量等）
        # 清理可能的空白和换行
        contract_body = contract_body.rstrip()

        # 在函数中查找局部变量声明
        # 匹配模式：类型 变量名 = 值; (在函数体内)
        # 使用命名组和正确的捕获组顺序
        local_var_pattern = r'(?<![a-zA-Z_0-9])(bool|u?int(?:8|16|32|64|128|256)?|address|string|bytes(?:32)?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^;]+);'
        
        new_state_vars = []
        local_to_state_map = {}

        def process_local_var(match):
            var_type = match.group(1)
            var_name = match.group(2)  # 修复：变量名是第2组
            var_value = match.group(3).strip()  # 修复：初始值是第3组

            # 跳过已经在映射中的变量
            if var_name in local_to_state_map:
                return match.group(0)

            # 跳过 Solidity 关键字和常见函数名
            if var_name in ['msg', 'block', 'tx', 'this', 'super']:
                return match.group(0)

            # 生成状态变量名
            state_var_name = self.generate_state_variable_name()
            local_to_state_map[var_name] = state_var_name

            # 创建状态变量声明
            state_var_decl = f"    {var_type} private {state_var_name};\n"
            new_state_vars.append((state_var_decl, var_name, state_var_name, var_value))

            # 返回修改后的局部变量赋值（使用状态变量）
            return f"{state_var_name} = {var_value};"

        # 处理函数中的局部变量
        processed_functions = re.sub(local_var_pattern, process_local_var, functions_code)

        # 在函数中替换变量引用
        for local_name, state_name in local_to_state_map.items():
            # 替换变量引用（但避免替换声明和 event 参数）
            # 使用更精确的模式，避免在 event 声明中替换
            def replace_var(match):
                # 检查是否在 event 声明中
                match_start = match.start()
                before_match = processed_functions[:match_start]
                # 查找最近的 event 关键字
                event_match = re.search(r'event\s+\w+\s*\([^)]*$', before_match, re.MULTILINE)
                if event_match:
                    # 检查是否在 event 参数列表中
                    event_end = event_match.end()
                    after_event = before_match[event_end:]
                    # 如果 event 声明未结束（没有找到闭合括号），则不替换
                    if ')' not in processed_functions[event_end:match_start]:
                        return match.group(0)
                return state_name
            
            pattern = r'\b' + re.escape(local_name) + r'\b(?!\s*[=;])'
            processed_functions = re.sub(pattern, replace_var, processed_functions)

        # 将新状态变量插入到合约体中
        if new_state_vars:
            state_vars_code = '\n'.join([sv[0] for sv in new_state_vars])
            # 在构造函数中初始化这些状态变量
            constructor_init = []
            for _, local_name, state_name, init_value in new_state_vars:
                constructor_init.append(f"        {state_name} = {init_value};")
            
            # 将状态变量添加到合约体
            contract_body = contract_body.rstrip()
            if contract_body:  # 如果合约体不为空，添加换行
                contract_body = contract_body + '\n' + state_vars_code
            else:  # 如果合约体为空，直接添加状态变量
                contract_body = state_vars_code
            
            # 查找或创建构造函数（构造函数应该在合约体内）
            constructor_pattern = r'constructor\s*\([^)]*\)\s*\{'
            constructor_match = re.search(constructor_pattern, contract_body)
            
            if constructor_match:
                # 在构造函数中添加初始化
                # 使用更健壮的方法找到构造函数的结束位置
                brace_count = 0
                pos = constructor_match.end()
                constructor_end = -1
                for i in range(pos, len(contract_body)):
                    if contract_body[i] == '{':
                        brace_count += 1
                    elif contract_body[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            constructor_end = i
                            break
                
                if constructor_end != -1:
                    init_code = '\n        '.join(constructor_init) + '\n'
                    contract_body = (contract_body[:constructor_end] + 
                                    '\n        ' + init_code + 
                                    contract_body[constructor_end:])
            else:
                # 创建新的构造函数，插入到合约体末尾（状态变量之后）
                constructor_code = f"\n    constructor() {{\n        " + '\n        '.join(constructor_init) + "\n    }}\n"
                contract_body = contract_body.rstrip() + '\n' + constructor_code

        # 确保最终组合的代码结构正确
        # contract_body 应该在合约内部，functions_code 也应该在合约内部
        # 清理 contract_body 末尾可能的闭合大括号（不应该有）
        contract_body = contract_body.rstrip()
        if contract_body.endswith('}'):
            contract_body = contract_body[:-1].rstrip()
        
        # 清理 processed_functions 开头可能的空白
        processed_functions = processed_functions.lstrip()
        
        # 确保 contract_body 和 processed_functions 之间有适当的换行
        if contract_body and not contract_body.endswith('\n'):
            contract_body = contract_body.rstrip() + '\n'
        
        # 确保 processed_functions 以换行开始（如果 contract_body 不为空）
        if contract_body and processed_functions and not processed_functions.startswith('\n'):
            # 检查是否需要添加换行
            if not contract_body.rstrip().endswith('}'):
                processed_functions = '\n' + processed_functions
        
        # 组合代码：pragma + contract { + contract_body + functions_code
        result = code[:contract_start] + contract_body + processed_functions
        
        return result

