from abc import ABC, abstractmethod
from typing import List
from .query_params import QueryParams
from .property_transaction import PropertyTransaction


class DataSourceClient(ABC):
    
    @abstractmethod
    def fetch_property_transactions(self, params: QueryParams) -> List[PropertyTransaction]:
        pass
    
    @abstractmethod
    def validate_params(self, params: QueryParams) -> bool:
        pass
