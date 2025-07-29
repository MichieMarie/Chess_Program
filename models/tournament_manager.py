import json
from pathlib import Path
from datetime import date
from typing import List, Optional

from .tournament import Tournament


class TournamentManager:
    """
    Manages tournament creation and updates.
    """

    def __init__(self, data_folder: str = "data/tournaments") -> None:
        datadir: Path = Path(data_folder)
        self.data_folder = datadir
        self.tournaments: List[Tournament] = []

        for filepath in datadir.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    with open(filepath) as f:
                        data: dict = json.load(f)
                    tournament = Tournament.from_dict(data, filepath=filepath)
                    self.tournaments.append(tournament)
                except json.JSONDecodeError:
                    print(filepath, "is invalid JSON file.")

    def create(
        self, name: str, start_date: date, end_date: date, venue: Optional[str] = None
    ) -> Tournament:
        """
        Create and save a new tournament to disk.

        Args:
            name (str): Tournament name.
            start_date (date): Start date of the tournament.
            end_date (date): End date of the tournament.
            venue (Optional[str]): Optional venue location.

        Returns:
            Tournament: The newly created Tournament object.
        """
        filepath = self.data_folder / name.replace(" ", "")
        filepath = filepath.with_suffix(".json")

        tournament = Tournament(
            name=name,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
            filepath=filepath,
        )
        tournament.save()
        self.tournaments.append(tournament)
        return tournament

    def get_all(self) -> List[Tournament]:
        return self.tournaments

    def get_by_name(self, name: str) -> Optional[Tournament]:
        for t in self.tournaments:
            if t.name == name:
                return t
        return None

    def active_tournament(self) -> Optional[Tournament]:
        for tournament in reversed(self.tournaments):
            if tournament.is_active():
                return tournament
        return None
