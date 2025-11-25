import json
import os
import re
from random import randint, random


class replaceComment:
    def __init__(self, _solContent):
        self.content = _solContent

    def replaceSingleComment(self, _content):
        def replace_match(match):
            comment_text = match.group(0).rstrip('\n')
            if comment_text.startswith('//'):
                star_count = randint(1, 20)
                return '//' + '*' * star_count + ('\n' if match.group(0).endswith('\n') else '')
            return match.group(0)

        pattern = r"//.*?(\n|$)"
        return re.sub(pattern, replace_match, _content)

    def replaceMultiComment(self, _content):
        def replace_match(match):
            comment_text = match.group(0)
            if comment_text.startswith('/*') and comment_text.endswith('*/'):
                content_length = len(comment_text) - 4
                if content_length > 0:
                    star_count = randint(1, max(3, content_length))
                    return '/*' + '*' * star_count + '*/'
            return match.group(0)

        pattern = r"/\*((.)|((\r)?\n))*?\*/"
        return re.sub(pattern, replace_match, _content, re.S)

    def doReplace(self):
        nowContent = self.content
        nowContent = self.replaceSingleComment(nowContent)
        nowContent = self.replaceMultiComment(nowContent)
        return nowContent


class changeFormat:
    def __init__(self, _solContent):
        self.content = _solContent

    def reSubT(self, _content):
        pattern = r"\t"
        return re.sub(pattern, " ", _content)

    def reSubN(self, _content):
        lines = _content.split('\n')
        new_lines = []
        consecutive_empty = 0

        for line in lines:
            stripped_line = line.strip()
            if stripped_line == '':
                consecutive_empty += 1
                if consecutive_empty <= 1:
                    new_lines.append('')
            else:
                consecutive_empty = 0
                compressed_line = re.sub(r'\s+', ' ', line.strip())
                new_lines.append(compressed_line)

        return '\n'.join(new_lines)

    def reSubS(self, _content):
        pattern = r"(\s){2,}"
        return re.sub(pattern, " ", _content)

    def doChange(self, _prob):
        nowContent = self.content
        if random() < _prob:
            nowContent = self.reSubT(nowContent)
        nowContent = self.reSubN(nowContent)
        if random() < _prob:
            nowContent = self.reSubS(nowContent)
        return nowContent


