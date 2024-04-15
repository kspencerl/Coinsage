from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.analysis.analysis_info import AnalysisInfoResponse
from src.services.analysis.analysis_collector import AnalysisCollector
from src.services.sectors_info_collector import SectorsCollector

router = APIRouter(prefix="/edwin_method", tags=["edwin_method"])


@router.get(
    path="/",
    name="edwin_method:read-last-analysis",
    response_model=AnalysisInfoResponse,
    description="Coletar dados da última análise.",
    status_code=status.HTTP_200_OK,
)
async def get_accounts(
    db: Session = Depends(get_db), limit: int = Query(20, ge=0), offset: int = Query(0, ge=0)
) -> AnalysisInfoResponse:
    return AnalysisCollector(session=db).get_last_analysis(limit, offset)
