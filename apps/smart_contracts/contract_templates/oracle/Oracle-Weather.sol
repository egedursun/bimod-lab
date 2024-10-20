// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WeatherOracle {
    address public admin;
    mapping(address => bool) public trustedSources;
    uint256 public latestTemperature;
    uint256 public latestHumidity;

    event WeatherUpdated(uint256 temperature, uint256 humidity);

    constructor() {
        admin = msg.sender;
    }

    function addTrustedSource(address source) public {
        require(msg.sender == admin, "Only admin can add sources");
        trustedSources[source] = true;
    }

    function removeTrustedSource(address source) public {
        require(msg.sender == admin, "Only admin can remove sources");
        trustedSources[source] = false;
    }

    function updateWeather(uint256 temperature, uint256 humidity) public {
        require(trustedSources[msg.sender], "Not a trusted source");

        latestTemperature = temperature;
        latestHumidity = humidity;

        emit WeatherUpdated(temperature, humidity);
    }

    function getWeatherData() public view returns (uint256, uint256) {
        return (latestTemperature, latestHumidity);
    }
}
