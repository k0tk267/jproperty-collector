from jproperty_collector.core.models import DataSourceClient, PropertyTransaction
from jproperty_collector.core.exceptions import ValidationError
from jproperty_collector.core.base_client import BaseHTTPClient
from jproperty_collector.sources.reinfolib.formatter import ReinfolibDataFormatter
from jproperty_collector.sources.reinfolib.models.query_params import ReinfolibQueryParams
from jproperty_collector.sources.reinfolib.endpoints import ReinfolibEndpoints
from logging import Logger
from typing import Any


class ReinfolibClient(DataSourceClient):
    
    BASE_URL = "https://www.reinfolib.mlit.go.jp"
    
    def __init__(self, logger: Logger, api_key: str, timeout: int = 30):
        if not api_key:
            raise ValidationError("API key is required for MLIT client")
            
        self.http_client = BaseHTTPClient(
            base_url=self.BASE_URL,
            api_key=api_key,
            timeout=timeout
        )
        self.formatter = ReinfolibDataFormatter()
        self.logger = logger
    
    def validate_params(self, params: ReinfolibQueryParams) -> bool:
        if not isinstance(params, ReinfolibQueryParams):
            raise ValidationError("Invalid parameter type for MLIT client")
        
        return True
    
    def fetch_property_transactions(
        self,
        params: ReinfolibQueryParams
    ) -> list[PropertyTransaction]:
        self.validate_params(params)
        
        api_params = params.to_api_params()
        
        self.logger.info(f"Fetching property data with params: {api_params}")
        
        try:
            response_data = self.http_client.get(
                ReinfolibEndpoints.PROPERTY_PRICES,
                params=api_params
            )

            transactions = []
            for item in response_data:
                try:
                    transaction = self.formatter.format_transaction(item)
                    if transaction:
                        transactions.append(transaction)
                except Exception as e:
                    self.logger.warning(f"Failed to format transaction data: {str(e)}")
                    continue
            
            self.logger.info(f"Successfully fetched {len(transactions)} transactions")
            return transactions
            
        except Exception as e:
            self.logger.error(f"Failed to fetch property transactions: {str(e)}")
            raise
    
    def fetch_municipalities(self, prefecture_code: str) -> list[dict[str, Any]]:
        if not prefecture_code or len(prefecture_code) != 2:
            raise ValidationError("Prefecture code must be 2 digits")
        
        try:
            response_data = self.http_client.get(
                ReinfolibEndpoints.MUNICIPALITIES,
                params={"area": prefecture_code}
            )
            return response_data if isinstance(response_data, list) else []
            
        except Exception as e:
            self.logger.error(f"Failed to fetch municipalities: {str(e)}")
            raise
