#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-19 22:24:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:24:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


BLOCKCHAIN_TYPE = [
    ('ethereum', 'Ethereum'),
]

DEFAULT_WEI_UNIT = 'ether'


class BlockchainTypesNames:
    ETHEREUM = 'ethereum'

    @staticmethod
    def as_list():
        return [BlockchainTypesNames.ETHEREUM]


SMART_CONTRACT_CATEGORIES = [
    ('token', 'Token Contract'),
    ('nft', 'NFT Contract'),
    ('escrow', 'Escrow Contract'),
    ('dao', 'DAO Contract'),
    ('crowdsale', 'Crowdsale Contract'),
    ('governance', 'Governance Contract'),
    ('staking', 'Staking Contract'),
    ('vesting', 'Vesting Contract'),
    ('liquidity_pool', 'Liquidity Pool Contract'),
    ('oracle', 'Oracle Contract'),
    ('marketplace', 'Marketplace Contract'),
    ('real_estate', 'Real Estate Tokenization Contract'),
    ('supply_chain', 'Supply Chain Contract'),
    ('insurance', 'Insurance Contract'),
    ('identity', 'Identity Verification Contract'),
    ('lottery', 'Lottery Contract'),
    ('royalties', 'Royalties Contract'),
    ('defi_protocol', 'DeFi Protocol Contract'),
    ('lending_borrowing', 'Lending & Borrowing Contract'),
    ('derivatives', 'Derivatives Contract'),
    ('voting', 'Voting Contract'),
]


class SmartContractCategoriesNames:
    TOKEN = 'token'
    NFT = 'nft'
    ESCROW = 'escrow'
    DAO = 'dao'
    CROWDSALE = 'crowdsale'
    GOVERNANCE = 'governance'
    STAKING = 'staking'
    VESTING = 'vesting'
    LIQUIDITY_POOL = 'liquidity_pool'
    ORACLE = 'oracle'
    MARKETPLACE = 'marketplace'
    REAL_ESTATE = 'real_estate'
    SUPPLY_CHAIN = 'supply_chain'
    INSURANCE = 'insurance'
    IDENTITY = 'identity'
    LOTTERY = 'lottery'
    ROYALTIES = 'royalties'
    DEFI_PROTOCOL = 'defi_protocol'
    LENDING_BORROWING = 'lending_borrowing'
    DERIVATIVES = 'derivatives'
    VOTING = 'voting'

    @staticmethod
    def as_list():
        return [
            SmartContractCategoriesNames.TOKEN,
            SmartContractCategoriesNames.NFT,
            SmartContractCategoriesNames.ESCROW,
            SmartContractCategoriesNames.DAO,
            SmartContractCategoriesNames.CROWDSALE,
            SmartContractCategoriesNames.GOVERNANCE,
            SmartContractCategoriesNames.STAKING,
            SmartContractCategoriesNames.VESTING,
            SmartContractCategoriesNames.LIQUIDITY_POOL,
            SmartContractCategoriesNames.ORACLE,
            SmartContractCategoriesNames.MARKETPLACE,
            SmartContractCategoriesNames.REAL_ESTATE,
            SmartContractCategoriesNames.SUPPLY_CHAIN,
            SmartContractCategoriesNames.INSURANCE,
            SmartContractCategoriesNames.IDENTITY,
            SmartContractCategoriesNames.LOTTERY,
            SmartContractCategoriesNames.ROYALTIES,
            SmartContractCategoriesNames.DEFI_PROTOCOL,
            SmartContractCategoriesNames.LENDING_BORROWING,
            SmartContractCategoriesNames.DERIVATIVES,
            SmartContractCategoriesNames.VOTING,
        ]


