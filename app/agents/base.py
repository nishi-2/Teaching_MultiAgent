from abc import ABC, abstractmethod

from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult

class BaseSubagent(ABC):
    name: str

    @abstractmethod
    def run(self, task: CoordinatorTask, coordinator: CoordinatorGateway) -> SubagentResult:
        ''' Execute the assigned task and return the result to the coordinator '''
        raise NotImplementedError