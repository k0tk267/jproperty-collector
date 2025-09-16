from dataclasses import dataclass

@dataclass
class PropertyTransaction:
    trade_price: int | None = None
    area: float | None= None
    unit_price: int | None = None
    transaction_period: str | None = None
    prefecture: str | None = None
    municipality: str | None = None
    district_name: str | None = None
    floor_plan: str | None = None
    building_year: str | None = None
    structure: str | None = None
    total_floor_area: float | None = None
    land_shape: str | None = None
    frontage: float | None = None
    purpose: str | None = None
    city_planning: str | None = None