SMART_CONTRACT_TEMPLATE_CHOICES = [
    # Crowdsale Contract Templates
    ('Crowdsale-Basic', 'Crowdsale-Basic'),
    ('Crowdsale-Refundable', 'Crowdsale-Refundable'),
    ('Crowdsale-Capped', 'Crowdsale-Capped'),
    ('Crowdsale-Timed', 'Crowdsale-Timed'),
    ('Crowdsale-Whitelisted', 'Crowdsale-Whitelisted'),
    ('Crowdsale-RefundableWithGoal', 'Crowdsale-RefundableWithGoal'),
    ('Crowdsale-TieredPricing', 'Crowdsale-TieredPricing'),
    ('Crowdsale-TokenDistribution', 'Crowdsale-TokenDistribution'),
    ('Crowdsale-Vesting', 'Crowdsale-Vesting'),
    ###
    ('Crowdsale-Custom', 'Crowdsale-Custom'),

    # DAO Contract Templates
    ('DAO-ERC20TokenVoting', 'DAO-ERC20TokenVoting'),
    ('DAO-MultiSignature', 'DAO-MultiSignature'),
    ('DAO-TokenCuratedRegistry', 'DAO-TokenCuratedRegistry'),
    ('DAO-TreasuryManagement', 'DAO-TreasuryManagement'),
    ('DAO-TreasuryTimelocked', 'DAO-TreasuryTimelocked'),
    ('DAO-VotingBasic', 'DAO-VotingBasic'),
    ('DAO-VotingDelegated', 'DAO-VotingDelegated'),
    ('DAO-VotingQuadratic', 'DAO-VotingQuadratic'),
    ('DAO-VotingOffChain', 'DAO-VotingOffChain'),
    ('DAO-VotingQuorumMajority', 'DAO-VotingQuorumMajority'),
    ###
    ('DAO-Custom', 'DAO-Custom'),

    # DeFi Protocol Contract Templates
    ('DeFi-AutoMarketMaker', 'DeFi-AutoMarketMaker'),
    ('DeFi-FlashLoan', 'DeFi-FlashLoan'),
    ('DeFi-Staking', 'DeFi-Staking'),
    ('DeFi-LendingBorrowing', 'DeFi-LendingBorrowing'),
    ('DeFi-DecentralizedStableCoin', 'DeFi-DecentralizedStableCoin'),
    ('DeFi-Dex', 'DeFi-Dex'),
    ('Defi-InsurancePool', 'Defi-InsurancePool'),
    ('DeFi-YieldFarming', 'DeFi-YieldFarming'),
    ###
    ('DeFi-Custom', 'DeFi-Custom'),

    # Derivatives Contract Templates
    ('Derivatives-Options', 'Derivatives-Options'),
    ('Derivatives-Futures', 'Derivatives-Futures'),
    ('Derivatives-CreditDefaultSwap', 'Derivatives-CreditDefaultSwap'),
    ('Derivatives-BinaryOptions', 'Derivatives-BinaryOptions'),
    ('Derivatives-Commodity', 'Derivatives-Commodity'),
    ('Derivatives-InterestRateSwap', 'Derivatives-InterestRateSwap'),
    ('Derivatives-LeveragedToken', 'Derivatives-LeveragedToken'),
    ('Derivatives-VolatilityIndex', 'Derivatives-VolatilityIndex'),
    ###
    ('Derivatives-Custom', 'Derivatives-Custom'),

    # Escrow Contract Templates
    ('Escrow-Basic', 'Escrow-Basic'),
    ('Escrow-Conditional', 'Escrow-Conditional'),
    ('Escrow-DisputeResolution', 'Escrow-DisputeResolution'),
    ('Escrow-MultiSignature', 'Escrow-MultiSignature'),
    ('Escrow-ProgressiveRelease', 'Escrow-ProgressiveRelease'),
    ('Escrow-Refund', 'Escrow-Refund'),
    ('Escrow-Timelock', 'Escrow-Timelock'),
    ('Escrow-Subscription', 'Escrow-Subscription'),
    ('Escrow-Milestone', 'Escrow-Milestone'),
    ###
    ('Escrow-Custom', 'Escrow-Custom'),

    # Governance Contract Templates
    ('Governance-MultipleProposal', 'Governance-MultipleProposal'),
    ('Governance-Timelocked', 'Governance-Timelocked'),
    ('Governance-Vesting', 'Governance-Vesting'),
    ('Governance-VotingBonded', 'Governance-VotingBonded'),
    ('Governance-VotingDelegated', 'Governance-VotingDelegated'),
    ('Governance-VotingDynamic', 'Governance-VotingDynamic'),
    ('Governance-VotingOffchain', 'Governance-VotingOffchain'),
    ('Governance-VotingOnchain', 'Governance-VotingOnchain'),
    ('Governance-VotingQuadratic', 'Governance-VotingQuadratic'),
    ('Governance-VotingQuorumMajority', 'Governance-VotingQuorumMajority'),
    ###
    ('Governance-Custom', 'Governance-Custom'),

    # Identity Verification Contract Templates
    ('ID-AccessControl', 'ID-AccessControl'),
    ('ID-CredentialIssuance', 'ID-CredentialIssuance'),
    ('ID-DecentralizedID', 'ID-DecentralizedID'),
    ('ID-DecentralizedIdentityAggregator', 'ID-DecentralizedIdentityAggregator'),
    ('ID-DecentralizedReputationSlashing', 'ID-DecentralizedReputationSlashing'),
    ('ID-IDBasedVoting', 'ID-IDBasedVoting'),
    ('ID-MultiSignatureIDVerification', 'ID-MultiSignatureIDVerification'),
    ('ID-ReputationSystem', 'ID-ReputationSystem'),
    ('ID-SoulboundTokens', 'ID-SoulboundTokens'),
    ('ID-ZeroKnowledgeProof', 'ID-ZeroKnowledgeProof'),
    ###
    ('ID-Custom', 'ID-Custom'),

    # Insurance Contract Templates
    ('Insurance-ClaimAndDisputeResolution', 'Insurance-ClaimAndDisputeResolution'),
    ('Insurance-DecentralizedReinsurance', 'Insurance-DecentralizedReinsurance'),
    ('Insurance-DecentralizedRiskPool', 'Insurance-DecentralizedRiskPool'),
    ('Insurance-Group', 'Insurance-Group'),
    ('Insurance-Micro', 'Insurance-Micro'),
    ('Insurance-Mutual', 'Insurance-Mutual'),
    ('Insurance-Parametric', 'Insurance-Parametric'),
    ('Insurance-PremiumPaymentAndRefund', 'Insurance-PremiumPaymentAndRefund'),
    ('Insurance-StakingForUnderwriting', 'Insurance-StakingForUnderwriting'),
    ('Insurance-Tokenized', 'Insurance-Tokenized'),
    ###
    ('Insurance-Custom', 'Insurance-Custom'),

    # Lending & Borrowing Contract Templates
    ('Lending-CollateralSwap', 'Lending-CollateralSwap'),
    ('Lending-DynamicInterestRateLoan', 'Lending-DynamicInterestRateLoan'),
    ('Lending-FlashLoan', 'Lending-FlashLoan'),
    ('Lending-InterestBearingToken', 'Lending-InterestBearingToken'),
    ('Lending-OverCollateralizedLoan', 'Lending-OverCollateralizedLoan'),
    ('Lending-P2PMarket', 'Lending-P2PMarket'),
    ('Lending-RevolvingCreditLine', 'Lending-RevolvingCreditLine'),
    ('Lending-Secured', 'Lending-Secured'),
    ###
    ('Lending-Custom', 'Lending-Custom'),

    # Liquidity Pool Contract Templates
    ('LiquidityPool-AutoBalancing', 'LiquidityPool-AutoBalancing'),
    ('LiquidityPool-Basic', 'LiquidityPool-Basic'),
    ('LiquidityPool-DynamicFee', 'LiquidityPool-DynamicFee'),
    ('LiquidityPool-FlashLoan', 'LiquidityPool-FlashLoan'),
    ('LiquidityPool-ImpermanentLossProtection', 'LiquidityPool-ImpermanentLossProtection'),
    ('LiquidityPool-Incentivized', 'LiquidityPool-Incentivized'),
    ('LiquidityPool-MultiToken', 'LiquidityPool-MultiToken'),
    ('LiquidityPool-Timelocked', 'LiquidityPool-Timelocked'),
    ('LiquidityPool-YieldFarming', 'LiquidityPool-YieldFarming'),
    ###
    ('LiquidityPool-Custom', 'LiquidityPool-Custom'),

    # Lottery Contract Templates
    ('Lottery-ChainlinkVRF', 'Lottery-ChainlinkVRF'),
    ('Lottery-CommunityDriven', 'Lottery-CommunityDriven'),
    ('Lottery-DecentralizedPool', 'Lottery-DecentralizedPool'),
    ('Lottery-DeflationaryToken', 'Lottery-DeflationaryToken'),
    ('Lottery-MultiWinner', 'Lottery-MultiWinner'),
    ('Lottery-RaffleBased', 'Lottery-RaffleBased'),
    ('Lottery-Simple', 'Lottery-Simple'),
    ('Lottery-SubscriptionBased', 'Lottery-SubscriptionBased'),
    ###
    ('Lottery-Custom', 'Lottery-Custom'),

    # Marketplace Contract Templates
    ('Marketplace-AuctionBased', 'Marketplace-AuctionBased'),
    ('Marketplace-DecentralizedRental', 'Marketplace-DecentralizedRental'),
    ('Marketplace-ERC20Token', 'Marketplace-ERC20Token'),
    ('Marketplace-NFTRoyaltyBased', 'Marketplace-NFTRoyaltyBased'),
    ('Marketplace-NFTSimple', 'Marketplace-NFTSimple'),
    ('Marketplace-P2PEscrow', 'Marketplace-P2PEscrow'),
    ('Marketplace-RevenueSharing', 'Marketplace-RevenueSharing'),
    ('Marketplace-Service', 'Marketplace-Service'),
    ('Marketplace-Whitelist', 'Marketplace-Whitelist'),
    ###
    ('Marketplace-Custom', 'Marketplace-Custom'),

    # NFT Contract Templates
    ('ERC-721', 'ERC-721'),
    ('ERC-721-BatchMining', 'ERC-721-BatchMining'),
    ('ERC-721-DutchAuction', 'ERC-721-DutchAuction'),
    ('ERC-721-Enumerable', 'ERC-721-Enumerable'),
    ('ERC-721-Fractionalization', 'ERC-721-Fractionalization'),
    ('ERC-721-Metadata', 'ERC-721-Metadata'),
    ('ERC-721-Pausable', 'ERC-721-Pausable'),
    ('ERC-721-Rentable', 'ERC-721-Rentable'),
    ('ERC-721-Staking', 'ERC-721-Staking'),
    ('ERC-721-Wrapped', 'ERC-721-Wrapped'),
    ('ERC-721-MultiToken', 'ERC-721-MultiToken'),
    ('ERC-721-Royalty', 'ERC-721-Royalty'),
    ###
    ('NFT-Custom', 'NFT-Custom'),

    # Oracle Contract Templates
    ('Oracle-APIBased', 'Oracle-APIBased'),
    ('Oracle-CustomDataFeed', 'Oracle-CustomDataFeed'),
    ('Oracle-DataSignatureVerification', 'Oracle-DataSignatureVerification'),
    ('Oracle-Fallback', 'Oracle-Fallback'),
    ('Oracle-MultiSourceAggregation', 'Oracle-MultiSourceAggregation'),
    ('Oracle-Price', 'Oracle-Price'),
    ('Oracle-Randomness', 'Oracle-Randomness'),
    ('Oracle-TimebasedDataFeed', 'Oracle-TimebasedDataFeed'),
    ('Oracle-Weather', 'Oracle-Weather'),
    ###
    ('Oracle-Custom', 'Oracle-Custom'),

    # Real Estate Tokenization Contract Templates
    ('RealEstate-Crowdfunding', 'RealEstate-Crowdfunding'),
    ('RealEstate-DAO', 'RealEstate-DAO'),
    ('RealEstate-FractionalOwnership', 'RealEstate-FractionalOwnership'),
    ('RealEstate-Loan', 'RealEstate-Loan'),
    ('RealEstate-Marketplace', 'RealEstate-Marketplace'),
    ('RealEstate-PropertyAuction', 'RealEstate-PropertyAuction'),
    ('RealEstate-PropertyLeaseToOwn', 'RealEstate-PropertyLeaseToOwn'),
    ('RealEstate-PropertyTokenization', 'RealEstate-PropertyTokenization'),
    ('RealEstate-RentalAgreement', 'RealEstate-RentalAgreement'),
    ###
    ('RealEstate-Custom', 'RealEstate-Custom'),

    # Royalties Contract Templates
    ('Royalties-EscrowBasedPayment', 'Royalties-EscrowBasedPayment'),
    ('Royalties-LicenceBased', 'Royalties-LicenceBased'),
    ('Royalties-NFTRoyaltyDistribution', 'Royalties-NFTRoyaltyDistribution'),
    ('Royalties-PercentageBased', 'Royalties-PercentageBased'),
    ('Royalties-PerformanceBased', 'Royalties-PerformanceBased'),
    ('Royalties-Pool', 'Royalties-Pool'),
    ('Royalties-RealTimeSplitting', 'Royalties-RealTimeSplitting'),
    ('Royalties-Streaming', 'Royalties-Streaming'),
    ('Royalties-TieredStructure', 'Royalties-TieredStructure'),
    ###
    ('Royalties-Custom', 'Royalties-Custom'),

    # Staking Contract Templates
    ('Staking-AutoCompounding', 'Staking-AutoCompounding'),
    ('Staking-Basic', 'Staking-Basic'),
    ('Staking-EarlyWithdrawalPenalty', 'Staking-EarlyWithdrawalPenalty'),
    ('Staking-Liquidity', 'Staking-Liquidity'),
    ('Staking-MultiAsset', 'Staking-MultiAsset'),
    ('Staking-MultiTier', 'Staking-MultiTier'),
    ('Staking-Timelocked', 'Staking-Timelocked'),
    ('Staking-ToAccess', 'Staking-ToAccess'),
    ('Staking-TokenGovernance', 'Staking-TokenGovernance'),
    ('Staking-YieldFarming', 'Staking-YieldFarming'),
    ###
    ('Staking-Custom', 'Staking-Custom'),

    # Supply Chain Contract Templates
    ('SupplyChain-AssetTransfer', 'SupplyChain-AssetTransfer'),
    ('SupplyChain-AutomatedPayment', 'SupplyChain-AutomatedPayment'),
    ('SupplyChain-CertificationVerification', 'SupplyChain-CertificationVerification'),
    ('SupplyChain-Financing', 'SupplyChain-Financing'),
    ('SupplyChain-InventoryManagement', 'SupplyChain-InventoryManagement'),
    ('SupplyChain-MultiPartyCoordination', 'SupplyChain-MultiPartyCoordination'),
    ('SupplyChain-ProductTracking', 'SupplyChain-ProductTracking'),
    ('SupplyChain-ShipmentTracking', 'SupplyChain-ShipmentTracking'),
    ('SupplyChain-SupplierVerification', 'SupplyChain-SupplierVerification'),
    ###
    ('SupplyChain-Custom', 'SupplyChain-Custom'),

    # Token Contract Templates
    ('ERC-20', 'ERC-20'),
    ('ERC-20-Burnable', 'ERC-20-Burnable'),
    ('ERC-20-Capped', 'ERC-20-Capped'),
    ('ERC-20-Deflationary', 'ERC-20-Deflationary'),
    ('ERC-20-Mintable', 'ERC-20-Mintable'),
    ('ERC-20-Pausable', 'ERC-20-Pausable'),
    ('ERC-20-Snapshot', 'ERC-20-Snapshot'),
    ('ERC-20-Taxable', 'ERC-20-Taxable'),
    ('ERC-20-Vesting', 'ERC-20-Vesting'),
    ###
    ('ERC-20-Custom', 'ERC-20-Custom'),

    # Vesting Contract Templates
    ('Vesting-AdjustableTerms', 'Vesting-AdjustableTerms'),
    ('Vesting-Cliff', 'Vesting-Cliff'),
    ('Vesting-CustomSchedule', 'Vesting-CustomSchedule'),
    ('Vesting-Deferred', 'Vesting-Deferred'),
    ('Vesting-GradualRelease', 'Vesting-GradualRelease'),
    ('Vesting-MilestoneBased', 'Vesting-MilestoneBased'),
    ('Vesting-PerformanceBased', 'Vesting-PerformanceBased'),
    ('Vesting-TeamBased', 'Vesting-TeamBased'),
    ('Vesting-TimeBased', 'Vesting-TimeBased'),
    ('Vesting-WithRevocation', 'Vesting-WithRevocation'),
    ###
    ('Vesting-Custom', 'Vesting-Custom'),

    # Voting Contract Templates
    ('Voting-Anonymous', 'Voting-Anonymous'),
    ('Voting-Delegated', 'Voting-Delegated'),
    ('Voting-LiquidDemocracy', 'Voting-LiquidDemocracy'),
    ('Voting-MultiSignature', 'Voting-MultiSignature'),
    ('Voting-Quadratic', 'Voting-Quadratic'),
    ('Voting-Timelocked', 'Voting-Timelocked'),
    ('Voting-TimeWeighted', 'Voting-TimeWeighted'),
    ('Voting-TokenBased', 'Voting-TokenBased'),
    ('Voting-Weighted', 'Voting-Weighted'),
    ###
    ('Voting-Custom', 'Voting-Custom'),
]


