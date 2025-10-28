#include "ast_generator.h"
#include <cstdio>  // popen/pclose
#include <string>

bool generate_ast(const std::string& input_sol_path, const std::string& output_ast_path) {
    // 构建 solc 命令：solc --ast-json 输入文件 > 输出文件
    // 注意：--ast-json 会输出带格式的 AST，若需压缩可加 --pretty-json false
    std::string cmd = "solc --ast-json " + input_sol_path + " > " + output_ast_path;

    // 执行命令并捕获错误（若合约有编译错误，solc 会返回非 0 状态）
    FILE* pipe = popen(cmd.c_str(), "r");
    if (!pipe) {
        return false; // 命令执行失败（如 solc 未安装）
    }

    // 等待命令执行完成，获取返回值
    int exit_status = pclose(pipe);
    if (exit_status != 0) {
        // 可能的原因：合约有语法错误、solc 版本不兼容
        return false;
    }

    return true;
}