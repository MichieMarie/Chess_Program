from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime
from pathlib import Path
import json

from .player import Player


@dataclass
class Tournament:
    """
    Represents a local chess tournament.
    Holds metadata and structure but does not perform logic like matchmaking.
    """

    name: str
    start_date: date
    end_date: date
    venue: Optional[str] = None
    players: List[Player] = field(default_factory=list)
    rounds: List[dict] = field(
        default_factory=list
    )  # Replace dict with Round type if modeled
    current_round_index: Optional[int] = None  # Tracks which round is active

    filepath: Optional[Path] = None  # For saving to disk

    def is_active(self) -> bool:
        today: date = date.today()
        return self.start_date <= today <= self.end_date

    def is_complete(self) -> bool:
        return date.today() > self.end_date

    def save(self) -> None:
        if not self.filepath:
            raise ValueError("No filepath provided for saving.")
        with open(self.filepath, "w") as f:
            json.dump(self.to_dict(), f, default=str, indent=2)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "venue": self.venue,
            "players": [p.serialize() for p in self.players],  # ✅ serialize players
            "rounds": self.rounds,
            "current_round_index": self.current_round_index,
        }

    @classmethod
    def from_dict(cls, data: dict, filepath: Optional[Path] = None) -> "Tournament":
        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]).date(),
            end_date=datetime.fromisoformat(data["end_date"]).date(),
            venue=data.get("venue"),
            players=[
                Player(**p) for p in data.get("players", [])
            ],  # ✅ deserialize players
            rounds=data.get("rounds", []),
            current_round_index=data.get("current_round_index"),
            filepath=filepath,
        )