class SmartContractTemplateNames:
    # Crowdsale Contract Templates
    CROWDSALE_BASIC = 'Crowdsale-Basic'
    CROWDSALE_REFUNDABLE = 'Crowdsale-Refundable'
    CROWDSALE_CAPPED = 'Crowdsale-Capped'
    CROWDSALE_TIMED = 'Crowdsale-Timed'
    CROWDSALE_WHITELISTED = 'Crowdsale-Whitelisted'
    CROWDSALE_REFUNDABLE_WITH_GOAL = 'Crowdsale-RefundableWithGoal'
    CROWDSALE_TIERED_PRICING = 'Crowdsale-TieredPricing'
    CROWDSALE_TOKEN_DISTRIBUTION = 'Crowdsale-TokenDistribution'
    CROWDSALE_VESTING = 'Crowdsale-Vesting'
    CROWDSALE_CUSTOM = 'Crowdsale-Custom'

    class CrowdSale:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.CROWDSALE_BASIC,
                SmartContractTemplateNames.CROWDSALE_REFUNDABLE,
                SmartContractTemplateNames.CROWDSALE_CAPPED,
                SmartContractTemplateNames.CROWDSALE_TIMED,
                SmartContractTemplateNames.CROWDSALE_WHITELISTED,
                SmartContractTemplateNames.CROWDSALE_REFUNDABLE_WITH_GOAL,
                SmartContractTemplateNames.CROWDSALE_TIERED_PRICING,
                SmartContractTemplateNames.CROWDSALE_TOKEN_DISTRIBUTION,
                SmartContractTemplateNames.CROWDSALE_VESTING,
                SmartContractTemplateNames.CROWDSALE_CUSTOM,
            ]

    # DAO Contract Templates
    DAO_ERC20_TOKEN_VOTING = 'DAO-ERC20TokenVoting'
    DAO_MULTI_SIGNATURE = 'DAO-MultiSignature'
    DAO_TOKEN_CURATED_REGISTRY = 'DAO-TokenCuratedRegistry'
    DAO_TREASURY_MANAGEMENT = 'DAO-TreasuryManagement'
    DAO_TREASURY_TIMELOCKED = 'DAO-TreasuryTimelocked'
    DAO_VOTING_BASIC = 'DAO-VotingBasic'
    DAO_VOTING_DELEGATED = 'DAO-VotingDelegated'
    DAO_VOTING_QUADRATIC = 'DAO-VotingQuadratic'
    DAO_VOTING_OFF_CHAIN = 'DAO-VotingOffChain'
    DAO_VOTING_QUORUM_MAJORITY = 'DAO-VotingQuorumMajority'
    DAO_CUSTOM = 'DAO-Custom'

    class DAO:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.DAO_ERC20_TOKEN_VOTING,
                SmartContractTemplateNames.DAO_MULTI_SIGNATURE,
                SmartContractTemplateNames.DAO_TOKEN_CURATED_REGISTRY,
                SmartContractTemplateNames.DAO_TREASURY_MANAGEMENT,
                SmartContractTemplateNames.DAO_TREASURY_TIMELOCKED,
                SmartContractTemplateNames.DAO_VOTING_BASIC,
                SmartContractTemplateNames.DAO_VOTING_DELEGATED,
                SmartContractTemplateNames.DAO_VOTING_QUADRATIC,
                SmartContractTemplateNames.DAO_VOTING_OFF_CHAIN,
                SmartContractTemplateNames.DAO_VOTING_QUORUM_MAJORITY,
                SmartContractTemplateNames.DAO_CUSTOM,
            ]

    # DeFi Protocol Contract Templates
    DEFI_AUTO_MARKET_MAKER = 'DeFi-AutoMarketMaker'
    DEFI_FLASH_LOAN = 'DeFi-FlashLoan'
    DEFI_STAKING = 'DeFi-Staking'
    DEFI_LENDING_BORROWING = 'DeFi-LendingBorrowing'
    DEFI_DECENTRALIZED_STABLE_COIN = 'DeFi-DecentralizedStableCoin'
    DEFI_DEX = 'DeFi-Dex'
    DEFI_INSURANCE_POOL = 'Defi-InsurancePool'
    DEFI_YIELD_FARMING = 'DeFi-YieldFarming'
    DEFI_CUSTOM = 'DeFi-Custom'

    class DeFi:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.DEFI_AUTO_MARKET_MAKER,
                SmartContractTemplateNames.DEFI_FLASH_LOAN,
                SmartContractTemplateNames.DEFI_STAKING,
                SmartContractTemplateNames.DEFI_LENDING_BORROWING,
                SmartContractTemplateNames.DEFI_DECENTRALIZED_STABLE_COIN,
                SmartContractTemplateNames.DEFI_DEX,
                SmartContractTemplateNames.DEFI_INSURANCE_POOL,
                SmartContractTemplateNames.DEFI_YIELD_FARMING,
                SmartContractTemplateNames.DEFI_CUSTOM,
            ]

    # Derivatives Contract Templates
    DERIVATIVES_OPTIONS = 'Derivatives-Options'
    DERIVATIVES_FUTURES = 'Derivatives-Futures'
    DERIVATIVES_CREDIT_DEFAULT_SWAP = 'Derivatives-CreditDefaultSwap'
    DERIVATIVES_BINARY_OPTIONS = 'Derivatives-BinaryOptions'
    DERIVATIVES_COMMODITY = 'Derivatives-Commodity'
    DERIVATIVES_INTEREST_RATE_SWAP = 'Derivatives-InterestRateSwap'
    DERIVATIVES_LEVERAGED_TOKEN = 'Derivatives-LeveragedToken'
    DERIVATIVES_VOLATILITY_INDEX = 'Derivatives-VolatilityIndex'
    DERIVATIVES_CUSTOM = 'Derivatives-Custom'

    class Derivatives:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.DERIVATIVES_OPTIONS,
                SmartContractTemplateNames.DERIVATIVES_FUTURES,
                SmartContractTemplateNames.DERIVATIVES_CREDIT_DEFAULT_SWAP,
                SmartContractTemplateNames.DERIVATIVES_BINARY_OPTIONS,
                SmartContractTemplateNames.DERIVATIVES_COMMODITY,
                SmartContractTemplateNames.DERIVATIVES_INTEREST_RATE_SWAP,
                SmartContractTemplateNames.DERIVATIVES_LEVERAGED_TOKEN,
                SmartContractTemplateNames.DERIVATIVES_VOLATILITY_INDEX,
                SmartContractTemplateNames.DERIVATIVES_CUSTOM,
            ]

    # Escrow Contract Templates
    ESCROW_BASIC = 'Escrow-Basic'
    ESCROW_CONDITIONAL = 'Escrow-Conditional'
    ESCROW_DISPUTE_RESOLUTION = 'Escrow-DisputeResolution'
    ESCROW_MULTI_SIGNATURE = 'Escrow-MultiSignature'
    ESCROW_PROGRESSIVE_RELEASE = 'Escrow-ProgressiveRelease'
    ESCROW_REFUND = 'Escrow-Refund'
    ESCROW_TIMELOCK = 'Escrow-Timelock'
    ESCROW_SUBSCRIPTION = 'Escrow-Subscription'
    ESCROW_MILESTONE = 'Escrow-Milestone'
    ESCROW_CUSTOM = 'Escrow-Custom'

    class Escrow:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.ESCROW_BASIC,
                SmartContractTemplateNames.ESCROW_CONDITIONAL,
                SmartContractTemplateNames.ESCROW_DISPUTE_RESOLUTION,
                SmartContractTemplateNames.ESCROW_MULTI_SIGNATURE,
                SmartContractTemplateNames.ESCROW_PROGRESSIVE_RELEASE,
                SmartContractTemplateNames.ESCROW_REFUND,
                SmartContractTemplateNames.ESCROW_TIMELOCK,
                SmartContractTemplateNames.ESCROW_SUBSCRIPTION,
                SmartContractTemplateNames.ESCROW_MILESTONE,
                SmartContractTemplateNames.ESCROW_CUSTOM,
            ]

    # Governance Contract Templates
    GOVERNANCE_MULTIPLE_PROPOSAL = 'Governance-MultipleProposal'
    GOVERNANCE_TIMELOCKED = 'Governance-Timelocked'
    GOVERNANCE_VESTING = 'Governance-Vesting'
    GOVERNANCE_VOTING_BONDED = 'Governance-VotingBonded'
    GOVERNANCE_VOTING_DELEGATED = 'Governance-VotingDelegated'
    GOVERNANCE_VOTING_DYNAMIC = 'Governance-VotingDynamic'
    GOVERNANCE_VOTING_OFFCHAIN = 'Governance-VotingOffchain'
    GOVERNANCE_VOTING_ONCHAIN = 'Governance-VotingOnchain'
    GOVERNANCE_VOTING_QUADRATIC = 'Governance-VotingQuadratic'
    GOVERNANCE_VOTING_QUORUM_MAJORITY = 'Governance-VotingQuorumMajority'
    GOVERNANCE_CUSTOM = 'Governance-Custom'

    class Governance:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.GOVERNANCE_MULTIPLE_PROPOSAL,
                SmartContractTemplateNames.GOVERNANCE_TIMELOCKED,
                SmartContractTemplateNames.GOVERNANCE_VESTING,
                SmartContractTemplateNames.GOVERNANCE_VOTING_BONDED,
                SmartContractTemplateNames.GOVERNANCE_VOTING_DELEGATED,
                SmartContractTemplateNames.GOVERNANCE_VOTING_DYNAMIC,
                SmartContractTemplateNames.GOVERNANCE_VOTING_OFFCHAIN,
                SmartContractTemplateNames.GOVERNANCE_VOTING_ONCHAIN,
                SmartContractTemplateNames.GOVERNANCE_VOTING_QUADRATIC,
                SmartContractTemplateNames.GOVERNANCE_VOTING_QUORUM_MAJORITY,
                SmartContractTemplateNames.GOVERNANCE_CUSTOM,
            ]

    # Identity Verification Contract Templates
    ID_ACCESS_CONTROL = 'ID-AccessControl'
    ID_CREDENTIAL_ISSUANCE = 'ID-CredentialIssuance'
    ID_DECENTRALIZED_ID = 'ID-DecentralizedID'
    ID_DECENTRALIZED_IDENTITY_AGGREGATOR = 'ID-DecentralizedIdentityAggregator'
    ID_DECENTRALIZED_REPUTATION_SLASHING = 'ID-DecentralizedReputationSlashing'
    ID_ID_BASED_VOTING = 'ID-IDBasedVoting'
    ID_MULTI_SIGNATURE_ID_VERIFICATION = 'ID-MultiSignatureIDVerification'
    ID_REPUTATION_SYSTEM = 'ID-ReputationSystem'
    ID_SOULBOUND_TOKENS = 'ID-SoulboundTokens'
    ID_ZERO_KNOWLEDGE_PROOF = 'ID-ZeroKnowledgeProof'
    ID_CUSTOM = 'ID-Custom'

    class Identity:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.ID_ACCESS_CONTROL,
                SmartContractTemplateNames.ID_CREDENTIAL_ISSUANCE,
                SmartContractTemplateNames.ID_DECENTRALIZED_ID,
                SmartContractTemplateNames.ID_DECENTRALIZED_IDENTITY_AGGREGATOR,
                SmartContractTemplateNames.ID_DECENTRALIZED_REPUTATION_SLASHING,
                SmartContractTemplateNames.ID_ID_BASED_VOTING,
                SmartContractTemplateNames.ID_MULTI_SIGNATURE_ID_VERIFICATION,
                SmartContractTemplateNames.ID_REPUTATION_SYSTEM,
                SmartContractTemplateNames.ID_SOULBOUND_TOKENS,
                SmartContractTemplateNames.ID_ZERO_KNOWLEDGE_PROOF,
                SmartContractTemplateNames.ID_CUSTOM,
            ]

    # Insurance Contract Templates
    INSURANCE_CLAIM_AND_DISPUTE_RESOLUTION = 'Insurance-ClaimAndDisputeResolution'
    INSURANCE_DECENTRALIZED_REINSURANCE = 'Insurance-DecentralizedReinsurance'
    INSURANCE_DECENTRALIZED_RISK_POOL = 'Insurance-DecentralizedRiskPool'
    INSURANCE_GROUP = 'Insurance-Group'
    INSURANCE_MICRO = 'Insurance-Micro'
    INSURANCE_MUTUAL = 'Insurance-Mutual'
    INSURANCE_PARAMETRIC = 'Insurance-Parametric'
    INSURANCE_PREMIUM_PAYMENT_AND_REFUND = 'Insurance-PremiumPaymentAndRefund'
    INSURANCE_STAKING_FOR_UNDERWRITING = 'Insurance-StakingForUnderwriting'
    INSURANCE_TOKENIZED = 'Insurance-Tokenized'
    INSURANCE_CUSTOM = 'Insurance-Custom'

    class Insurance:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.INSURANCE_CLAIM_AND_DISPUTE_RESOLUTION,
                SmartContractTemplateNames.INSURANCE_DECENTRALIZED_REINSURANCE,
                SmartContractTemplateNames.INSURANCE_DECENTRALIZED_RISK_POOL,
                SmartContractTemplateNames.INSURANCE_GROUP,
                SmartContractTemplateNames.INSURANCE_MICRO,
                SmartContractTemplateNames.INSURANCE_MUTUAL,
                SmartContractTemplateNames.INSURANCE_PARAMETRIC,
                SmartContractTemplateNames.INSURANCE_PREMIUM_PAYMENT_AND_REFUND,
                SmartContractTemplateNames.INSURANCE_STAKING_FOR_UNDERWRITING,
                SmartContractTemplateNames.INSURANCE_TOKENIZED,
                SmartContractTemplateNames.INSURANCE_CUSTOM,
            ]

    # Lending & Borrowing Contract Templates
    LENDING_COLLATERAL_SWAP = 'Lending-CollateralSwap'
    LENDING_DYNAMIC_INTEREST_RATE_LOAN = 'Lending-DynamicInterestRateLoan'
    LENDING_FLASH_LOAN = 'Lending-FlashLoan'
    LENDING_INTEREST_BEARING_TOKEN = 'Lending-InterestBearingToken'
    LENDING_OVER_COLLATERALIZED_LOAN = 'Lending-OverCollateralizedLoan'
    LENDING_P2P_MARKET = 'Lending-P2PMarket'
    LENDING_REVOLVING_CREDIT_LINE = 'Lending-RevolvingCreditLine'
    LENDING_SECURED = 'Lending-Secured'
    LENDING_CUSTOM = 'Lending-Custom'

    class Lending:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.LENDING_COLLATERAL_SWAP,
                SmartContractTemplateNames.LENDING_DYNAMIC_INTEREST_RATE_LOAN,
                SmartContractTemplateNames.LENDING_FLASH_LOAN,
                SmartContractTemplateNames.LENDING_INTEREST_BEARING_TOKEN,
                SmartContractTemplateNames.LENDING_OVER_COLLATERALIZED_LOAN,
                SmartContractTemplateNames.LENDING_P2P_MARKET,
                SmartContractTemplateNames.LENDING_REVOLVING_CREDIT_LINE,
                SmartContractTemplateNames.LENDING_SECURED,
                SmartContractTemplateNames.LENDING_CUSTOM,
            ]

    # Liquidity Pool Contract Templates
    LIQUIDITY_POOL_AUTO_BALANCING = 'LiquidityPool-AutoBalancing'
    LIQUIDITY_POOL_BASIC = 'LiquidityPool-Basic'
    LIQUIDITY_POOL_DYNAMIC_FEE = 'LiquidityPool-DynamicFee'
    LIQUIDITY_POOL_FLASH_LOAN = 'LiquidityPool-FlashLoan'
    LIQUIDITY_POOL_IMPERMANENT_LOSS_PROTECTION = 'LiquidityPool-ImpermanentLossProtection'
    LIQUIDITY_POOL_INCENTIVIZED = 'LiquidityPool-Incentivized'
    LIQUIDITY_POOL_MULTI_TOKEN = 'LiquidtyPool-MultiToken'
    LIQUIDITY_POOL_TIMELOCKED = 'LiquidityPool-Timelocked'
    LIQUIDITY_POOL_YIELD_FARMING = 'LiquidityPool-YieldFarming'
    LIQUIDITY_POOL_CUSTOM = 'LiquidityPool-Custom'

    class LiquidityPool:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.LIQUIDITY_POOL_AUTO_BALANCING,
                SmartContractTemplateNames.LIQUIDITY_POOL_BASIC,
                SmartContractTemplateNames.LIQUIDITY_POOL_DYNAMIC_FEE,
                SmartContractTemplateNames.LIQUIDITY_POOL_FLASH_LOAN,
                SmartContractTemplateNames.LIQUIDITY_POOL_IMPERMANENT_LOSS_PROTECTION,
                SmartContractTemplateNames.LIQUIDITY_POOL_INCENTIVIZED,
                SmartContractTemplateNames.LIQUIDITY_POOL_MULTI_TOKEN,
                SmartContractTemplateNames.LIQUIDITY_POOL_TIMELOCKED,
                SmartContractTemplateNames.LIQUIDITY_POOL_YIELD_FARMING,
                SmartContractTemplateNames.LIQUIDITY_POOL_CUSTOM,
            ]

    # Lottery Contract Templates
    LOTTERY_CHAINLINK_VRF = 'Lottery-ChainlinkVRF'
    LOTTERY_COMMUNITY_DRIVEN = 'Lottery-CommunityDriven'
    LOTTERY_DECENTRALIZED_POOL = 'Lottery-DecentralizedPool'
    LOTTERY_DEFLATIONARY_TOKEN = 'Lottery-DeflationaryToken'
    LOTTERY_MULTI_WINNER = 'Lottery-MultiWinner'
    LOTTERY_RAFFLE_BASED = 'Lottery-RaffleBased'
    LOTTERY_SIMPLE = 'Lottery-Simple'
    LOTTERY_SUBSCRIPTION_BASED = 'Lottery-SubscriptionBased'
    LOTTERY_CUSTOM = 'Lottery-Custom'

    class Lottery:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.LOTTERY_CHAINLINK_VRF,
                SmartContractTemplateNames.LOTTERY_COMMUNITY_DRIVEN,
                SmartContractTemplateNames.LOTTERY_DECENTRALIZED_POOL,
                SmartContractTemplateNames.LOTTERY_DEFLATIONARY_TOKEN,
                SmartContractTemplateNames.LOTTERY_MULTI_WINNER,
                SmartContractTemplateNames.LOTTERY_RAFFLE_BASED,
                SmartContractTemplateNames.LOTTERY_SIMPLE,
                SmartContractTemplateNames.LOTTERY_SUBSCRIPTION_BASED,
                SmartContractTemplateNames.LOTTERY_CUSTOM,
            ]

    # Marketplace Contract Templates
    MARKETPLACE_AUCTION_BASED = 'Marketplace-AuctionBased'
    MARKETPLACE_DECENTRALIZED_RENTAL = 'Marketplace-DecentralizedRental'
    MARKETPLACE_ERC20_TOKEN = 'Marketplace-ERC20Token'
    MARKETPLACE_NFT_ROYALTY_BASED = 'Marketplace-NFTRoyaltyBased'
    MARKETPLACE_NFT_SIMPLE = 'Marketplace-NFTSimple'
    MARKETPLACE_P2P_ESCROW = 'Marketplace-P2PEscrow'
    MARKETPLACE_REVENUE_SHARING = 'Marketplace-RevenueSharing'
    MARKETPLACE_SERVICE = 'Marketplace-Service'
    MARKETPLACE_WHITELIST = 'Marketplace-Whitelist'
    MARKETPLACE_CUSTOM = 'Marketplace-Custom'

    class Marketplace:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.MARKETPLACE_AUCTION_BASED,
                SmartContractTemplateNames.MARKETPLACE_DECENTRALIZED_RENTAL,
                SmartContractTemplateNames.MARKETPLACE_ERC20_TOKEN,
                SmartContractTemplateNames.MARKETPLACE_NFT_ROYALTY_BASED,
                SmartContractTemplateNames.MARKETPLACE_NFT_SIMPLE,
                SmartContractTemplateNames.MARKETPLACE_P2P_ESCROW,
                SmartContractTemplateNames.MARKETPLACE_REVENUE_SHARING,
                SmartContractTemplateNames.MARKETPLACE_SERVICE,
                SmartContractTemplateNames.MARKETPLACE_WHITELIST,
                SmartContractTemplateNames.MARKETPLACE_CUSTOM,
            ]

    # NFT Contract Templates
    ERC_721 = 'ERC-721'
    ERC_721_BATCH_MINING = 'ERC-721-BatchMining'
    ERC_721_DUTCH_AUCTION = 'ERC-721-DutchAuction'
    ERC_721_ENUMERABLE = 'ERC-721-Enumerable'
    ERC_721_FRACTIONALIZATION = 'ERC-721-Fractionalization'
    ERC_721_METADATA = 'ERC-721-Metadata'
    ERC_721_PAUSABLE = 'ERC-721-Pausable'
    ERC_721_RENTABLE = 'ERC-721-Rentable'
    ERC_721_STAKING = 'ERC-721-Staking'
    ERC_721_WRAPPED = 'ERC-721-Wrapped'
    ERC_721_MULTI_TOKEN = 'ERC-721-MultiToken'
    ERC_721_ROYALTY = 'ERC-721-Royalty'
    NFT_CUSTOM = 'NFT-Custom'

    class NFT:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.ERC_721,
                SmartContractTemplateNames.ERC_721_BATCH_MINING,
                SmartContractTemplateNames.ERC_721_DUTCH_AUCTION,
                SmartContractTemplateNames.ERC_721_ENUMERABLE,
                SmartContractTemplateNames.ERC_721_FRACTIONALIZATION,
                SmartContractTemplateNames.ERC_721_METADATA,
                SmartContractTemplateNames.ERC_721_PAUSABLE,
                SmartContractTemplateNames.ERC_721_RENTABLE,
                SmartContractTemplateNames.ERC_721_STAKING,
                SmartContractTemplateNames.ERC_721_WRAPPED,
                SmartContractTemplateNames.ERC_721_MULTI_TOKEN,
                SmartContractTemplateNames.ERC_721_ROYALTY,
                SmartContractTemplateNames.NFT_CUSTOM,
            ]

    # Oracle Contract Templates
    ORACLE_API_BASED = 'Oracle-APIBased'
    ORACLE_CUSTOM_DATA_FEED = 'Oracle-CustomDataFeed'
    ORACLE_DATA_SIGNATURE_VERIFICATION = 'Oracle-DataSignatureVerification'
    ORACLE_FALLBACK = 'Oracle-Fallback'
    ORACLE_MULTI_SOURCE_AGGREGATION = 'Oracle-MultiSourceAggregation'
    ORACLE_PRICE = 'Oracle-Price'
    ORACLE_RANDOMNESS = 'Oracle-Randomness'
    ORACLE_TIME_BASED_DATA_FEED = 'Oracle-TimebasedDataFeed'
    ORACLE_WEATHER = 'Oracle-Weather'
    ORACLE_CUSTOM = 'Oracle-Custom'

    class Oracle:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.ORACLE_API_BASED,
                SmartContractTemplateNames.ORACLE_CUSTOM_DATA_FEED,
                SmartContractTemplateNames.ORACLE_DATA_SIGNATURE_VERIFICATION,
                SmartContractTemplateNames.ORACLE_FALLBACK,
                SmartContractTemplateNames.ORACLE_MULTI_SOURCE_AGGREGATION,
                SmartContractTemplateNames.ORACLE_PRICE,
                SmartContractTemplateNames.ORACLE_RANDOMNESS,
                SmartContractTemplateNames.ORACLE_TIME_BASED_DATA_FEED,
                SmartContractTemplateNames.ORACLE_WEATHER,
                SmartContractTemplateNames.ORACLE_CUSTOM,
            ]

    # Real Estate Tokenization Contract Templates
    REAL_ESTATE_CROWDFUNDING = 'RealEstate-Crowdfunding'
    REAL_ESTATE_DAO = 'RealEstate-DAO'
    REAL_ESTATE_FRACTIONAL_OWNERSHIP = 'RealEstate-FractionalOwnership'
    REAL_ESTATE_LOAN = 'RealEstate-Loan'
    REAL_ESTATE_MARKETPLACE = 'RealEstate-Marketplace'
    REAL_ESTATE_PROPERTY_AUCTION = 'RealEstate-PropertyAuction'
    REAL_ESTATE_PROPERTY_LEASE_TO_OWN = 'RealEstate-PropertyLeaseToOwn'
    REAL_ESTATE_PROPERTY_TOKENIZATION = 'RealEstate-PropertyTokenization'
    REAL_ESTATE_RENTAL_AGREEMENT = 'RealEstate-RentalAgreement'
    REAL_ESTATE_CUSTOM = 'RealEstate-Custom'

    class RealEstate:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.REAL_ESTATE_CROWDFUNDING,
                SmartContractTemplateNames.REAL_ESTATE_DAO,
                SmartContractTemplateNames.REAL_ESTATE_FRACTIONAL_OWNERSHIP,
                SmartContractTemplateNames.REAL_ESTATE_LOAN,
                SmartContractTemplateNames.REAL_ESTATE_MARKETPLACE,
                SmartContractTemplateNames.REAL_ESTATE_PROPERTY_AUCTION,
                SmartContractTemplateNames.REAL_ESTATE_PROPERTY_LEASE_TO_OWN,
                SmartContractTemplateNames.REAL_ESTATE_PROPERTY_TOKENIZATION,
                SmartContractTemplateNames.REAL_ESTATE_RENTAL_AGREEMENT,
                SmartContractTemplateNames.REAL_ESTATE_CUSTOM,
            ]

    # Royalties Contract Templates
    ROYALTIES_ESCROW_BASED_PAYMENT = 'Royalties-EscrowBasedPayment'
    ROYALTIES_LICENCE_BASED = 'Royalties-LicenceBased'
    ROYALTIES_NFT_ROYALTY_DISTRIBUTION = 'Royalties-NFTRoyaltyDistribution'
    ROYALTIES_PERCENTAGE_BASED = 'Royalties-PercentageBased'
    ROYALTIES_PERFORMANCE_BASED = 'Royalties-PerformanceBased'
    ROYALTIES_POOL = 'Royalties-Pool'
    ROYALTIES_REAL_TIME_SPLITTING = 'Royalties-RealTimeSplitting'
    ROYALTIES_STREAMING = 'Royalties-Streaming'
    ROYALTIES_TIERED_STRUCTURE = 'Royalties-TieredStructure'
    ROYALTIES_CUSTOM = 'Royalties-Custom'

    class Royalties:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.ROYALTIES_ESCROW_BASED_PAYMENT,
                SmartContractTemplateNames.ROYALTIES_LICENCE_BASED,
                SmartContractTemplateNames.ROYALTIES_NFT_ROYALTY_DISTRIBUTION,
                SmartContractTemplateNames.ROYALTIES_PERCENTAGE_BASED,
                SmartContractTemplateNames.ROYALTIES_PERFORMANCE_BASED,
                SmartContractTemplateNames.ROYALTIES_POOL,
                SmartContractTemplateNames.ROYALTIES_REAL_TIME_SPLITTING,
                SmartContractTemplateNames.ROYALTIES_STREAMING,
                SmartContractTemplateNames.ROYALTIES_TIERED_STRUCTURE,
                SmartContractTemplateNames.ROYALTIES_CUSTOM,
            ]

    # Staking Contract Templates
    STAKING_AUTO_COMPOUNDING = 'Staking-AutoCompounding'
    STAKING_BASIC = 'Staking-Basic'
    STAKING_EARLY_WITHDRAWAL_PENALTY = 'Staking-EarlyWithdrawalPenalty'
    STAKING_LIQUIDITY = 'Staking-Liquidity'
    STAKING_MULTI_ASSET = 'Staking-MultiAsset'
    STAKING_MULTI_TIER = 'Staking-MultiTier'
    STAKING_TIMELOCKED = 'Staking-Timelocked'
    STAKING_TO_ACCESS = 'Staking-ToAccess'
    STAKING_TOKEN_GOVERNANCE = 'Staking-TokenGovernance'
    STAKING_YIELD_FARMING = 'Staking-YieldFarming'
    STAKING_CUSTOM = 'Staking-Custom'

    class Staking:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.STAKING_AUTO_COMPOUNDING,
                SmartContractTemplateNames.STAKING_BASIC,
                SmartContractTemplateNames.STAKING_EARLY_WITHDRAWAL_PENALTY,
                SmartContractTemplateNames.STAKING_LIQUIDITY,
                SmartContractTemplateNames.STAKING_MULTI_ASSET,
                SmartContractTemplateNames.STAKING_MULTI_TIER,
                SmartContractTemplateNames.STAKING_TIMELOCKED,
                SmartContractTemplateNames.STAKING_TO_ACCESS,
                SmartContractTemplateNames.STAKING_TOKEN_GOVERNANCE,
                SmartContractTemplateNames.STAKING_YIELD_FARMING,
                SmartContractTemplateNames.STAKING_CUSTOM,
            ]

    # Supply Chain Contract Templates
    SUPPLY_CHAIN_ASSET_TRANSFER = 'SupplyChain-AssetTransfer'
    SUPPLY_CHAIN_AUTOMATED_PAYMENT = 'SupplyChain-AutomatedPayment'
    SUPPLY_CHAIN_CERTIFICATION_VERIFICATION = 'SupplyChain-CertificationVerification'
    SUPPLY_CHAIN_FINANCING = 'SupplyChain-Financing'
    SUPPLY_CHAIN_INVENTORY_MANAGEMENT = 'SupplyChain-InventoryManagement'
    SUPPLY_CHAIN_MULTI_PARTY_COORDINATION = 'SupplyChain-MultiPartyCoordination'
    SUPPLY_CHAIN_PRODUCT_TRACKING = 'SupplyChain-ProductTracking'
    SUPPLY_CHAIN_SHIPMENT_TRACKING = 'SupplyChain-ShipmentTracking'
    SUPPLY_CHAIN_SUPPLIER_VERIFICATION = 'SupplyChain-SupplierVerification'
    SUPPLY_CHAIN_CUSTOM = 'SupplyChain-Custom'

    class SupplyChain:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.SUPPLY_CHAIN_ASSET_TRANSFER,
                SmartContractTemplateNames.SUPPLY_CHAIN_AUTOMATED_PAYMENT,
                SmartContractTemplateNames.SUPPLY_CHAIN_CERTIFICATION_VERIFICATION,
                SmartContractTemplateNames.SUPPLY_CHAIN_FINANCING,
                SmartContractTemplateNames.SUPPLY_CHAIN_INVENTORY_MANAGEMENT,
                SmartContractTemplateNames.SUPPLY_CHAIN_MULTI_PARTY_COORDINATION,
                SmartContractTemplateNames.SUPPLY_CHAIN_PRODUCT_TRACKING,
                SmartContractTemplateNames.SUPPLY_CHAIN_SHIPMENT_TRACKING,
                SmartContractTemplateNames.SUPPLY_CHAIN_SUPPLIER_VERIFICATION,
                SmartContractTemplateNames.SUPPLY_CHAIN_CUSTOM,
            ]

    # Token Contract Templates
    ERC_20 = 'ERC-20'
    ERC_20_BURNABLE = 'ERC-20-Burnable'
    ERC_20_CAPPED = 'ERC-20-Capped'
    ERC_20_DEFLATIONARY = 'ERC-20-Deflationary'
    ERC_20_MINTABLE = 'ERC-20-Mintable'
    ERC_20_PAUSABLE = 'ERC-20-Pausable'
    ERC_20_SNAPSHOT = 'ERC-20-Snapshot'
    ERC_20_TAXABLE = 'ERC-20-Taxable'
    ERC_20_VESTING = 'ERC-20-Vesting'
    ERC_20_CUSTOM = 'ERC-20-Custom'

    class Token:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.ERC_20,
                SmartContractTemplateNames.ERC_20_BURNABLE,
                SmartContractTemplateNames.ERC_20_CAPPED,
                SmartContractTemplateNames.ERC_20_DEFLATIONARY,
                SmartContractTemplateNames.ERC_20_MINTABLE,
                SmartContractTemplateNames.ERC_20_PAUSABLE,
                SmartContractTemplateNames.ERC_20_SNAPSHOT,
                SmartContractTemplateNames.ERC_20_TAXABLE,
                SmartContractTemplateNames.ERC_20_VESTING,
                SmartContractTemplateNames.ERC_20_CUSTOM,
            ]

    # Vesting Contract Templates
    VESTING_ADJUSTABLE_TERMS = 'Vesting-AdjustableTerms'
    VESTING_CLIFF = 'Vesting-Cliff'
    VESTING_CUSTOM_SCHEDULE = 'Vesting-CustomSchedule'
    VESTING_DEFERRED = 'Vesting-Deferred'
    VESTING_GRADUAL_RELEASE = 'Vesting-GradualRelease'
    VESTING_MILESTONE_BASED = 'Vesting-MilestoneBased'
    VESTING_PERFORMANCE_BASED = 'Vesting-PerformanceBased'
    VESTING_TEAM_BASED = 'Vesting-TeamBased'
    VESTING_TIME_BASED = 'Vesting-TimeBased'
    VESTING_WITH_REVOCATION = 'Vesting-WithRevocation'
    VESTING_CUSTOM = 'Vesting-Custom'

    class Vesting:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.VESTING_ADJUSTABLE_TERMS,
                SmartContractTemplateNames.VESTING_CLIFF,
                SmartContractTemplateNames.VESTING_CUSTOM_SCHEDULE,
                SmartContractTemplateNames.VESTING_DEFERRED,
                SmartContractTemplateNames.VESTING_GRADUAL_RELEASE,
                SmartContractTemplateNames.VESTING_MILESTONE_BASED,
                SmartContractTemplateNames.VESTING_PERFORMANCE_BASED,
                SmartContractTemplateNames.VESTING_TEAM_BASED,
                SmartContractTemplateNames.VESTING_TIME_BASED,
                SmartContractTemplateNames.VESTING_WITH_REVOCATION,
                SmartContractTemplateNames.VESTING_CUSTOM,
            ]

    # Voting Contract Templates
    VOTING_ANONYMOUS = 'Voting-Anonymous'
    VOTING_DELEGATED = 'Voting-Delegated'
    VOTING_LIQUID_DEMOCRACY = 'Voting-LiquidDemocracy'
    VOTING_MULTI_SIGNATURE = 'Voting-MultiSignature'
    VOTING_QUADRATIC = 'Voting-Quadratic'
    VOTING_TIMELOCKED = 'Voting-Timelocked'
    VOTING_TIME_WEIGHTED = 'Voting-TimeWeighted'
    VOTING_TOKEN_BASED = 'Voting-TokenBased'
    VOTING_WEIGHTED = 'Voting-Weighted'
    VOTING_CUSTOM = 'Voting-Custom'

    class Voting:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.VOTING_ANONYMOUS,
                SmartContractTemplateNames.VOTING_DELEGATED,
                SmartContractTemplateNames.VOTING_LIQUID_DEMOCRACY,
                SmartContractTemplateNames.VOTING_MULTI_SIGNATURE,
                SmartContractTemplateNames.VOTING_QUADRATIC,
                SmartContractTemplateNames.VOTING_TIMELOCKED,
                SmartContractTemplateNames.VOTING_TIME_WEIGHTED,
                SmartContractTemplateNames.VOTING_TOKEN_BASED,
                SmartContractTemplateNames.VOTING_WEIGHTED,
                SmartContractTemplateNames.VOTING_CUSTOM,
            ]

    class Custom:
        @staticmethod
        def as_list():
            return [
                SmartContractTemplateNames.CROWDSALE_CUSTOM,
                SmartContractTemplateNames.DAO_CUSTOM,
                SmartContractTemplateNames.DEFI_CUSTOM,
                SmartContractTemplateNames.DERIVATIVES_CUSTOM,
                SmartContractTemplateNames.ESCROW_CUSTOM,
                SmartContractTemplateNames.GOVERNANCE_CUSTOM,
                SmartContractTemplateNames.ID_CUSTOM,
                SmartContractTemplateNames.INSURANCE_CUSTOM,
                SmartContractTemplateNames.LENDING_CUSTOM,
                SmartContractTemplateNames.LIQUIDITY_POOL_CUSTOM,
                SmartContractTemplateNames.LOTTERY_CUSTOM,
                SmartContractTemplateNames.MARKETPLACE_CUSTOM,
                SmartContractTemplateNames.NFT_CUSTOM,
                SmartContractTemplateNames.ORACLE_CUSTOM,
                SmartContractTemplateNames.REAL_ESTATE_CUSTOM,
                SmartContractTemplateNames.ROYALTIES_CUSTOM,
                SmartContractTemplateNames.STAKING_CUSTOM,
                SmartContractTemplateNames.SUPPLY_CHAIN_CUSTOM,
                SmartContractTemplateNames.ERC_20_CUSTOM,
                SmartContractTemplateNames.VESTING_CUSTOM,
                SmartContractTemplateNames.VOTING_CUSTOM,
            ]

    @staticmethod
    def as_list():
        return [
            SmartContractTemplateNames.CROWDSALE_BASIC,
            SmartContractTemplateNames.CROWDSALE_REFUNDABLE,
            SmartContractTemplateNames.CROWDSALE_CAPPED,
            SmartContractTemplateNames.CROWDSALE_TIMED,
            SmartContractTemplateNames.CROWDSALE_WHITELISTED,
            SmartContractTemplateNames.CROWDSALE_REFUNDABLE_WITH_GOAL,
            SmartContractTemplateNames.CROWDSALE_TIERED_PRICING,
            SmartContractTemplateNames.CROWDSALE_TOKEN_DISTRIBUTION,
            SmartContractTemplateNames.CROWDSALE_VESTING,
            SmartContractTemplateNames.CROWDSALE_CUSTOM,
            SmartContractTemplateNames.DAO_ERC20_TOKEN_VOTING,
            SmartContractTemplateNames.DAO_MULTI_SIGNATURE,
            SmartContractTemplateNames.DAO_TOKEN_CURATED_REGISTRY,
            SmartContractTemplateNames.DAO_TREASURY_MANAGEMENT,
            SmartContractTemplateNames.DAO_TREASURY_TIMELOCKED,
            SmartContractTemplateNames.DAO_VOTING_BASIC,
            SmartContractTemplateNames.DAO_VOTING_DELEGATED,
            SmartContractTemplateNames.DAO_VOTING_QUADRATIC,
            SmartContractTemplateNames.DAO_VOTING_OFF_CHAIN,
            SmartContractTemplateNames.DAO_VOTING_QUORUM_MAJORITY,
            SmartContractTemplateNames.DAO_CUSTOM,
            SmartContractTemplateNames.DEFI_AUTO_MARKET_MAKER,
            SmartContractTemplateNames.DEFI_FLASH_LOAN,
            SmartContractTemplateNames.DEFI_STAKING,
            SmartContractTemplateNames.DEFI_LENDING_BORROWING,
            SmartContractTemplateNames.DEFI_DECENTRALIZED_STABLE_COIN,
            SmartContractTemplateNames.DEFI_DEX,
            SmartContractTemplateNames.DEFI_INSURANCE_POOL,
            SmartContractTemplateNames.DEFI_YIELD_FARMING,
            SmartContractTemplateNames.DEFI_CUSTOM,
            SmartContractTemplateNames.DERIVATIVES_OPTIONS,
            SmartContractTemplateNames.DERIVATIVES_FUTURES,
            SmartContractTemplateNames.DERIVATIVES_CREDIT_DEFAULT_SWAP,
            SmartContractTemplateNames.DERIVATIVES_BINARY_OPTIONS,
            SmartContractTemplateNames.DERIVATIVES_COMMODITY,
            SmartContractTemplateNames.DERIVATIVES_INTEREST_RATE_SWAP,
            SmartContractTemplateNames.DERIVATIVES_LEVERAGED_TOKEN,
            SmartContractTemplateNames.DERIVATIVES_VOLATILITY_INDEX,
            SmartContractTemplateNames.DERIVATIVES_CUSTOM,
            SmartContractTemplateNames.ESCROW_BASIC,
            SmartContractTemplateNames.ESCROW_CONDITIONAL,
            SmartContractTemplateNames.ESCROW_DISPUTE_RESOLUTION,
            SmartContractTemplateNames.ESCROW_MULTI_SIGNATURE,
            SmartContractTemplateNames.ESCROW_PROGRESSIVE_RELEASE,
            SmartContractTemplateNames.ESCROW_REFUND,
            SmartContractTemplateNames.ESCROW_TIMELOCK,
            SmartContractTemplateNames.ESCROW_SUBSCRIPTION,
            SmartContractTemplateNames.ESCROW_MILESTONE,
            SmartContractTemplateNames.ESCROW_CUSTOM,
            SmartContractTemplateNames.GOVERNANCE_MULTIPLE_PROPOSAL,
            SmartContractTemplateNames.GOVERNANCE_TIMELOCKED,
            SmartContractTemplateNames.GOVERNANCE_VESTING,
            SmartContractTemplateNames.GOVERNANCE_VOTING_BONDED,
            SmartContractTemplateNames.GOVERNANCE_VOTING_DELEGATED,
            SmartContractTemplateNames.GOVERNANCE_VOTING_DYNAMIC,
            SmartContractTemplateNames.GOVERNANCE_VOTING_OFFCHAIN,
            SmartContractTemplateNames.GOVERNANCE_VOTING_ONCHAIN,
            SmartContractTemplateNames.GOVERNANCE_VOTING_QUADRATIC,
            SmartContractTemplateNames.GOVERNANCE_VOTING_QUORUM_MAJORITY,
            SmartContractTemplateNames.GOVERNANCE_CUSTOM,
            SmartContractTemplateNames.ID_ACCESS_CONTROL,
            SmartContractTemplateNames.ID_CREDENTIAL_ISSUANCE,
            SmartContractTemplateNames.ID_DECENTRALIZED_ID,
            SmartContractTemplateNames.ID_DECENTRALIZED_IDENTITY_AGGREGATOR,
            SmartContractTemplateNames.ID_DECENTRALIZED_REPUTATION_SLASHING,
            SmartContractTemplateNames.ID_ID_BASED_VOTING,
            SmartContractTemplateNames.ID_MULTI_SIGNATURE_ID_VERIFICATION,
            SmartContractTemplateNames.ID_REPUTATION_SYSTEM,
            SmartContractTemplateNames.ID_SOULBOUND_TOKENS,
            SmartContractTemplateNames.ID_ZERO_KNOWLEDGE_PROOF,
            SmartContractTemplateNames.ID_CUSTOM,
            SmartContractTemplateNames.INSURANCE_CLAIM_AND_DISPUTE_RESOLUTION,
            SmartContractTemplateNames.INSURANCE_DECENTRALIZED_REINSURANCE,
            SmartContractTemplateNames.INSURANCE_DECENTRALIZED_RISK_POOL,
            SmartContractTemplateNames.INSURANCE_GROUP,
            SmartContractTemplateNames.INSURANCE_MICRO,
            SmartContractTemplateNames.INSURANCE_MUTUAL,
            SmartContractTemplateNames.INSURANCE_PARAMETRIC,
            SmartContractTemplateNames.INSURANCE_PREMIUM_PAYMENT_AND_REFUND,
            SmartContractTemplateNames.INSURANCE_STAKING_FOR_UNDERWRITING,
            SmartContractTemplateNames.INSURANCE_TOKENIZED,
            SmartContractTemplateNames.INSURANCE_CUSTOM,
            SmartContractTemplateNames.LENDING_COLLATERAL_SWAP,
            SmartContractTemplateNames.LENDING_DYNAMIC_INTEREST_RATE_LOAN,
            SmartContractTemplateNames.LENDING_FLASH_LOAN,
            SmartContractTemplateNames.LENDING_INTEREST_BEARING_TOKEN,
            SmartContractTemplateNames.LENDING_OVER_COLLATERALIZED_LOAN,
            SmartContractTemplateNames.LENDING_P2P_MARKET,
            SmartContractTemplateNames.LENDING_REVOLVING_CREDIT_LINE,
            SmartContractTemplateNames.LENDING_SECURED,
            SmartContractTemplateNames.LENDING_CUSTOM,
            SmartContractTemplateNames.LIQUIDITY_POOL_AUTO_BALANCING,
            SmartContractTemplateNames.LIQUIDITY_POOL_BASIC,
            SmartContractTemplateNames.LIQUIDITY_POOL_DYNAMIC_FEE,
            SmartContractTemplateNames.LIQUIDITY_POOL_FLASH_LOAN,
            SmartContractTemplateNames.LIQUIDITY_POOL_IMPERMANENT_LOSS_PROTECTION,
            SmartContractTemplateNames.LIQUIDITY_POOL_INCENTIVIZED,
            SmartContractTemplateNames.LIQUIDITY_POOL_MULTI_TOKEN,
            SmartContractTemplateNames.LIQUIDITY_POOL_TIMELOCKED,
            SmartContractTemplateNames.LIQUIDITY_POOL_YIELD_FARMING,
            SmartContractTemplateNames.LIQUIDITY_POOL_CUSTOM,
            SmartContractTemplateNames.LOTTERY_CHAINLINK_VRF,
            SmartContractTemplateNames.LOTTERY_COMMUNITY_DRIVEN,
            SmartContractTemplateNames.LOTTERY_DECENTRALIZED_POOL,
            SmartContractTemplateNames.LOTTERY_DEFLATIONARY_TOKEN,
            SmartContractTemplateNames.LOTTERY_MULTI_WINNER,
            SmartContractTemplateNames.LOTTERY_RAFFLE_BASED,
            SmartContractTemplateNames.LOTTERY_SIMPLE,
            SmartContractTemplateNames.LOTTERY_SUBSCRIPTION_BASED,
            SmartContractTemplateNames.LOTTERY_CUSTOM,
            SmartContractTemplateNames.MARKETPLACE_AUCTION_BASED,
            SmartContractTemplateNames.MARKETPLACE_DECENTRALIZED_RENTAL,
            SmartContractTemplateNames.MARKETPLACE_ERC20_TOKEN,
            SmartContractTemplateNames.MARKETPLACE_NFT_ROYALTY_BASED,
            SmartContractTemplateNames.MARKETPLACE_NFT_SIMPLE,
            SmartContractTemplateNames.MARKETPLACE_P2P_ESCROW,
            SmartContractTemplateNames.MARKETPLACE_REVENUE_SHARING,
            SmartContractTemplateNames.MARKETPLACE_SERVICE,
            SmartContractTemplateNames.MARKETPLACE_WHITELIST,
            SmartContractTemplateNames.MARKETPLACE_CUSTOM,
            SmartContractTemplateNames.ERC_721,
            SmartContractTemplateNames.ERC_721_BATCH_MINING,
            SmartContractTemplateNames.ERC_721_DUTCH_AUCTION,
            SmartContractTemplateNames.ERC_721_ENUMERABLE,
            SmartContractTemplateNames.ERC_721_FRACTIONALIZATION,
            SmartContractTemplateNames.ERC_721_METADATA,
            SmartContractTemplateNames.ERC_721_PAUSABLE,
            SmartContractTemplateNames.ERC_721_RENTABLE,
            SmartContractTemplateNames.ERC_721_STAKING,
            SmartContractTemplateNames.ERC_721_WRAPPED,
            SmartContractTemplateNames.ERC_721_MULTI_TOKEN,
            SmartContractTemplateNames.ERC_721_ROYALTY,
            SmartContractTemplateNames.NFT_CUSTOM,
            SmartContractTemplateNames.ORACLE_API_BASED,
            SmartContractTemplateNames.ORACLE_CUSTOM_DATA_FEED,
            SmartContractTemplateNames.ORACLE_DATA_SIGNATURE_VERIFICATION,
            SmartContractTemplateNames.ORACLE_FALLBACK,
            SmartContractTemplateNames.ORACLE_MULTI_SOURCE_AGGREGATION,
            SmartContractTemplateNames.ORACLE_PRICE,
            SmartContractTemplateNames.ORACLE_RANDOMNESS,
            SmartContractTemplateNames.ORACLE_TIME_BASED_DATA_FEED,
            SmartContractTemplateNames.ORACLE_WEATHER,
            SmartContractTemplateNames.ORACLE_CUSTOM,
            SmartContractTemplateNames.REAL_ESTATE_CROWDFUNDING,
            SmartContractTemplateNames.REAL_ESTATE_DAO,
            SmartContractTemplateNames.REAL_ESTATE_FRACTIONAL_OWNERSHIP,
            SmartContractTemplateNames.REAL_ESTATE_LOAN,
            SmartContractTemplateNames.REAL_ESTATE_MARKETPLACE,
            SmartContractTemplateNames.REAL_ESTATE_PROPERTY_AUCTION,
            SmartContractTemplateNames.REAL_ESTATE_PROPERTY_LEASE_TO_OWN,
            SmartContractTemplateNames.REAL_ESTATE_PROPERTY_TOKENIZATION,
            SmartContractTemplateNames.REAL_ESTATE_RENTAL_AGREEMENT,
            SmartContractTemplateNames.REAL_ESTATE_CUSTOM,
            SmartContractTemplateNames.ROYALTIES_ESCROW_BASED_PAYMENT,
            SmartContractTemplateNames.ROYALTIES_LICENCE_BASED,
            SmartContractTemplateNames.ROYALTIES_NFT_ROYALTY_DISTRIBUTION,
            SmartContractTemplateNames.ROYALTIES_PERCENTAGE_BASED,
            SmartContractTemplateNames.ROYALTIES_PERFORMANCE_BASED,
            SmartContractTemplateNames.ROYALTIES_POOL,
            SmartContractTemplateNames.ROYALTIES_REAL_TIME_SPLITTING,
            SmartContractTemplateNames.ROYALTIES_STREAMING,
            SmartContractTemplateNames.ROYALTIES_TIERED_STRUCTURE,
            SmartContractTemplateNames.ROYALTIES_CUSTOM,
            SmartContractTemplateNames.STAKING_AUTO_COMPOUNDING,
            SmartContractTemplateNames.STAKING_BASIC,
            SmartContractTemplateNames.STAKING_EARLY_WITHDRAWAL_PENALTY,
            SmartContractTemplateNames.STAKING_LIQUIDITY,
            SmartContractTemplateNames.STAKING_MULTI_ASSET,
            SmartContractTemplateNames.STAKING_MULTI_TIER,
            SmartContractTemplateNames.STAKING_TIMELOCKED,
            SmartContractTemplateNames.STAKING_TO_ACCESS,
            SmartContractTemplateNames.STAKING_TOKEN_GOVERNANCE,
            SmartContractTemplateNames.STAKING_YIELD_FARMING,
            SmartContractTemplateNames.STAKING_CUSTOM,
            SmartContractTemplateNames.SUPPLY_CHAIN_ASSET_TRANSFER,
            SmartContractTemplateNames.SUPPLY_CHAIN_AUTOMATED_PAYMENT,
            SmartContractTemplateNames.SUPPLY_CHAIN_CERTIFICATION_VERIFICATION,
            SmartContractTemplateNames.SUPPLY_CHAIN_FINANCING,
            SmartContractTemplateNames.SUPPLY_CHAIN_INVENTORY_MANAGEMENT,
            SmartContractTemplateNames.SUPPLY_CHAIN_MULTI_PARTY_COORDINATION,
            SmartContractTemplateNames.SUPPLY_CHAIN_PRODUCT_TRACKING,
            SmartContractTemplateNames.SUPPLY_CHAIN_SHIPMENT_TRACKING,
            SmartContractTemplateNames.SUPPLY_CHAIN_SUPPLIER_VERIFICATION,
            SmartContractTemplateNames.SUPPLY_CHAIN_CUSTOM,
            SmartContractTemplateNames.ERC_20,
            SmartContractTemplateNames.ERC_20_BURNABLE,
            SmartContractTemplateNames.ERC_20_CAPPED,
            SmartContractTemplateNames.ERC_20_DEFLATIONARY,
            SmartContractTemplateNames.ERC_20_MINTABLE,
            SmartContractTemplateNames.ERC_20_PAUSABLE,
            SmartContractTemplateNames.ERC_20_SNAPSHOT,
            SmartContractTemplateNames.ERC_20_TAXABLE,
            SmartContractTemplateNames.ERC_20_VESTING,
            SmartContractTemplateNames.ERC_20_CUSTOM,
            SmartContractTemplateNames.VESTING_ADJUSTABLE_TERMS,
            SmartContractTemplateNames.VESTING_CLIFF,
            SmartContractTemplateNames.VESTING_CUSTOM_SCHEDULE,
            SmartContractTemplateNames.VESTING_DEFERRED,
            SmartContractTemplateNames.VESTING_GRADUAL_RELEASE,
            SmartContractTemplateNames.VESTING_MILESTONE_BASED,
            SmartContractTemplateNames.VESTING_PERFORMANCE_BASED,
            SmartContractTemplateNames.VESTING_TEAM_BASED,
            SmartContractTemplateNames.VESTING_TIME_BASED,
            SmartContractTemplateNames.VESTING_WITH_REVOCATION,
            SmartContractTemplateNames.VESTING_CUSTOM,
            SmartContractTemplateNames.VOTING_ANONYMOUS,
            SmartContractTemplateNames.VOTING_DELEGATED,
            SmartContractTemplateNames.VOTING_LIQUID_DEMOCRACY,
            SmartContractTemplateNames.VOTING_MULTI_SIGNATURE,
            SmartContractTemplateNames.VOTING_QUADRATIC,
            SmartContractTemplateNames.VOTING_TIMELOCKED,
            SmartContractTemplateNames.VOTING_TIME_WEIGHTED,
            SmartContractTemplateNames.VOTING_TOKEN_BASED,
            SmartContractTemplateNames.VOTING_WEIGHTED,
            SmartContractTemplateNames.VOTING_CUSTOM,
        ]


