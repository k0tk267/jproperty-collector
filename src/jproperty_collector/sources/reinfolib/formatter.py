from typing import Any
from jproperty_collector.core.models.property_transaction import PropertyTransaction

class ReinfolibDataFormatter:
    
    def format_transaction(self, raw_data: dict[str, Any]) -> PropertyTransaction | None:
        try:
            return PropertyTransaction(
                trade_price=self._safe_int(raw_data.get("TradePrice")),
                area=self._safe_float(raw_data.get("Area")),
                unit_price=self._safe_int(raw_data.get("UnitPrice")),
                transaction_period=raw_data.get("Period"),
                prefecture=raw_data.get("Prefecture"),
                municipality=raw_data.get("Municipality"),
                district_name=raw_data.get("DistrictName"),
                floor_plan=raw_data.get("FloorPlan"),
                building_year=raw_data.get("BuildingYear"),
                structure=raw_data.get("Structure"),
                total_floor_area=self._safe_float(raw_data.get("TotalFloorArea")),
                land_shape=raw_data.get("LandShape"),
                frontage=self._safe_float(raw_data.get("Frontage")),
                purpose=raw_data.get("Purpose"),
                city_planning=raw_data.get("CityPlanning"),
            )
        except Exception as e:
            return None
    
    @staticmethod
    def _safe_int(value: Any) -> int | None:
        if value is None or value == "":
            return None
        try:
            return int(str(value).replace(",", ""))
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _safe_float(value: Any) -> float | None:
        if value is None or value == "":
            return None
        try:
            return float(str(value).replace(",", ""))
        except (ValueError, TypeError):
            return None

