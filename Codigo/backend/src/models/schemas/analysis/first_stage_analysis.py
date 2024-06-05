from datetime import datetime
from uuid import UUID

from sqlalchemy import Enum

from src.models.schemas.base import BaseSchemaModel
from src.models.schemas.sector import SectorRead


class AnalysisCurrencyInfo(BaseSchemaModel):
    symbol: str
    uuid: UUID
    logo: str
    main_sector: SectorRead


class FirstStageAnalysisResponse(BaseSchemaModel):
    currency: AnalysisCurrencyInfo
    week_increase_percentage: float | None
    valorization_date: datetime | None
    closing_price: float | None
    open_price: float | None
    last_week_closing_price: float | None
    ema8: float | None
    ema8_greater_open: bool | None
    ema8_less_close: bool | None
    ema_aligned: bool | None
    market_cap: float | None
    ranking: int | None
    current_price: float | None
    increase_volume_day: datetime | None
    increase_volume: float | None
    today_volume: float
    volume_before_increase: float | None


class VolumeAnalysis(BaseSchemaModel):
    symbol: str
    volume_before_increase: float | None
    increase_volume_day: datetime | None
    expressive_volume_increase: bool
    increase_volume: float | None
    today_volume: float
