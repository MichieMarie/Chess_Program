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
    """

    round_number: int
    matches: List[Match] = field(default_factory=list)
    is_complete: bool = False

    def name(self) -> str:
        """
        Gets the display name of the round.

        Returns:
            str: A string like 'Round 1'.
        """
        return f"Round {self.round_number}"

    def serialize(self) -> List[dict]:
        """
        Serializes the matches in this round to a list of dictionaries,
        suitable for JSON storage.

        Returns:
            List[dict]: A list of serialized match dictionaries.
        """
        return [match.serialize() for match in self.matches]

    @classmethod
    def from_list(
        cls, match_data_list: List[dict], players_by_id: dict, round_number: int
    ) -> "Round":
        """
        Reconstructs a Round from serialized match data and a player lookup.

        Args:
            match_data_list (List[dict]): List of serialized match data.
            players_by_id (dict): Mapping of player chess IDs to Player objects.
            round_number (int): The round number to assign.

        Returns:
            Round: A Round object reconstructed from the provided data.
        """
        matches = [Match.from_dict(md, players_by_id) for md in match_data_list]
        return cls(round_number=round_number, matches=matches)
