// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RealEstateCrowdfunding {
    address public propertyOwner;
    uint256 public fundingGoal;
    uint256 public totalFundsRaised;
    bool public fundingClosed;

    struct Investor {
        uint256 contribution;
        uint256 tokensReceived;
    }

    mapping(address => Investor) public investors;
    address[] public investorList;

    event InvestmentMade(address indexed investor, uint256 amount);
    event PropertyPurchased();

    constructor(uint256 _fundingGoal) {
        propertyOwner = msg.sender;
        fundingGoal = _fundingGoal;
        fundingClosed = false;
    }

    function invest() public payable {
        require(!fundingClosed, "Funding is closed");
        require(msg.value > 0, "Investment must be greater than 0");

        investors[msg.sender].contribution += msg.value;
        investorList.push(msg.sender);
        totalFundsRaised += msg.value;

        // Assign proportional tokens based on investment (using a token contract, not shown here)
        // For example: investors[msg.sender].tokensReceived = calculateTokens(msg.value);

        emit InvestmentMade(msg.sender, msg.value);

        if (totalFundsRaised >= fundingGoal) {
            fundingClosed = true;
            emit PropertyPurchased();
        }
    }

    function getInvestorDetails(address investor) public view returns (uint256 contribution, uint256 tokensReceived) {
        return (investors[investor].contribution, investors[investor].tokensReceived);
    }
}
