pragma solidity 0.6.2;

contract Foo {
	                      
	                                 
	                 
	                 
	                          

	constructor() public{
		(s2c.b3, s2c.b4) = returnTrue();
		//b4 = returnTrue();
	}

	function returnTrue() internal pure returns(bool, bool){
		return (true && true, true);
	}

	function ifState() view external returns(uint256){
		return s2c.number;
	}

	function whileState() external pure returns(bool){
		bool b5 = true;
		bool b6 = false;
		return b5 || b6;
	}
	struct scalar2Vector {
		uint256 number;
		bool b4;
		bool b3;
		bool b2;
		bool b1;
	}
	scalar2Vector s2c = scalar2Vector( 0, false, false,  false || false,  true);
}
