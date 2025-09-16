import pandas as pd
from jproperty_collector.core.models.property_transaction import PropertyTransaction
from typing import Any

class DataFrameFormatter:
    
    @staticmethod
    def to_dataframe(transactions: list[PropertyTransaction]) -> pd.DataFrame:
        if not transactions:
            return pd.DataFrame()
        
        data = []
        for transaction in transactions:
            data.append({
                'trade_price': transaction.trade_price,
                'area': transaction.area,
                'unit_price': transaction.unit_price,
                'transaction_period': transaction.transaction_period,
                'prefecture': transaction.prefecture,
                'municipality': transaction.municipality,
                'district_name': transaction.district_name,
                'floor_plan': transaction.floor_plan,
                'building_year': transaction.building_year,
                'structure': transaction.structure,
                'total_floor_area': transaction.total_floor_area,
                'land_shape': transaction.land_shape,
                'frontage': transaction.frontage,
                'purpose': transaction.purpose,
                'city_planning': transaction.city_planning,
            })
        
        return pd.DataFrame(data)
