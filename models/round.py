from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from .match import Match


@dataclass
class Round:
    round_number: int
    matches: List[Match] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def is_complete(self) -> bool:
        """Returns True if all matches in this round are completed."""
        return all(match.completed for match in self.matches)

    def name(self) -> str:
        """Returns a display name like 'Round 1'."""
        return f"Round {self.round_number}"

    def start(self):
        """Marks the round as started."""
        self.start_time = datetime.now()

    def end(self):
        """Marks the round as completed (timestamp only). Use is_complete() to check match status."""
        self.end_time = datetime.now()

    def serialize(self) -> List[dict]:
        """Serialize matches for saving to JSON."""
        return [match.serialize() for match in self.matches]

    @classmethod
    def from_list(
        cls, match_data_list: List[dict], players_by_id: dict, round_number: int
    ) -> "Round":
        matches = [Match.from_dict(md, players_by_id) for md in match_data_list]
        return cls(round_number=round_number, matches=matches)
