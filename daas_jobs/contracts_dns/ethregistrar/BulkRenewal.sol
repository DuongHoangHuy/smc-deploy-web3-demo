//SPDX-License-Identifier: MIT
pragma solidity ~0.8.17;

import "../registry/ENS.sol";
import "./ETHRegistrarController.sol";
import "./IETHRegistrarController.sol";
import "../resolvers/Resolver.sol";
import "./IBulkRenewal.sol";
import "./IPriceOracle.sol";

import "../@openzeppelin/contracts/utils/introspection/IERC165.sol";

contract BulkRenewal is IBulkRenewal {
    bytes32 private constant ETH_NAMEHASH =
        0x74df4ab2564a9f9bb6d4b6b77bf4fc02ac80f07bd9e1776d3967578b3fc36be4;

    ENS public immutable ens;

    constructor(ENS _ens) {
        ens = _ens;
    }

    function getController() internal view returns (ETHRegistrarController) {
        Resolver r = Resolver(ens.resolver(ETH_NAMEHASH));
        return
            ETHRegistrarController(
                r.interfaceImplementer(
                    ETH_NAMEHASH,
                    type(IETHRegistrarController).interfaceId
                )
            );
    }

    function rentPrice(
        string[] calldata names,
        uint256 duration,
        address user
    ) external view override returns (uint256 total) {
        ETHRegistrarController controller = getController();
        uint256 length = names.length;
        for (uint256 i = 0; i < length; ) {
            IPriceOracle.Price memory price = controller.rentPrice(
                names[i],
                duration,
                user
            );
            unchecked {
                ++i;
                total += (price.base + price.premium);
            }
        }
    }

    function renewAll(
        string[] calldata names,
        uint256 duration
    ) external payable override {
        ETHRegistrarController controller = getController();
        uint256 length = names.length;
        uint256 total;
        for (uint256 i = 0; i < length; ) {
            IPriceOracle.Price memory price = controller.rentPrice(
                names[i],
                duration,
                msg.sender
            );
            uint256 totalPrice = price.base + price.premium;
            controller.renew{value: totalPrice}(names[i], duration);
            unchecked {
                ++i;
                total += totalPrice;
            }
        }
        // Send any excess funds back
        payable(msg.sender).transfer(address(this).balance);
    }

    function supportsInterface(
        bytes4 interfaceID
    ) external pure returns (bool) {
        return
            interfaceID == type(IERC165).interfaceId ||
            interfaceID == type(IBulkRenewal).interfaceId;
    }
}
