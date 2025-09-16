from dataclasses import dataclass
from jproperty_collector.core.models import QueryParams, Quarter
from .price_classification import PriceClassification


@dataclass
class ReinfolibQueryParams(QueryParams):
    year: int
    quarter: Quarter | None = None
    prefecture_code: str | None = None
    city_code: str | None = None
    station_code: str | None = None
    price_classification: PriceClassification | None = PriceClassification.BOTH
    
    def to_api_params(self) -> dict:
        params: dict[str, str | int] = {"year": self.year}
        
        if self.quarter:
            params["quarter"] = self.quarter.value
        if self.prefecture_code:
            params["area"] = self.prefecture_code
        if self.city_code:
            params["city"] = self.city_code
        if self.station_code:
            params["station"] = self.station_code
        if self.price_classification and self.price_classification != PriceClassification.BOTH:
            params["priceClassification"] = self.price_classification.value
            
        return params
