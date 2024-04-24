from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.models.schemas.analysis.first_stage_analysis import FirstStageAnalysisResponse
from src.models.schemas.base import BaseSchemaModel


class AnalysisInfo(BaseSchemaModel):
    page: int
    total: int
    remaining: int
    data: List[FirstStageAnalysisResponse]


class LastUpdate(BaseSchemaModel):
    time: datetime
    data: AnalysisInfo


class AnalysisInfoResponse(BaseSchemaModel):
    next_update: datetime | None
    last_update: LastUpdate
