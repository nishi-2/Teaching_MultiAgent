from collections import defaultdict
from typing import DefaultDict, List


class CoordinatorContextStore:
    """ Stores finding centrally for Coordinator-mediated context exchange. """

    def __init__(self) -> None:
        self._findings: DefaultDict[str, List[str]] = defaultdict(list)

    def add_finding(self, request_id: str, finding: str) -> None:
        """ Store a finding under the parent request ID """
        cleaned_finding = finding.strip()
        if cleaned_finding:
            self._findings[request_id].append(cleaned_finding)

    def get_findings(self, request_id: str) -> List[str]:
        """ Return a copy of findings for a request """
        return list(self._findings.get(request_id, []))

    def search_findings(self, request_id: str, topic: str) -> List[str]:
        """ Return findings containing the requested topic """
        normalized_topic = topic.strip().lower()
        if not normalized_topic:
            return self.get_findings(request_id)
        return [
            finding for finding in self.get_findings(request_id) if normalized_topic in finding.lower()
        ]