from dataclasses import dataclass, field
from typing import List

from .match import Match


@dataclass
class Round:
    """
    Represents one round of a tournament.

    Attributes:
        round_number (int): The number of the round in the tournament.
        matches (List[Match]): List of matches in the round.
        is_complete (bool): Whether the round has been completed.
    """

    round_number: int
    matches: List[Match] = field(default_factory=list)
    is_complete: bool = False

    @property
    def name(self) -> str:
        """
        Gets the display name of the round (e.g., 'Round 1').

        Returns:
            str: Display name of the round.
        """
        return f"Round {self.round_number}"

    def serialize(self) -> dict:
        """
        Serializes the round to a dictionary for JSON storage.

        Returns:
            dict: A dictionary with round number, match list, and status.
        """
        return {
            "round_number": self.round_number,
            "matches": [match.serialize() for match in self.matches],
            "is_complete": self.is_complete,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Round":
        """
        Deserializes a Round from a dictionary (used in JSON loading).

        Args:
            data (dict): Dictionary containing round information.

        Returns:
            Round: A new Round instance built from the given data.
        """
        if "round_number" not in data:
            raise ValueError("Invalid round format")
        return cls(
            round_number=data["round_number"],
            matches=data["matches"],
            is_complete=data.get("is_complete", False),
        )

    @classmethod
    def from_list(
        cls,
        match_data_list: List[dict],
        registrants_by_id: dict[str, dict],
        round_number: int,
    ) -> "Round":
        """
        Reconstructs a Round using tournament registrants instead of full Player objects.

        Args:
            match_data_list (List[dict]): Serialized match data.
            registrants_by_id (dict): Mapping of chess_id to registrant dictionaries.
            round_number (int): Round number label.

        Returns:
            Round: A new Round instance built from registrant data.
        """
        matches = []
        for data in match_data_list:
            p1_id, p2_id = data["players"]
            match = Match(
                player1=registrants_by_id[p1_id],
                player2=registrants_by_id[p2_id],
                winner=data.get("winner"),
                completed=data.get("completed", False),
            )
            matches.append(match)

        return cls(round_number=round_number, matches=matches)
