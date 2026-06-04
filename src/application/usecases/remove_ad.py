from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import RemoveAdPort


class RemoveAd(RemoveAdPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, ad_id: int) -> None:
        async with self._uow:
            # 1. Удаляем из индекса
            await self._uow.search.delete(ad_id)
            # 2. Фиксируем транзакцию
            await self._uow.commit()
