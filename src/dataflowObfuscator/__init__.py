"""
Dataflow Obfuscator Package
数据流混淆器包，包含多个子混淆模块
"""
from .base import BaseObfuscator
from .local_to_state import LocalToStateObfuscator
from .static_data_dynamic_generate import StaticDataDynamicGenerateObfuscator
from .literal_to_expression import LiteralToExpressionObfuscator
from .split_boolean_variable import SplitBooleanVariableObfuscator
from .scalar_to_vector import ScalarToVectorObfuscator
from .split_constants import SplitConstantsObfuscator
from .insert_temp_variables import InsertTempVariablesObfuscator

__all__ = [
    'BaseObfuscator',
    'LocalToStateObfuscator',
    'StaticDataDynamicGenerateObfuscator',
    'LiteralToExpressionObfuscator',
    'SplitBooleanVariableObfuscator',
    'ScalarToVectorObfuscator',
    'SplitConstantsObfuscator',
    'InsertTempVariablesObfuscator',
]

