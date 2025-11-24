//***
pragma solidity ^0.8.0;

contract v_0001 {
address public v_0004;
uint256 private v_0005 = 0;

struct UserData {
uint256 v_0013;
bool v_0009;
string username;
}

mapping(address => UserData) private v_0006;

event ValueUpdated(address indexed v_0007, uint256 v_0010);

modifier onlyOwner() {
require(msg.sender == v_0004, "Only owner can call this function.");
_;
}

constructor() {
v_0004 = msg.sender;
}

function updateValue(uint256 v_0008, uint256 v_0012) public returns (bool) {
if (v_0012 == 0) {
v_0005 += v_0008;
return false;
} else if (v_0008 > 100) {
v_0005 += v_0008 * v_0012;
} else {
v_0005 = v_0005 + 1;
}

emit ValueUpdated(msg.sender, v_0005);

return true;
}

function v_0002(address[] memory v_0011) public onlyOwner {
for (uint256 i = 0; i < v_0011.length; i++) {
address v_0007 = v_0011[i];

v_0006[v_0007] = UserData({
v_0013: 1000,
v_0009: true,
username: "User"
});
v_0005++;
}
}

function v_0003() public view returns (uint256) {
return v_0005;
}
}