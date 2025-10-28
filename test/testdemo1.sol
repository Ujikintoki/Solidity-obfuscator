// simple .sol test
pragma solidity ^0.8.0;
contract Test {
    uint256 public x;
    function setX(uint256 _x) public {
        x = _x;
    }
}