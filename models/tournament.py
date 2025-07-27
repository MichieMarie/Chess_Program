from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime
from pathlib import Path
import json

from .player import Player
from .round import Round


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
    rounds: List[Round] = field(default_factory=list)
    current_round_index: Optional[int] = None

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
            "players": [p.serialize() for p in self.players],
            "rounds": [rnd.serialize() for rnd in self.rounds],
            "current_round_index": self.current_round_index,
        }

    @classmethod
    def from_dict(cls, data: dict, filepath: Optional[Path] = None) -> "Tournament":
        # Convert player dicts into Player objects
        player_objs = [Player(**p) for p in data.get("players", [])]
        players_by_id = {p.chess_id: p for p in player_objs}

        # Rebuild rounds using players_by_id for match references
        rounds = [
            Round.from_list(rnd_data, players_by_id, round_number=i + 1)
            for i, rnd_data in enumerate(data.get("rounds", []))
        ]

        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]).date(),
            end_date=datetime.fromisoformat(data["end_date"]).date(),
            venue=data.get("venue"),
            players=player_objs,
            rounds=rounds,
            current_round_index=data.get("current_round_index"),
            filepath=filepath,
        )

    def get_player_scores(self) -> dict[Player, float]:
        """
        Returns a dictionary of total points per player in the tournament.
        Uses match.get_points() to calculate each player's score.
        """
        scores = {p.chess_id: 0.0 for p in self.players}

        for rnd in self.rounds:
            for match in rnd.matches:
                for player in (match.player1, match.player2):
                    scores[player.chess_id] += match.get_points(player)

        return scores
