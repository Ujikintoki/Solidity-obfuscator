"""
Base class for dataflow obfuscation modules
提供所有子模块共享的基础功能
"""
from utils.tools import generate_random_name


class BaseObfuscator:
    """
    基础混淆器类，提供所有子模块共享的方法
    """
    
    def __init__(self):
        """
        Initialize the base obfuscator
        """
        self.temp_variable_counter = 0
        self.state_variable_counter = 0
        self.struct_counter = 0
        self.local_to_state_map = {}  # 映射局部变量名到状态变量名
        self.scalar_to_struct_map = {}  # 映射标量变量到结构体

    def generate_temp_variable(self):
        """
        Generate a temporary variable name
        :return: Temporary variable name
        """
        self.temp_variable_counter += 1
        return f"tempVar_{self.temp_variable_counter}"

    def generate_state_variable_name(self):
        """
        Generate a state variable name
        :return: State variable name
        """
        self.state_variable_counter += 1
        return generate_random_name(prefix="state_")

    def generate_struct_name(self):
        """
        Generate a struct name
        :return: Struct name
        """
        self.struct_counter += 1
        return generate_random_name(prefix="Struct_")