BLOCKCHAIN_WALLET_CONNECTION_ADMIN_LIST = ('organization', 'blockchain_type', 'nickname', 'wallet_balance',
                                           'balance_last_synced_at')
BLOCKCHAIN_WALLET_CONNECTION_ADMIN_FILTER = ('organization', 'blockchain_type', 'created_at', 'updated_at')
BLOCKCHAIN_WALLET_CONNECTION_ADMIN_SEARCH = ('organization', 'blockchain_type', 'nickname', 'wallet_address')

BLOCKCHAIN_SMART_CONTRACT_ADMIN_LIST = ['nickname', 'wallet', 'category', 'contract_template', 'created_at',
                                        'updated_at']
BLOCKCHAIN_SMART_CONTRACT_ADMIN_FILTER = ['nickname', 'wallet', 'category', 'contract_template', 'created_at',
                                          'updated_at']
BLOCKCHAIN_SMART_CONTRACT_ADMIN_SEARCH = ['nickname', 'wallet', 'category', 'contract_template',
                                          'contract_template_filepath']

DEPLOYMENT_STATUSES = [
    ('not-generated', 'Not Generated'),
    ('generated-unsigned', 'Generated Unsigned'),
    ('transaction-staged', 'Transaction Staged'),
    ('waiting-for-mining', 'Waiting for Mining'),
    ('deployed', 'Deployed'),
    ('failed', 'Failed'),
]


