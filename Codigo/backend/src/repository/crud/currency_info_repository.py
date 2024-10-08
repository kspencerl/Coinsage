from typing import List

from loguru import logger
from sqlalchemy import or_, select, Uuid
from sqlalchemy.orm import Session

from src.models.db import currency_base_info
from src.models.db.rel_setor_currency_base_info import SetorCurrencyBaseInfo
from src.models.schemas import currency_info
from src.utilities.runtime import show_runtime


def get_by_match(db: Session, match: str) -> List[currency_base_info.CurrencyBaseInfoModel | None]:
    return db.execute(
        select(currency_base_info.CurrencyBaseInfoModel).where(
            or_(
                currency_base_info.CurrencyBaseInfoModel.name.ilike(f"{match}%"),
                currency_base_info.CurrencyBaseInfoModel.name.ilike(f"% {match}%"),
                currency_base_info.CurrencyBaseInfoModel.symbol.ilike(f"{match}%"),
                currency_base_info.CurrencyBaseInfoModel.cmc_slug.ilike(f"{match}%"),
            )
        )
    ).scalars()


def get_crypto(db: Session, crypto_uuid: Uuid) -> currency_base_info.CurrencyBaseInfoModel | None:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.uuid == crypto_uuid)
        .first()
    )


def get_currency_info_by_uuid(db: Session, uuid_value: Uuid) -> currency_base_info.CurrencyBaseInfoModel | None:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.uuid == uuid_value)
        .first()
    )


def get_cryptos(db: Session, skip: int = 0, limit: int = 10000) -> list[currency_base_info.CurrencyBaseInfoModel]:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.active == True)
        .all()
    )


def get_currency_info_by_symbol(db: Session, symbol: str) -> currency_base_info.CurrencyBaseInfoModel | None:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.symbol == symbol)
        .first()
    )


def create_crypto(db: Session, crypto: currency_info.CurrencyInfo) -> currency_base_info.CurrencyBaseInfoModel:
    currency = currency_base_info.CurrencyBaseInfoModel(
        symbol=crypto.symbol,
        cmc_id=crypto.cmc_id,
        cmc_slug=crypto.cmc_slug,
        logo=crypto.logo,
        name=crypto.name,
        description=crypto.description,
        technical_doc=crypto.technical_doc,
        urls=crypto.urls,
    )
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency


def clear_table(db: Session) -> None:
    db.query(currency_base_info.CurrencyBaseInfoModel).delete()


def get_coins_by_sector(db: Session, sector_uuid: Uuid) -> List[currency_base_info.CurrencyBaseInfoModel]:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .join(
            SetorCurrencyBaseInfo, SetorCurrencyBaseInfo.uuid_currency == currency_base_info.CurrencyBaseInfoModel.uuid
        )
        .filter(SetorCurrencyBaseInfo.uuid_setor == sector_uuid)
        .all()
    )


def clear_inactive(db: Session, cmc_symbols: List[str]) -> None:
    symbols = (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.symbol.notin_(cmc_symbols))
        .all()
    )

    logger.warning(f"Clearing {len(symbols)} inactive symbols {[symbol.symbol for symbol in symbols]}")

    for symbol in symbols:
        symbol.active = False

    db.commit()
