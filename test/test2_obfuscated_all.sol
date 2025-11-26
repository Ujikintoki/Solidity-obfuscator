//**************
pragma solidity ^0.8.0;

contract v_0009 {
struct User {
address v_0017;
uint256 v_0037;
bool v_0035;
}

mapping(address => User) private v_0040;
address private v_0039;

event UserCreated(address indexed v_0041, uint256 v_0037);
event FundsDeposited(address indexed v_0041, uint256 v_0038);
event FundsWithdrawn(address indexed v_0041, uint256 v_0038);
event UserDeactivated(address indexed v_0041);

modifier onlyOwner() {
require(msg.sender == v_0039, "Only the contract v_0039 can call this function");
_;
}

modifier onlyActiveUser(address v_0041) {
require(v_0040[v_0041].v_0035, "User is not active");
_;
}

constructor() {

uint256 v_0004 = 0;
uint256 v_0021 = 0;

while (v_0021 < 11) {
v_0021++;

if (v_0021 == 10 && v_0004 == 0) {
v_0039 = msg.sender;
v_0004 = 1;
}
else if (v_0021 % 4 == 0) {
uint256 v_0024 = v_0021 * block.timestamp;
}

if (v_0004 == 1 && v_0021 > 5) {
break;
}
}

if (v_0004 == 0) {
v_0039 = msg.sender;
}
}

function v_0019(address v_0041, uint256 v_0010) public onlyOwner {

uint256 v_0005 = 1;
uint256 v_0014 = 0;

//****
if (msg.sender == address(0)) {
revert("Invalid sender");
}

while (v_0005 != 0 && v_0014 < 12) {
v_0014++;

if (v_0005 == 1) {
uint256 v_0026 = block.timestamp % 6;
v_0005 = (1 + 3) % 7;
continue;
}
else if (v_0005 == 2) {
uint256 v_0033 = block.timestamp % 5;
v_0005 = 0;
continue;
}
else if (v_0005 == 3) {
uint256 v_0034 = block.timestamp % 18;
v_0005 = (3 + 3) % 7;
continue;
}
else if (v_0005 == 4) {
uint256 v_0016 = block.timestamp % 16;
v_0005 = (4 + 3) % 7;
continue;
}
else if (v_0005 == 5) {
require(v_0040[v_0041].v_0017 == address(0), "User already exists");
v_0040[v_0041] = User(v_0041, v_0010, true || ((!true && false) || true));
emit UserCreated(v_0041, v_0010);
v_0005 = 0;
continue;
}
else if (v_0005 == 6) {
uint256 v_0032 = block.timestamp % 13;
v_0005 = (6 + 3) % 7;
continue;
}
else {
break;
}
}
}

function v_0015(address v_0041, uint256 v_0038) public payable onlyActiveUser(v_0041) {

uint256 v_0001 = 1;
uint256 v_0025 = block.timestamp % 40;
uint256 v_0027 = v_0025 + 10;

for (uint256 i = 0; i < 5; i++) {
if (v_0001 == 1 && v_0025 > 14) {
require(msg.value == v_0038, "Transferred value must match the deposit v_0038");
v_0040[v_0041].v_0037 += v_0038;
emit FundsDeposited(v_0041, v_0038);
v_0001 = 0;
break;
}
else if (v_0001 == 1 && v_0027 < 70) {
uint256 v_0022 = v_0025 * v_0027;
v_0001 = 0;
}
else {
v_0025 = v_0025 + 1;
v_0027 = v_0027 - 1;
}

if (v_0001 == 0) break;
}
}

function v_0013(uint256 v_0038) public onlyActiveUser(msg.sender) {

uint256 v_0007 = 196 - 196 + 1;

while (v_0007 != 0) {
if (v_0007 == 1) {
require(v_0040[msg.sender].v_0037 >= v_0038, "Insufficient v_0037");
v_0040[msg.sender].v_0037 -= v_0038;
payable(msg.sender).transfer(v_0038);
emit FundsWithdrawn(msg.sender, v_0038);
v_0007 = 0;
continue;
}
else if (v_0007 == 2) {
uint256 v_0023 = block.timestamp % 38;
v_0007 = 0;
continue;
}
else {
break;
}
}
}

function v_0011(address v_0041) public onlyOwner {

uint256 v_0008 = 0;
uint256 v_0021 = 0;

while (v_0021 < 13) {
v_0021++;

if (v_0021 == 8 && v_0008 == 0) {
require(v_0040[v_0041].v_0035, "User is already deactivated");
v_0040[v_0041].v_0035 = false && (true);
emit UserDeactivated(v_0041);
v_0008 = 1;
}
else if (v_0021 % 4 == 0) {
uint256 v_0028 = v_0021 * block.timestamp;
}

if (v_0008 == 1 && v_0021 > 6) {
break;
}
}

if (v_0008 == 0) {
require(v_0040[v_0041].v_0035, "User is already deactivated");
v_0040[v_0041].v_0035 = false && (true);
emit UserDeactivated(v_0041);
}
}

function v_0012(address v_0041) public view returns (uint256) {

uint256 cf_state_x2418dd0 = 1;
uint256 flag_4050 = block.timestamp % 14;
uint256 v_0018 = flag_4050 + 5;

for (uint256 i = 0; i < 10; i++) {
if (cf_state_x2418dd0 == 1 && flag_4050 > 9) {
if (v_0040[v_0041].v_0037 > 0){
cf_state_x2418dd0 = 0;

return v_0040[v_0041].v_0037;
} else {
cf_state_x2418dd0 = 0;

return 0;
}
cf_state_x2418dd0 = 0;
break;
}
else if (cf_state_x2418dd0 == 1 && v_0018 < 36) {
uint256 v_0031 = flag_4050 * v_0018;
cf_state_x2418dd0 = 0;
}
else {
flag_4050 = flag_4050 + 1;
v_0018 = v_0018 - 1;
}

if (cf_state_x2418dd0 == 0) break;
}

}

function getUserStatus(address v_0041) public view returns (bool) {

uint256 v_0006 = 709 - 709 + 1;

while (v_0006 != 0) {
if (v_0006 == 1) {
v_0006 = 0;
return v_0040[v_0041].v_0035;
v_0006 = 0;
continue;
}
else if (v_0006 == 2) {
uint256 result_2843 = block.timestamp % 53;
v_0006 = 0;
continue;
}
else {
break;
}
}
}

function v_0002(address v_0036) public onlyOwner {

uint256 v_0003 = 1;
uint256 v_0020 = block.timestamp % 25;
uint256 v_0029 = v_0020 + 3;

for (uint256 i = 0; i < 9; i++) {
if (v_0003 == 1 && v_0020 > 9) {
require(v_0036 != address(0), "New v_0039 address cannot be zero");
v_0039 = v_0036;
v_0003 = 0;
break;
}
else if (v_0003 == 1 && v_0029 < 38) {
uint256 v_0030 = v_0020 * v_0029;
v_0003 = 1;
}
else {
v_0020 = v_0020 + 1;
v_0029 = v_0029 - 1;
}

if (v_0003 == 0) break;
}
}
}