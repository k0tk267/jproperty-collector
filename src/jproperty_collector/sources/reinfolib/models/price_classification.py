from enum import Enum

class PriceClassification(Enum):
    TRANSACTION_ONLY = "01"
    CONTRACT_ONLY = "02"
    BOTH = None
