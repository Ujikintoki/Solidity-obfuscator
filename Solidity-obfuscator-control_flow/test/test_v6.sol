// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract TestObfuscation {
    address public contractOwner;
    uint256 private totalCounter = 0;

    struct UserData {
        uint256 balance;
        bool isActive;
        string username;
    }

    mapping(address => UserData) private userRecords;

    event ValueUpdated(address indexed userAddress, uint256 newValue);

    modifier onlyOwner() {
        require(msg.sender == contractOwner, "Only owner can call this function.");
        _;
    }

    constructor() public {
        contractOwner = msg.sender;
    }

    function updateValue(uint256 _newValue, uint256 _factor) public returns (bool) {
        if (_factor == 0) {
            totalCounter += _newValue;
            return false;
        } else if (_newValue > 100) {
            totalCounter += _newValue * _factor;
        } else {
            totalCounter = totalCounter + 1;
        }

        emit ValueUpdated(msg.sender, totalCounter);

        return true;
    }

    function initializeUsers(address[] memory userList) public onlyOwner {
        for (uint256 i = 0; i < userList.length; i++) {
            address userAddress = userList[i];

            userRecords[userAddress] = UserData({
                balance: 1000,
                isActive: true,
                username: "User"
            });
        }
    }

    function calculateResult(uint256 x, uint256 y) public pure returns (uint256) {
        uint256 result = 0;
        
        if (x > 50 && y < 20) {
            result = x + y;
        } else if (x <= 50) {
            result = x * 2;
        } else {
            result = y * 3;
        }
        
        return result;
    }
}

