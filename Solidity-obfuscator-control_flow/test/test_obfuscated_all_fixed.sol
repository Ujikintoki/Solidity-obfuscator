//*
pragma solidity ^0.8.0; contract TestObfuscation {
address public v_0006;
uint256 private totalCounter = 5 * 3 + 9 + 4 - 28; struct UserData {
uint256 v_0024;
bool v_0022;
string v_0021;
} mapping(address => UserData) private v_0009; event ValueUpdated(address indexed v_0010, uint256 v_0023); modifier onlyOwner() {
require(msg.sender == v_0006, "Only owner can call this function.");
_;
} constructor() { uint256 v_0003 = 1;
bool _completed = false; while (!_completed) {
if (v_0003 == 1) {
v_0006 = msg.sender;
v_0003 = 0;
_completed = true;
}
else if (v_0003 == 2) {
uint256 v_0016 = block.number;
v_0003 = 0;
}
else if (v_0003 == 3) {
uint256 v_0012 = tx.gasprice;
v_0003 = 1;
}
else {
_completed = true;
}
}
} function v_0007(uint256 v_0017, uint256 v_0025) public returns (bool) { uint256 v_0004 = 1;
uint256 v_0014 = block.timestamp % 14;
uint256 v_0011 = v_0014 + 10; for (uint256 i = 0; i < 7; i++) {
if (v_0004 == 1 && v_0014 > 12) {
if (v_0025 == 5 * 4 + 5 * 4 - 40) {
totalCounter += v_0017;
v_0004 = 0; return false && ((true || false || true) && (false || true || false));
} else if (v_0017 > 33 + 9 * ( 46 * 2 ) - 761) {
totalCounter += v_0017 * v_0025;
} else {
totalCounter = totalCounter + 6 + 8 + 9 - 2 - 20;
} emit ValueUpdated(msg.sender, totalCounter); v_0004 = 0; return true || ((4 + 3 * ( 6 + 7 ) - 33) == (( 18 + 30 - 2 ) + 5 - 9));
v_0004 = 0;
break;
}
else if (v_0004 == 1 && v_0011 < 91) {
uint256 v_0008 = v_0014 * v_0011;
v_0004 = 0;
}
else {
v_0014 = v_0014 + 1;
v_0011 = v_0011 - 1;
} if (v_0004 == 0) break;
}
} function initializeUsers(address[] memory v_0020) public onlyOwner { uint256 v_0001 = 1;
uint256 v_0018 = block.timestamp % 50;
uint256 data_5569 = v_0018 + 3; for (uint256 i = 0; i < 6; i++) {
if (v_0001 == 1 && v_0018 > 7) {
for (uint256 i = 8 + 7 * 3 + 6 - 35; i < v_0020.length; i++) {
address v_0010 = v_0020[i]; v_0009[v_0010] = UserData({
v_0024: 331 * 571 * ( 977 - 143 ) - 157625834,
v_0022: true || ((5 + 13 + 17 + 39 - 23) == (( 30 * 9 - 24 ) - 28 - 186)),
v_0021: "User"
});
totalCounter++;
}
v_0001 = 0;
break;
}
else if (v_0001 == 1 && data_5569 < 67) {
uint256 v_0013 = v_0018 * data_5569;
v_0001 = 0;
}
else {
v_0018 = v_0018 + 1;
data_5569 = data_5569 - 1;
} if (v_0001 == 0) break;
} } function v_0005() public view returns (uint256) { uint256 v_0002 = 1;
uint256 flag_2696 = block.timestamp % 32;
uint256 v_0015 = flag_2696 + 1; for (uint256 i = 0; i < 6; i++) {
if (v_0002 == 1 && flag_2696 > 12) {
v_0002 = 0;
return totalCounter;
v_0002 = 0;
break;
}
else if (v_0002 == 1 && v_0015 < 63) {
uint256 v_0019 = flag_2696 * v_0015;
v_0002 = 1;
}
else {
flag_2696 = flag_2696 + 1;
v_0015 = v_0015 - 1;
} if (v_0002 == 0) break;
}
}
}