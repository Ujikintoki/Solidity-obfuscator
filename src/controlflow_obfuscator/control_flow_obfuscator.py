import json
import random
import re
from random import choice, randint


class ControlFlowObfuscator:
    """
    控制流扁平化混淆器。
    """

    def __init__(self, sourceCode, astJsonData):
        self.source_code = sourceCode
        self.ast_data = astJsonData
        self.function_map = {}
        self.state_var_prefix = "cf_state_"
        self.fake_var_prefix = "fake_"
        self.obfuscation_strategies = [
            self._strategy_simple_state_machine,
            self._strategy_complex_state_machine,
            self._strategy_nested_conditions,
            self._strategy_switch_based,
            self._strategy_loop_based,
        ]

    def _get_src_code_by_loc(self, src_info):
        """
        根据 AST 的 src 信息（"offset:length:fileId"）提取源代码片段。
        """
        try:
            parts = src_info.split(':')
            if len(parts) < 2:
                raise ValueError("Invalid src format")

            offset, length = map(int, parts[:2])
            return self.source_code[offset:offset + length]
        except Exception:
            return ""

    def _generate_state_variable_name(self, func_name):
        """生成唯一的混淆状态变量名"""
        unique_id = hex(hash(func_name + str(randint(0, 99999))))[2:10]
        return f"{self.state_var_prefix}{unique_id}"

    def _generate_fake_variable_name(self):
        """生成虚假变量名"""
        fake_names = ["temp", "tmp", "data", "value", "result", "flag"]
        return f"{choice(fake_names)}_{randint(1000, 9999)}"

    def _generate_complex_expression(self, base_value):
        """生成复杂的等价表达式"""
        expressions = [
            f"{base_value}",
            f"({randint(100, 999)} % {randint(10, 99)} + {base_value} - {base_value}) + {base_value}",
            f"(block.timestamp % {randint(2, 50)}) == {randint(0, 1)} ? {base_value} : {base_value}",
            f"({base_value} * {randint(1, 3)}) / {randint(1, 3)}",
        ]
        return choice(expressions)

    def _generate_fake_transition(self, current_state, total_states):
        """生成虚假状态转移"""
        if random.random() < 0.3:
            return randint(1, total_states)
        elif random.random() < 0.6:
            return 0
        else:
            return f"({current_state} + {randint(1, 3)}) % {total_states + 1}"

    def _traverse_and_collect_functions(self, node):
        """
        遍历 AST，收集所有 FunctionDefinition 节点的 src 信息。
        """
        if isinstance(node, dict):
            node_type = node.get('nodeType', '')

            if node_type == 'FunctionDefinition':
                src = node.get('src')
                name = node.get('name', 'constructor')
                if not name:
                    name = 'constructor'

                body = node.get('body')
                if body and body.get('nodeType') == 'Block':
                    body_src = body.get('src')
                    statements = body.get('statements', [])
                    if statements:
                        self.function_map[src] = {
                            'name': name,
                            'body_src': body_src,
                            'statements': statements,
                            'node': node,
                        }

            for key, value in node.items():
                if key not in ['src', 'id', 'referencedDeclaration', 'absolutePath']:
                    self._traverse_and_collect_functions(value)

        elif isinstance(node, list):
            for item in node:
                self._traverse_and_collect_functions(item)

    def _extract_inner_code(self, func_info):
        """精确提取函数内部代码"""
        statements = func_info.get('statements', [])

        if not statements:
            return None

        first_statement_src = statements[0].get('src')
        try:
            start_offset, _, _ = map(int, first_statement_src.split(':'))
        except Exception:
            return None

        last_statement_src = statements[-1].get('src')
        try:
            last_offset, last_length, _ = map(int, last_statement_src.split(':'))
            end_offset = last_offset + last_length

            # 某些语句（如 ExpressionStatement / Return）在 AST 长度中不包含末尾分号，
            # 如果源代码紧随其后的是 ';'，手动将其纳入提取范围。
            if end_offset < len(self.source_code) and self.source_code[end_offset] == ';':
                end_offset += 1
                while end_offset < len(self.source_code) and self.source_code[end_offset].isspace():
                    end_offset += 1
        except Exception:
            return None

        inner_body_code = self.source_code[start_offset:end_offset].strip()

        code_without_comments = re.sub(r'//.*|\/\*[\s\S]*?\*\/|\s', '', inner_body_code)
        if not code_without_comments:
            return None

        return {
            'start': start_offset,
            'end': end_offset,
            'code': inner_body_code,
        }

    def _handle_control_flow_statements(self, code, state_var):
        """处理 return 语句，保持语法有效并在返回前更新状态。"""

        def replace_return(match):
            indent = match.group("indent") or ""
            return_value = match.group("value").strip() if match.group("value") else ""

            if return_value:
                return f"{indent}{state_var} = 0;\n{indent}return {return_value};"
            else:
                return f"{indent}{state_var} = 0;\n{indent}return;"

        return_pattern = r'(?P<indent>\s*)return\s*(?P<value>[^;]*)\s*;'
        code = re.sub(return_pattern, replace_return, code)

        return code

    def _add_anti_analysis_code(self):
        """添加反分析代码"""
        anti_patterns = [
            f"""
            // 环境检查
            if (tx.gasprice > {randint(100, 1000)} gwei) {{
                revert("Execution reverted");
            }}
            """,
            f"""
            // 区块检查
            if (block.number > {randint(1000000, 5000000)}) {{
                uint256 {self._generate_fake_variable_name()} = block.timestamp;
            }}
            """,
            f"""
            // 虚假的调用者检查
            if (msg.sender == address(0)) {{
                revert("Invalid sender");
            }}
            """,
        ]
        return choice(anti_patterns)

    def _strategy_simple_state_machine(self, func_name, inner_code):
        """策略1: 简单状态机"""
        state_var = self._generate_state_variable_name(func_name)
        magic_num = randint(100, 999)

        processed_code = self._handle_control_flow_statements(inner_code, state_var)

        return f"""
        uint256 {state_var} = {magic_num} - {magic_num} + 1;

        while ({state_var} != 0) {{
            if ({state_var} == 1) {{
                {processed_code}
                {state_var} = 0;
                continue;
            }}
            else if ({state_var} == 2) {{
                uint256 {self._generate_fake_variable_name()} = block.timestamp % {randint(10, 100)};
                {state_var} = 0;
                continue;
            }}
            else {{
                break;
            }}
        }}
        """

    def _strategy_complex_state_machine(self, func_name, inner_code):
        """策略2: 复杂状态机"""
        state_var = self._generate_state_variable_name(func_name)
        total_states = randint(4, 8)
        initial_state = randint(1, total_states)

        processed_code = self._handle_control_flow_statements(inner_code, state_var)

        state_machine = f"""
        uint256 {state_var} = {self._generate_complex_expression(initial_state)};
        uint256 _exec_counter = 0;
        """

        state_machine += self._add_anti_analysis_code()
        state_machine += f"""

        while ({state_var} != 0 && _exec_counter < {total_states * 2}) {{
            _exec_counter++;
            """

        real_state = randint(1, total_states)
        first_branch = True
        for state in range(1, total_states + 1):
            branch_keyword = "if" if first_branch else "else if"
            if state == real_state:
                state_machine += f"""
            {branch_keyword} ({state_var} == {state}) {{
                {processed_code}
                {state_var} = 0;
                continue;
            }}"""
            else:
                next_state = self._generate_fake_transition(state, total_states)
                state_machine += f"""
            {branch_keyword} ({state_var} == {state}) {{
                uint256 {self._generate_fake_variable_name()} = block.timestamp % {randint(2, 20)};
                {state_var} = {next_state};
                continue;
            }}"""
            first_branch = False

        state_machine += """
            else {
                break;
            }
        }
        """
        return state_machine

    def _strategy_nested_conditions(self, func_name, inner_code):
        """策略3: 嵌套条件状态机"""
        state_var = self._generate_state_variable_name(func_name)
        fake_var1 = self._generate_fake_variable_name()
        fake_var2 = self._generate_fake_variable_name()

        processed_code = self._handle_control_flow_statements(inner_code, state_var)

        return f"""
        uint256 {state_var} = 1;
        uint256 {fake_var1} = block.timestamp % {randint(10, 50)};
        uint256 {fake_var2} = {fake_var1} + {randint(1, 10)};

        for (uint256 i = 0; i < {randint(3, 10)}; i++) {{
            if ({state_var} == 1 && {fake_var1} > {randint(5, 20)}) {{
                {processed_code}
                {state_var} = 0;
                break;
            }}
            else if ({state_var} == 1 && {fake_var2} < {randint(30, 100)}) {{
                uint256 {self._generate_fake_variable_name()} = {fake_var1} * {fake_var2};
                {state_var} = {randint(0, 1)};
            }}
            else {{
                {fake_var1} = {fake_var1} + 1;
                {fake_var2} = {fake_var2} - 1;
            }}

            if ({state_var} == 0) break;
        }}
        """

    def _strategy_switch_based(self, func_name, inner_code):
        """策略4: 基于switch的状态机"""
        state_var = self._generate_state_variable_name(func_name)

        processed_code = self._handle_control_flow_statements(inner_code, state_var)

        return f"""
        uint256 {state_var} = 1;
        bool _completed = false;

        while (!_completed) {{
            if ({state_var} == 1) {{
                {processed_code}
                {state_var} = 0;
                _completed = true;
            }}
            else if ({state_var} == 2) {{
                uint256 {self._generate_fake_variable_name()} = block.number;
                {state_var} = {randint(0, 3)};
            }}
            else if ({state_var} == 3) {{
                uint256 {self._generate_fake_variable_name()} = tx.gasprice;
                {state_var} = 1;
            }}
            else {{
                _completed = true;
            }}
        }}
        """

    def _strategy_loop_based(self, func_name, inner_code):
        """策略5: 基于循环的混淆"""
        state_var = self._generate_state_variable_name(func_name)
        loop_limit = randint(5, 15)

        processed_code = self._handle_control_flow_statements(inner_code, state_var)

        return f"""
        uint256 {state_var} = 0;
        uint256 _iteration = 0;

        while (_iteration < {loop_limit}) {{
            _iteration++;

            if (_iteration == {randint(2, loop_limit-1)} && {state_var} == 0) {{
                {processed_code}
                {state_var} = 1;
            }}
            else if (_iteration % {randint(2, 4)} == 0) {{
                uint256 {self._generate_fake_variable_name()} = _iteration * block.timestamp;
            }}

            if ({state_var} == 1 && _iteration > {loop_limit // 2}) {{
                break;
            }}
        }}

        if ({state_var} == 0) {{
            {processed_code}
        }}
        """

    def _flatten_function(self, func_info):
        """执行函数控制流扁平化"""
        func_name = func_info['name']

        code_info = self._extract_inner_code(func_info)
        if not code_info:
            print(f"    跳过函数 {func_name}：无法提取有效代码。")
            return None

        strategy = choice(self.obfuscation_strategies)
        strategy_name = strategy.__name__.replace('_strategy_', '').replace('_', ' ').title()
        print(f"    使用策略: {strategy_name}")

        obfuscated_code = strategy(func_name, code_info['code'])

        return {
            'start': code_info['start'],
            'end': code_info['end'],
            'new_code': obfuscated_code,
        }

    def _apply_replacements(self, replacements):
        """
        根据替换列表，从后往前对代码进行文本替换，以避免 offset 错误。
        """
        sorted_replacements = sorted(replacements, key=lambda x: x['end'], reverse=True)

        current_code = self.source_code
        for rep in sorted_replacements:
            start = rep['start']
            end = rep['end']
            new_code = rep['new_code']

            current_code = current_code[:start] + new_code + current_code[end:]

        return current_code

    def doObfuscate(self):
        """执行混淆操作"""
        print("步骤: 开始增强版控制流扁平化混淆...")

        if not self.ast_data:
            print("错误: 缺少有效的AST数据，跳过控制流扁平化。")
            return self.source_code

        ast_root = self.ast_data.get('ast', self.ast_data)
        self._traverse_and_collect_functions(ast_root)

        if not self.function_map:
            print("警告: 未在AST中找到任何非空函数定义进行扁平化。")
            return self.source_code

        replacements = []
        for _, func_info in self.function_map.items():
            print(f"正在处理函数: {func_info['name']}")
            replacement = self._flatten_function(func_info)
            if replacement and isinstance(replacement, dict):
                replacements.append(replacement)
            elif replacement is None:
                print(f"    跳过函数 {func_info['name']}：无法处理函数体内容。")

        if replacements:
            obfuscated_code = self._apply_replacements(replacements)
            print(f"成功扁平化 {len(replacements)} 个函数。")
        else:
            obfuscated_code = self.source_code
            print("未执行任何控制流扁平化。")

        return obfuscated_code

