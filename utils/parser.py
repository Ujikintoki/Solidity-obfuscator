import os
import sys
import subprocess
import json
import re

class SolidityParser:
    """
    调用 solc 编译器，将 .sol 文件解析为 AST JSON 文件。
    """
    def __init__(self, sol_file_path):
        self.sol_file_path = sol_file_path
        
        try:
            # 检查 solc 是否可用
            subprocess.run(['solc', '--version'], check=True, capture_output=True)
        except FileNotFoundError:
            print("错误: 找不到 solc 编译器。请确保 solc 已安装并配置到 PATH 环境变量中。")
            sys.exit(1)
        except subprocess.CalledProcessError:
            pass

    def get_ast_output_path(self):
        """生成 AST 文件的输出路径，格式为 xxx.ast"""
        name, ext = os.path.splitext(self.sol_file_path)
        return f"{name}.ast"

    def clean_solc_output(self, raw_output):
        """
        清理 solc 输出，提取有效的 JSON 部分。
        :param raw_output: solc 的原始输出字符串
        :return: 纯净的 JSON 字符串
        """
        # 查找第一个 { 的位置
        start = raw_output.find('{')
        # 查找最后一个 } 的位置
        end = raw_output.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            # 提取纯净的 JSON 字符串
            return raw_output[start : end + 1]
        else:
            print("错误: 无法在 solc 输出中找到有效的 JSON 结构。")
            return ""

    def parse_to_ast(self):
        """
        调用 solc --ast-compact-json 命令生成 AST 文件。
        :return: 生成的 AST 文件路径 (str)
        """
        if not os.path.exists(self.sol_file_path):
            print(f"错误: Solidity 文件 '{self.sol_file_path}' 不存在。")
            return None

        output_path = self.get_ast_output_path()
        
        # 使用 --ast-compact-json
        command = [
            'solc',
            '--ast-compact-json',
            self.sol_file_path
        ]
        
        print(f"正在调用 solc 解析 AST...")
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
            
            # 清理 solc 的无效输出
            ast_content = self.clean_solc_output(result.stdout)
            
            if not ast_content:
                 # 清理后没有内容
                if result.stderr:
                    print(f"Solc 报告错误: \n{result.stderr}")
                return None

            # 写入 AST 文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(ast_content)
            
            print(f"成功: AST 文件已生成到 '{output_path}'")
            return output_path

        except subprocess.CalledProcessError as e:
            print("-" * 50)
            print(f"错误: Solc 编译或解析失败，请检查 Solidity 文件语法。")
            print(f"Solc 输出 (Stderr):\n{e.stderr}")
            print("-" * 50)
            return None
        except Exception as e:
            print(f"发生未知错误: {e}")
            return None

def main():
    """
    接收命令行参数 <solidity_file.sol> 并执行解析。
    """
    if len(sys.argv) != 2:
        print("用法: python parser.py <solidity_file.sol>")
        sys.exit(1)

    sol_file = sys.argv[1]
    if not sol_file.lower().endswith('.sol'):
        print(f"错误: 文件 '{sol_file}' 不是 Solidity 文件。")
        sys.exit(1)

    parser = SolidityParser(sol_file)
    ast_path = parser.parse_to_ast()

    if ast_path:
        print(f"解析流程完成，AST 文件路径: {ast_path}")

if __name__ == "__main__":
    main()