class replaceVarName:
    def __init__(self, sourceCode, astJsonData):
        self.sourceCodeContent = sourceCode
        self.astData = astJsonData
        self.reserved_keywords = {
            'pragma', 'contract', 'function', 'returns', 'public', 'private', 'internal', 'external',
            'view', 'pure', 'payable', 'constructor', 'modifier', 'event', 'struct', 'enum',
            'if', 'else', 'for', 'while', 'do', 'break', 'continue', 'return',
            'uint', 'uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256',
            'int', 'int8', 'int16', 'int32', 'int64', 'int128', 'int256',
            'address', 'bool', 'string', 'bytes', 'bytes1', 'bytes32',
            'mapping', 'array', 'memory', 'storage', 'calldata',
            'require', 'assert', 'revert', 'emit', 'new', 'delete', 'selfdestruct',
            'true', 'false', 'this', 'super',
            'msg', 'block', 'tx', 'now', 'gasleft'
        }

    def extractAllIdentifiers(self, jsonData):
        print("开始解析AST查找标识符...")
        identifiers = set()

        def traverse_node(node, depth=0):
            if depth > 50:
                return

            if isinstance(node, dict):
                node_type = node.get('nodeType', '')

                if node_type in ['VariableDeclaration', 'FunctionDefinition', 'ContractDefinition']:
                    name = node.get('name')
                    if (name and isinstance(name, str) and
                            name not in self.reserved_keywords and
                            len(name) > 1 and
                            not name.startswith('msg') and
                            not name.startswith('block') and
                            not name.startswith('tx')):
                        identifiers.add(name)

                for key, value in node.items():
                    if key not in ['src', 'id', 'referencedDeclaration', 'absolutePath']:
                        traverse_node(value, depth + 1)

            elif isinstance(node, list):
                for item in node:
                    traverse_node(item, depth + 1)

        if isinstance(jsonData, dict):
            if 'nodes' in jsonData:
                traverse_node(jsonData['nodes'])
            elif 'ast' in jsonData:
                traverse_node(jsonData['ast'])
            else:
                traverse_node(jsonData)

        identifiers = {id for id in identifiers if id and len(id) > 1}
        print(f"找到 {len(identifiers)} 个可替换标识符: {list(identifiers)}")
        return identifiers

    def doReplace(self, replacementProbability):
        print("开始变量名替换...")
        identifierList = self.extractAllIdentifiers(self.astData)
        obfuscatedContent = self.sourceCodeContent

        if not identifierList:
            print("警告: 没有找到任何标识符进行替换")
            print("尝试手动提取变量名...")
            manual_identifiers = self._extractIdentifiersFromSource(obfuscatedContent)
            if manual_identifiers:
                print(f"手动找到标识符: {manual_identifiers}")
                identifierList = manual_identifiers

        replace_count = 0
        used_names = set()
        sorted_identifiers = sorted(identifierList, key=len, reverse=True)

        for identifier in sorted_identifiers:
            if (identifier and len(identifier) > 1 and
                    identifier not in self.reserved_keywords and
                    random() < replacementProbability):

                print(f"正在替换: '{identifier}'")
                new_name = self._generateUniqueName(identifier, used_names)
                used_names.add(new_name)

                old_content = obfuscatedContent
                obfuscatedContent = self._replaceSingleIdentifier(obfuscatedContent, identifier, new_name)

                if old_content != obfuscatedContent:
                    replace_count += 1
                    print(f"成功替换 '{identifier}' -> '{new_name}'")

        print(f"成功替换了 {replace_count} 个标识符")
        return obfuscatedContent

    def _extractIdentifiersFromSource(self, sourceCode):
        patterns = [
            r'\b(address|uint256|string|bool)\s+(public|private|internal|external)?\s*(\w+)\s*[;=]',
            r'function\s+(\w+)\s*\(',
            r'contract\s+(\w+)',
            r'modifier\s+(\w+)',
            r'event\s+(\w+)',
            r'struct\s+(\w+)'
        ]

        identifiers = set()
        for pattern in patterns:
            matches = re.findall(pattern, sourceCode)
            for match in matches:
                if isinstance(match, tuple):
                    for item in match:
                        if (item and len(item) > 1 and
                                item not in ['public', 'private', 'internal', 'external'] and
                                item not in self.reserved_keywords):
                            identifiers.add(item)
                elif match and len(match) > 1 and match not in self.reserved_keywords:
                    identifiers.add(match)

        return identifiers

    def _buildRegexPattern(self, targetString):
        return r"\b" + re.escape(targetString) + r"\b"

    def _generateUniqueName(self, originalString, used_names):
        counter = len(used_names) + 1
        while True:
            new_name = f"v_{counter:04d}"
            if new_name not in used_names:
                return new_name
            counter += 1

    def _replaceSingleIdentifier(self, codeContent, identifierName, newName):
        try:
            protected_patterns = [
                r'msg\.sender', r'msg\.value', r'block\.timestamp', r'block\.number',
                r'tx\.origin', r'require\(', r'assert\(', r'revert\('
            ]

            for pattern in protected_patterns:
                if identifierName in pattern:
                    print(f"跳过保护标识符: {identifierName}")
                    return codeContent

            regexPattern = self._buildRegexPattern(identifierName)
            new_content = re.sub(regexPattern, newName, codeContent)
            return new_content
        except Exception as e:  # pragma: no cover - defensive
            print(f"替换错误 {identifierName}: {e}")
            return codeContent


class LayoutObfuscator:
    def __init__(self, sol_file, ast_file, output_sol_path=None):
        self.sol_file = sol_file
        self.ast_file = ast_file
        self.output_sol = output_sol_path or self.get_output_filename(sol_file, "_obfuscated")
        self.output_ast = self.get_output_filename(ast_file, "_obfuscated") if ast_file else None

    def get_output_filename(self, filename, suffix):
        name, ext = os.path.splitext(filename)
        return f"{name}{suffix}{ext}"

    def read_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, filename, content):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def obfuscate(self,
                  replace_comments=True,
                  change_format=True,
                  replace_variables=True,
                  format_prob=0.5,
                  variable_prob=0.8):
        print("开始智能合约混淆...")

        sol_content = self.read_file(self.sol_file)
        original_length = len(sol_content)
        print(f"原始Solidity文件长度: {original_length} 字符")

        try:
            ast_content = self.read_file(self.ast_file)
            ast_json = json.loads(ast_content)
            print("成功读取和解析AST文件")
        except Exception as e:
            print(f"AST文件处理错误: {e}")
            print("跳过变量名替换...")
            ast_json = {}
            replace_variables = False

        if replace_comments:
            print("步骤1: 替换注释内容为星号...")
            rc = replaceComment(sol_content)
            sol_content = rc.doReplace()

        if change_format:
            print("步骤2: 调整代码格式...")
            cf = changeFormat(sol_content)
            sol_content = cf.doChange(format_prob)

        if replace_variables and ast_json:
            print("步骤3: 替换变量名和函数名...")
            rvn = replaceVarName(sol_content, ast_json)
            sol_content = rvn.doReplace(variable_prob)
        else:
            print("跳过变量名替换步骤")

        print("保存混淆结果...")
        self.write_file(self.output_sol, sol_content)

        print("混淆完成!")
        print(f"输出文件: {self.output_sol}")
        print(f"文件大小变化: {original_length} -> {len(sol_content)} 字符")

        print("\n混淆后内容预览:")
        print(sol_content[:500] + "..." if len(sol_content) > 500 else sol_content)

        return self.output_sol

