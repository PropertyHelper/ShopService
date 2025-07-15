import uuid

from sqlalchemy import select

from src.core.models import Item
from src.core.ports.abstract_item_repository import AbstractItemRepository
from src.database.adapters.sql_base_class import SQLBaseClass
from src.database.models import Item as ItemModel


def transform_item_model_to_domain(item_model: ItemModel) -> Item:
    return Item(
        iid=item_model.iid,
        name=item_model.name,
        description=item_model.description,
        photo_url=item_model.photo_url,
        price=item_model.price,
        percent_point_allocation=item_model.percent_point_allocation,
        shop_id=item_model.shop_id
    )


class SQLItemRepository(SQLBaseClass, AbstractItemRepository):
    async def save_item(self, item: Item) -> None:
        await self.save_items([item])

    async def get_all_items_by_shop_id(self, shop_id: uuid.UUID) -> list[Item]:
        async with self.get_session() as session:
            stmt = select(ItemModel).where(ItemModel.shop_id == shop_id)
            result = await session.execute(stmt)
            items = [transform_item_model_to_domain(item) for item in result.scalars().all()]
            return items

    async def get_item(self, item_id: uuid.UUID) -> Item:
        async with self.get_session() as session:
            stmt = select(ItemModel).where(ItemModel.iid == item_id)
            result = await session.execute(stmt)
            item = result.scalar_one_or_none()
            if item is None:
                raise ValueError("Item does not exist")
            return transform_item_model_to_domain(item)

    async def save_items(self, items: list[Item]) -> None:
        models = [None] * len(items)
        for idx, item in enumerate(items):
            models[idx] = ItemModel(iid=item.iid,
                                    name=item.name,
                                    description=item.description,
                                    photo_url=item.photo_url,
                                    price=item.price,
                                    percent_point_allocation=item.percent_point_allocation,
                                    shop_id=item.shop_id)
        async with self.get_session() as session:
            session.add_all(models)
            await session.commit()

    async def get_items(self, item_id_list: list[uuid.UUID]) -> list[Item]:
        async with self.get_session() as session:
            stmt = select(ItemModel).where(ItemModel.iid.in_(item_id_list))
            result = await session.execute(stmt)
            items = result.scalars().all()
            return [transform_item_model_to_domain(item) for item in items]
