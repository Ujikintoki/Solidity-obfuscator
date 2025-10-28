#include "ast_generator.h"
#include <iostream>

int main() {
    // test solc
    std::string input_sol = "test/testdemo2.sol";
    std::string output_ast = "test/testdemo2.ast";     // 输出 AST 的路径

    bool success = generate_ast(input_sol, output_ast);

    if (success) {
        std::cout << "AST 生成成功！输出文件：" << output_ast << std::endl;
    } else {
        std::cout << "AST 生成失败！可能原因：solc 未安装、合约有错误或路径无效。" << std::endl;
    }

    // test2 
    bool fail_case = generate_ast("error.sol", "error_ast.json");
    if (!fail_case) {
        std::cout << "错误处理正常：对无效文件返回失败。" << std::endl;
    }

    return 0;
}