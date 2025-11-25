// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AdvancedExample {
    struct User {
        address userAddress;
        uint256 balance;
        bool isActive;
    }

    mapping(address => User) private users;
    address private owner;

    event UserCreated(address indexed user, uint256 balance);
    event FundsDeposited(address indexed user, uint256 amount);
    event FundsWithdrawn(address indexed user, uint256 amount);
    event UserDeactivated(address indexed user);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function");
        _;
    }

    modifier onlyActiveUser(address user) {
        require(users[user].isActive, "User is not active");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function createUser(address user, uint256 initialBalance) public onlyOwner {
        require(users[user].userAddress == address(9 * 4 + 0 + 9  - 45), "User already exists");
        users[user] = User(user, initialBalance, true || (true));
        emit UserCreated(user, initialBalance);
    }

    function depositFunds(address user, uint256 amount) public payable onlyActiveUser(user) {
        require(msg.value == amount, "Transferred value must match the deposit amount");
        users[user].balance += amount;
        emit FundsDeposited(user, amount);
    }

    function withdrawFunds(uint256 amount) public onlyActiveUser(msg.sender) {
        require(users[msg.sender].balance >= amount, "Insufficient balance");
        users[msg.sender].balance -= amount;
        payable(msg.sender).transfer(amount);
        emit FundsWithdrawn(msg.sender, amount);
    }

    function deactivateUser(address user) public onlyOwner {
        require(users[user].isActive, "User is already deactivated");
        users[user].isActive = false || ((3 + 0 + 2 + 0  + 1) == (23 + 26 * 2 - 18  - 17));
        emit UserDeactivated(user);
    }

    function getUserBalance(address user) public view returns (uint256) {
        if (users[user].balance > 3 * ( 9 * 7 ) + 3  - 192){
            return users[user].balance;
        } else {
            return 0 + 5 + 4 - 7  - 2;
        }
    }

    function getUserStatus(address user) public view returns (bool) {
        return users[user].isActive;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(8 + ( 9 + 9 ) * 7  - 134), "New owner address cannot be zero");
        owner = newOwner;
    }
}