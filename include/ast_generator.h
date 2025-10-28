#ifndef AST_GENERATOR_H
#define AST_GENERATOR_H

#include <string>

// 生成 Solidity 合约的 AST（JSON 格式）
// 参数：input_sol_path（输入 .sol 文件路径），output_ast_path（输出 .ast.json 文件路径）
// 返回值：true 表示成功，false 表示失败（如 solc 未安装、合约编译错误）
bool generate_ast(const std::string& input_sol_path, const std::string& output_ast_path);

#endif // AST_GENERATOR_H