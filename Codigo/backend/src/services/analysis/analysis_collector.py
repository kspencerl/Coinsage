import datetime
import time
from typing import Any, List

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.analysis import Analysis
from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel
from src.models.schemas.analysis.analysis_info import AnalysisInfo, AnalysisInfoResponse, LastUpdate
from src.models.schemas.generic_pagination import PaginatedResponse
from src.repository.crud import analysis_info_repository, analysis_info_schedule_repository
from src.services.analysis.first_stage.closing_price_service import PriceService
from src.services.analysis.first_stage.week_percentage_val_service import WeekPercentageValorizationService
from src.services.currencies_info_collector import CurrenciesLogoCollector
from src.utilities.runtime import show_runtime


class AnalysisCollector:
    def __init__(self, session: Session):
        self.session = session
        self.symbols_service: CurrenciesLogoCollector = CurrenciesLogoCollector(session=session)
        self.repository = analysis_info_repository
        self.schedule_repository = analysis_info_schedule_repository

        # flows
        self.prices_service = PriceService(session=session)
        self.week_increse_service = WeekPercentageValorizationService(
            session=session, closing_price_service=self.prices_service
        )

    def _new_analysis(self) -> Analysis:
        analysis: Analysis = Analysis()
        self.session.add(analysis)
        self.session.commit()
        self.session.refresh(analysis)
        return analysis

    @show_runtime
    def start_analysis(self):
        logger.info(f"Starting analysis at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            new_analysis: Analysis = self._new_analysis()

            cryptos_str: List[str] = [crypto.symbol for crypto in self.symbols_service.get_cryptos().last_update.data]

            self.prices_service.collect(analysis_indentifier=new_analysis.uuid)
            self.week_increse_service.calculate_all_week_percentage_valorization(cryptos_str, new_analysis.uuid)

            self.session.add(AnalysisInfoScheduleModel(next_scheduled_time=self.calculate_next_time()))
            self.session.commit()
        except Exception as err:
            logger.error(f"Error on start_analysis: {err}")
            self.session.rollback()

    def calculate_next_time(self) -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(days=1)

    @show_runtime
    def get_last_analysis(self, limit: int, offset: int):
        last_analysis: Analysis | None = self.repository.get_last(self.session)
        schedule: AnalysisInfoScheduleModel | None = self.schedule_repository.get_last_update(self.session)

        if last_analysis and schedule:
            all_first_stage, paginated = self.prices_service.get_all_by_analysis_uuid(
                last_analysis.uuid, limit, offset
            )

            try:
                analysis = AnalysisInfo(
                    data=all_first_stage, total=paginated.total, remaining=paginated.remaining, page=paginated.page
                )
                return AnalysisInfoResponse(
                    next_update=schedule.next_scheduled_time,  # type: ignore
                    last_update=LastUpdate(time=last_analysis.date, data=analysis),  # type: ignore
                )
            except Exception as e:
                logger.error(f"Error on get_last_analysis: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on getting last analysis"
                )

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No analysis found")
