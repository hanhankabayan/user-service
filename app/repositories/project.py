from abc import ABC, abstractmethod

from app.models.project import Project


class AbstractProjectRepository(ABC):
    @abstractmethod
    async def find_by_id(self, project_id: int) -> Project | None:
        pass