class DeploymentStatusesNames:
    NOT_GENERATED = 'not-generated'  #
    GENERATED_UNSIGNED = 'generated-unsigned'  #
    TRANSACTION_STAGED = 'transaction-staged'  #
    WAITING_FOR_MINING = 'waiting-for-mining'  #
    DEPLOYED = 'deployed'  #
    FAILED = 'failed' #

    @staticmethod
    def as_list():
        return [
            DeploymentStatusesNames.NOT_GENERATED,
            DeploymentStatusesNames.GENERATED_UNSIGNED,
            DeploymentStatusesNames.TRANSACTION_STAGED,
            DeploymentStatusesNames.WAITING_FOR_MINING,
            DeploymentStatusesNames.DEPLOYED,
            DeploymentStatusesNames.FAILED,
        ]


class GenerateSmartContractViewActionTypes:
    GENERATE_CONTRACT = 'generate_contract'
    SIGN_AND_DEPLOY_CONTRACT = 'sign_and_deploy_contract'


SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_LIST = ["smart_contract", "assistant", "created_by_user", "created_at", "updated_at"]
SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_FILTER = ["smart_contract", "assistant", "created_by_user", "created_at", "updated_at"]
SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_SEARCH = ["smart_contract", "assistant", "created_by_user", "created_at", "updated_at"]
