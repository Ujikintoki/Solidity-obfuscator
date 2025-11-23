"""
Data Flow Obfuscator - 实现多种数据流混淆技术
使用模块化的子混淆器实现各种混淆功能
"""
from src.dataflowObfuscator import (
    LocalToStateObfuscator,
    StaticDataDynamicGenerateObfuscator,
    LiteralToExpressionObfuscator,
    SplitBooleanVariableObfuscator,
    ScalarToVectorObfuscator,
    SplitConstantsObfuscator,
    InsertTempVariablesObfuscator,
)


class DataflowObfuscator:
    """
    Data Flow Obfuscator - 实现多种数据流混淆技术
    通过组合各个子混淆模块来实现完整的混淆功能
    """

    def __init__(self):
        """
        Initialize the obfuscator and its sub-modules
        """
        # 初始化各个子混淆器
        self.local_to_state_obfuscator = LocalToStateObfuscator()
        self.static_data_dynamic_generate_obfuscator = StaticDataDynamicGenerateObfuscator()
        self.literal_to_expression_obfuscator = LiteralToExpressionObfuscator()
        self.split_boolean_variable_obfuscator = SplitBooleanVariableObfuscator()
        self.scalar_to_vector_obfuscator = ScalarToVectorObfuscator()
        self.split_constants_obfuscator = SplitConstantsObfuscator()
        self.insert_temp_variables_obfuscator = InsertTempVariablesObfuscator()

    def generate_temp_variable(self):
        """
        Generate a temporary variable name
        :return: Temporary variable name
        """
        return self.insert_temp_variables_obfuscator.generate_temp_variable()

    def generate_state_variable_name(self):
        """
        Generate a state variable name
        :return: State variable name
        """
        return self.local_to_state_obfuscator.generate_state_variable_name()

    def generate_struct_name(self):
        """
        Generate a struct name
        :return: Struct name
        """
        return self.scalar_to_vector_obfuscator.generate_struct_name()

    # ==================== 1. 本地变量转状态变量（Local to State） ====================
    def local_to_state(self, code):
        """
        将函数内的局部变量转换为合约的状态变量
        :param code: Input code
        :return: Code with local variables converted to state variables
        """
        return self.local_to_state_obfuscator.obfuscate(code)

    # ==================== 2. 静态数据动态生成（Static Data Dynamic Generate） ====================
    def static_data_dynamic_generate(self, code):
        """
        将合约中固定的常量转换为通过动态计算生成的形式
        :param code: Input code
        :return: Code with static data converted to dynamic generation
        """
        return self.static_data_dynamic_generate_obfuscator.obfuscate(code)

    # ==================== 3. 字面量转表达式（Literal to Expression） ====================
    def literal_to_expression(self, code):
        """
        将整数、布尔值等字面量转换为等价的算术或逻辑表达式
        :param code: Input code
        :return: Code with literals converted to expressions
        """
        return self.literal_to_expression_obfuscator.obfuscate(code)

    # ==================== 4. 布尔变量拆分（Split Boolean Variable） ====================
    def split_boolean_variable(self, code):
        """
        将单个布尔变量的逻辑拆分到多个布尔变量的组合中
        :param code: Input code
        :return: Code with boolean variables split
        """
        return self.split_boolean_variable_obfuscator.obfuscate(code)

    # ==================== 5. 标量转向量（Scalar to Vector） ====================
    def scalar_to_vector(self, code):
        """
        将单个标量变量转换为包含该标量的结构体
        :param code: Input code
        :return: Code with scalars converted to structs
        """
        return self.scalar_to_vector_obfuscator.obfuscate(code)

    # ==================== 6. 常量拆分（Split Constants） ====================
    def split_constants(self, code):
        """
        将较大的整数常量拆分为多个小整数的算术组合
        :param code: Input code
        :return: Code with constants split into expressions
        """
        return self.split_constants_obfuscator.obfuscate(code)

    # ==================== 7. 插入临时变量（Insert Temporary Variables） ====================
    def insert_temp_variables(self, code):
        """
        在变量赋值过程中插入临时变量，将直接赋值拆分为多步间接赋值
        :param code: Input code
        :return: Code with temporary variables inserted
        """
        return self.insert_temp_variables_obfuscator.obfuscate(code)

    # ==================== 主混淆方法 ====================
    def obfuscate(self, code):
        """
        应用所有数据流混淆技术
        :param code: Input code
        :return: Obfuscated code
        """
        # 按顺序应用各种混淆技术
        
        # 1. 字面量转表达式（先处理，为后续步骤做准备）
        code = self.literal_to_expression(code)
        
        # 2. 常量拆分
        code = self.split_constants(code)
        
        # 3. 静态数据动态生成
        code = self.static_data_dynamic_generate(code)
        
        # 4. 标量转向量（在局部变量转状态变量之前，因为状态变量可能是标量）
        # code = self.scalar_to_vector(code)
        
        # 5. 本地变量转状态变量
        # code = self.local_to_state(code)
        
        # 6. 布尔变量拆分
        # code = self.split_boolean_variable(code)
        
        # 7. 插入临时变量（最后处理，增加赋值链的复杂度）
        code = self.insert_temp_variables(code)

        return code
