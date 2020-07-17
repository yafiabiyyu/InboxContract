pragma solidity 0.5.6;

contract Inbox{

    string public message;

    constructor(string memory InitialMessage) public {
        message = InitialMessage;
    }

    function SetMessage(string memory _SetMessage) public {
        message = _SetMessage;
    }

    function GetMessage() public view returns(string memory) {
        return message;
    }
}