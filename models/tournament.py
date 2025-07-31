from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json

from .match import Match, PLAYER1, PLAYER2, DRAW
from .round import Round
from .player import Player


@dataclass
class Tournament:
    name: str
    start_date: datetime
    end_date: datetime
    venue: str
    players: List[dict[str, str]] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    current_round_index: int = -1
    num_rounds: int = 4
    filepath: Optional[Path] = None
    is_complete: bool = False

    @staticmethod
    def tournament_registrant(player: Player) -> dict[str, str]:
        """
        Extracts minimal tournament registration info from a full Player object.

        Args:
            player (Player): A Player instance.

        Returns:
            dict[str, str]: Dictionary with name, club_name, and chess_id.
        """
        return {
            "name": player.name,
            "chess_id": player.chess_id,
            "club_name": player.club_name,
        }

    @staticmethod
    def tournament_players(players: List[Player]) -> List[dict[str, str]]:
        """
        Converts a list of Player objects into tournament registration format.

        Args:
            players (List[Player]): List of Player instances.

        Returns:
            List[dict[str, str]]: Simplified player info for tournament storage.
        """
        return [Tournament.tournament_registrant(p) for p in players]

    def player_scores(self) -> dict[str, float]:
        """
        Calculates total tournament points for each player.

        Returns:
            dict[str, float]: Dictionary mapping player chess_id to cumulative score.
        """
        scores: dict[str, float] = {p["chess_id"]: 0.0 for p in self.players}

        for rnd in self.rounds:
            for match in rnd.matches:
                if match.winner == DRAW:
                    scores[match.player1.chess_id] += 0.5
                    scores[match.player2.chess_id] += 0.5
                elif match.winner == PLAYER1:
                    scores[match.player1.chess_id] += 1.0
                elif match.winner == PLAYER2:
                    scores[match.player2.chess_id] += 1.0

        return scores

    def to_dict(self) -> dict:
        """
        Converts the tournament to a dictionary suitable for JSON serialization.
        """
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "venue": self.venue,
            "players": self.players,
            "rounds": [rnd.serialize() for rnd in self.rounds],
            "current_round_index": self.current_round_index,
            "num_rounds": self.num_rounds,
            "is_complete": self.is_complete,
        }

    @classmethod
    def from_dict(cls, data: dict, filepath: Optional[Path] = None) -> Tournament:
        """
        Create a Tournament instance from a dictionary (e.g., loaded from JSON).
        Handles both modern and legacy round formats.

        Args:
            data (dict): The dictionary of tournament data.
            filepath (Optional[Path]): Filepath to the tournament file.

        Returns:
            Tournament: The reconstructed Tournament instance.
        """
        players: List[dict[str, str]] = data.get("players", [])

        raw_rounds = data.get("rounds", [])
        rounds: List[Round] = []

        if raw_rounds and isinstance(raw_rounds[0], list):
            # Legacy format: list of match dicts per round
            for idx, match_list in enumerate(raw_rounds, start=1):
                matches = []
                for m in match_list:
                    p1_id, p2_id = m["players"]
                    winner = m.get("winner")

                    # Determine result string (for our app's format)
                    if winner is None:
                        result = DRAW
                    elif winner == p1_id:
                        result = PLAYER1
                    elif winner == p2_id:
                        result = PLAYER2
                    else:
                        result = None  # fallback

                    match = Match(
                        player1=Player(
                            name="", email="", chess_id=p1_id, birthday="", club_name=""
                        ),
                        player2=Player(
                            name="", email="", chess_id=p2_id, birthday="", club_name=""
                        ),
                        winner=result,
                    )
                    matches.append(match)

                rounds.append(Round(matches=matches, round_number=idx))
        else:
            # Current format
            rounds = [Round.deserialize(rdata) for rdata in raw_rounds]

        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            venue=data["venue"],
            players=players,
            rounds=rounds,
            current_round_index=data.get("current_round_index", -1),
            num_rounds=data.get("num_rounds", 4),
            filepath=filepath,
            is_complete=data.get("is_complete", False),
        )

    def save(self) -> None:
        """
        Save the current tournament state to its JSON file.
        """
        if not self.filepath:
            raise ValueError("No filepath provided for saving.")
        with open(self.filepath, "w") as f:
            json.dump(self.to_dict(), f, default=str, indent=2)

        print(f"[DEBUG] Saving tournament to: {self.filepath}")
