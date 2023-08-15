// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Domain {
    string public domain;
    string public description;
    uint256 public expiryDate;

    constructor(string memory _domain, string memory _description, uint256 _expiryDate) {
        domain = _domain;
        description = _description;
        expiryDate = _expiryDate;
    }

    function getDomainInfo() public view returns (string memory, string memory, uint256) {
        return (domain, description, expiryDate);
    }

    function setDomainInfo(string memory _domain, string memory _description, uint256 _expiryDate) public {
        domain = _domain;
        description = _description;
        expiryDate = _expiryDate;
    }
}