from dependency_injector import containers, providers

from src.database.adapters.sql_cashier_repository import SQLCashierRepository
from src.database.adapters.sql_item_repository import SQLItemRepository
from src.database.adapters.sql_shop_repository import SQLShopRepository
from src.database.engine import create_db_engine, create_db_session_factory


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection Container for UserDataService.

    Manages all application dependencies including database connections,
    repositories, and domain services. Follows singleton pattern to avoid duplicating essential objects.
    """

    config = providers.Configuration()

    engine = providers.Singleton(
        create_db_engine,
        db_url=config.db_url,
        echo=True
    )

    session_factory = providers.Singleton(
        create_db_session_factory,
        engine=engine
    )

    shop_repository = providers.Singleton(
        SQLShopRepository,
        session_factory=session_factory
    )

    cashier_repository = providers.Singleton(
        SQLCashierRepository,
        session_factory=session_factory
    )

    item_repository = providers.Singleton(
        SQLItemRepository,
        session_factory=session_factory
    )


