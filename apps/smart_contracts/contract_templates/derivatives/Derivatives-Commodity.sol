// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CommodityToken is ERC20 {
    address public commodityIssuer;
    uint256 public commodityPricePerUnit;

    event CommodityMinted(address indexed issuer, uint256 amount, uint256 pricePerUnit);

    constructor(uint256 _initialSupply, uint256 _commodityPricePerUnit) ERC20("CommodityToken", "COM") {
        _mint(msg.sender, _initialSupply);
        commodityIssuer = msg.sender;
        commodityPricePerUnit = _commodityPricePerUnit;
    }

    function mintCommodityTokens(uint256 amount, uint256 pricePerUnit) public {
        require(msg.sender == commodityIssuer, "Only issuer can mint tokens");

        _mint(msg.sender, amount);
        commodityPricePerUnit = pricePerUnit;

        emit CommodityMinted(msg.sender, amount, pricePerUnit);
    }

    function redeemTokens(uint256 amount) public {
        _burn(msg.sender, amount);
        payable(msg.sender).transfer(amount * commodityPricePerUnit);
    }
}
