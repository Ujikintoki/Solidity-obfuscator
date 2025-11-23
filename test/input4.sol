// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TestContract {
    uint public myNumber;

    function setValue(uint _value) public {
        uint localVar = _value * 2; // 本地变量
        myNumber = localVar + 10;   // 整数常量
        bool flag = (myNumber > 100); // 布尔变量
        if (flag) {
            myNumber = 0;
        }
    }
}