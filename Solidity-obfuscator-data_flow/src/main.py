# import os
# import sys
# import subprocess
# from data_flow_obfuscation.dataflow import dataflowObfuscation

# def main():
#     if len(sys.argv) == 3:
#         sol_path = sys.argv[1]       # 源合约路径
#         ast_path = sys.argv[2]       # 预编译的AST路径
#     else:
#         # 默认测试文件路径
#         sol_path = "./test/test.sol"
#         ast_path = "./test/test_ast.json"

#     if not os.path.exists(sol_path):
#         print(f"错误：源合约文件不存在 - {sol_path}")
#         return
#     if not os.path.exists(ast_path):
#         print(f"错误：AST文件不存在 - {ast_path}")
#         # 尝试自动编译生成AST（可选）
#         print("尝试自动编译生成AST...")
#         try:
#             # 调用solc编译生成AST
#             subprocess.run(
#                 ["solc", "--ast-compact-json", "--overwrite", sol_path, "-o", os.path.dirname(ast_path)],
#                 check=True,
#                 capture_output=True
#             )
#             print(f"已自动生成AST: {ast_path}")
#         except Exception as e:
#             print(f"自动编译失败: {str(e)}")
#             return

#     # 3. 初始化并执行数据流混淆
#     try:
#         # dataflowObfuscation类初始化参数（sol文件路径, AST文件路径）
#         obfuscator = dataflowObfuscation(sol_path, ast_path)
#         obfuscator.run()  # 执行混淆流程
#         print(f"Save file: {obfuscator.outputFileName}")
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return

# if __name__ == "__main__":
#     main()
#!/usr/bin/python
#-*- coding: utf-8 -*-

# from layoutConfuse import layoutConfuse
from data_flow_obfuscation.dataflow import dataflowObfuscation
import os
import sys


def main():
	if len(sys.argv) != 3:
		print("wrong parameters.")
	else:	
		dfo = dataflowObfuscation(sys.argv[1], sys.argv[2])
		dfo.run()
		# lc = layoutConfuse("temp.sol", "temp.sol_json.ast")
		# lc.run()


colors = True # Output should be colored
machine = sys.platform # Detecting the os of current system
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False # Colors shouldn't be displayed in mac & windows
if not colors:
	end = green = bad = info = ''
	start = ' ['
	stop = ']'
else:
	end = '\033[1;m'
	green = '\033[1;32m'
	white = "\033[1;37m"
	blue = "\033[1;34m"
	yellow = "\033[1;33m"
	bad = '\033[1;31m[-]\033[1;m'
	info = '\033[1;33m[!]\033[1;m'
	start = ' \033[1;31m[\033[0m'
	stop = '\033[1;31m]\033[0m'
	backGreenFrontWhite = "\033[1;37m\033[42m"
main()