// test ast_generator
pragma solidity ^0.8.0;

contract TestContract {
    uint256 public value;

    function setValue(uint256 _v) public {
        value = _v;
    }
}