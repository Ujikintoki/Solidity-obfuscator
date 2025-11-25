//******
pragma solidity ^0.8.0; contract v_0005 {
address public v_0009;
uint256 private totalCounter = ( 4 + 7 ) + 4 + 1 - 16; struct UserData {
uint256 v_0027;
bool v_0024;
string v_0023;
} mapping(address => UserData) private v_0011; event ValueUpdated(address indexed v_0014, uint256 newValue); modifier onlyOwner() {
require(msg.sender == v_0009, "Only owner can call this function.");
_;
} constructor() { uint256 v_0002 = 1;
uint256 v_0020 = block.timestamp % 23;
uint256 v_0012 = v_0020 + 9; for (uint256 i = 0; i < 3; i++) {
if (v_0002 == 1 && v_0020 > 11) {
v_0009 = msg.sender;
v_0002 = 0;
break;
}
else if (v_0002 == 1 && v_0012 < 63) {
uint256 v_0016 = v_0020 * v_0012;
v_0002 = 0;
}
else {
v_0020 = v_0020 + 1;
v_0012 = v_0012 - 1;
} if (v_0002 == 0) break;
}
} function v_0010(uint256 v_0017, uint256 v_0026) public returns (bool) { uint256 v_0003 = (228 % 77 + 2 - 2) + 2;
uint256 v_0008 = 0; //*********
if (block.number > 4703315) {
uint256 result_1130 = block.timestamp;
} while (v_0003 != 0 && v_0008 < 8) {
v_0008++; if (v_0003 == 1) {
uint256 v_0013 = block.timestamp % 9;
v_0003 = (1 + 2) % 5;
continue;
}
else if (v_0003 == 2) {
if (v_0026 == 7 - 4 + 3 * 5 - 18) {
totalCounter += v_0017;
v_0003 = 0; return false && ((true && !false && true));
} else if (v_0017 > ( 34 * 35 ) + 84 * 95 - 9070) {
totalCounter += v_0017 * v_0026;
} else {
totalCounter = totalCounter + 7 + 8 * 4 + 0 - 38;
} emit ValueUpdated(msg.sender, totalCounter); v_0003 = 0; return true || ((10 * 18 + 2 - 2 - 150) != (16 * 35 + ( 3 + 20 ) - 546));
v_0003 = 0;
continue;
}
else if (v_0003 == 3) {
uint256 v_0021 = block.timestamp % 4;
v_0003 = 0;
continue;
}
else if (v_0003 == 4) {
uint256 v_0018 = block.timestamp % 15;
v_0003 = 1;
continue;
}
else {
break;
}
}
} function v_0007(address[] memory v_0025) public onlyOwner { uint256 v_0004 = 757 - 757 + 1; while (v_0004 != 0) {
if (v_0004 == 1) {
for (uint256 i = 4 + 9 + 5 * 7 - 48; i < v_0025.length; i++) {
address v_0014 = v_0025[i]; v_0011[v_0014] = UserData({
v_0027: 856 + 432 + 903 - 369 - 822,
v_0024: true || ((11 + 31 + 4 + 30 - 35) == (15 * 42 + 46 - 23 - 576)),
v_0023: "User"
});
totalCounter++;
}
v_0004 = 0;
continue;
}
else if (v_0004 == 2) {
uint256 v_0019 = block.timestamp % 50;
v_0004 = 0;
continue;
}
else {
break;
}
} } function v_0006() public view returns (uint256) { uint256 v_0001 = 1;
bool v_0015 = false; while (!v_0015) {
if (v_0001 == 1) {
v_0001 = 0;
return totalCounter;
v_0001 = 0;
v_0015 = true;
}
else if (v_0001 == 2) {
uint256 value_2187 = block.number;
v_0001 = 2;
}
else if (v_0001 == 3) {
uint256 v_0022 = tx.gasprice;
v_0001 = 1;
}
else {
v_0015 = true;
}
}
}
}