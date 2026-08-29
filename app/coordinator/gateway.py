from abc import ABC, abstractmethod
from typing import List
from app.domain.messages import CoordinatorTask, SubagentResult


class CoordinatorGateway(ABC):
    """ Restricted communication channel available to subagents. """

    @abstractmethod
    def submit_finding(self, task_id: str, finding: str) -> None:
        """ Send finding to the coordinator """
        raise NotImplementedError


    @abstractmethod
    def request_context(self, task_id: str, topic:str) -> List[str]:
        """ Request approved findings collected by the coordinator """
        raise NotImplementedError


    @abstractmethod
    def request_follow_up(self, task: CoordinatorTask, objective: str) -> SubagentResult:
        """ Ask the coordinator to arrange additional work """
        raise NotImplementedError