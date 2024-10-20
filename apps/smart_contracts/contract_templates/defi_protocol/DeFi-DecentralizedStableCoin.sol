// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DecentralizedStablecoin is ERC20 {
    IERC20 public collateralToken;
    uint256 public collateralizationRatio;

    mapping(address => uint256) public collateralDeposits;

    event StablecoinMinted(address indexed user, uint256 amount);
    event StablecoinBurned(address indexed user, uint256 amount);

    constructor(IERC20 _collateralToken, uint256 _collateralizationRatio)
        ERC20("Decentralized Stablecoin", "DUSD")
    {
        collateralToken = _collateralToken;
        collateralizationRatio = _collateralizationRatio;
    }

    function depositCollateral(uint256 amount) public {
        require(amount > 0, "Collateral amount must be greater than 0");

        collateralToken.transferFrom(msg.sender, address(this), amount);
        collateralDeposits[msg.sender] += amount;

        uint256 mintAmount = (amount * collateralizationRatio) / 100;
        _mint(msg.sender, mintAmount);

        emit StablecoinMinted(msg.sender, mintAmount);
    }

    function withdrawCollateral(uint256 stablecoinAmount) public {
        require(balanceOf(msg.sender) >= stablecoinAmount, "Insufficient stablecoin balance");

        uint256 collateralAmount = (stablecoinAmount * 100) / collateralizationRatio;
        require(collateralDeposits[msg.sender] >= collateralAmount, "Insufficient collateral");

        _burn(msg.sender, stablecoinAmount);
        collateralDeposits[msg.sender] -= collateralAmount;

        collateralToken.transfer(msg.sender, collateralAmount);

        emit StablecoinBurned(msg.sender, stablecoinAmount);
    }
}
