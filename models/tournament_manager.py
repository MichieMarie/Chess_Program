import json
from datetime import datetime
from pathlib import Path
import re
from typing import Optional

from .tournament import Tournament


class TournamentManager:
    """
    Manages loading, creating, and storing tournaments from disk.
    """

    def __init__(self, data_folder: str = "data/tournaments") -> None:
        """
        Initialize the manager and load tournaments from JSON files.

        Args:
            data_folder (str): Path to the folder containing tournament files.
        """
        project_root = Path(__file__).resolve().parents[1]
        datadir: Path = project_root / data_folder
        self.data_folder: Path = datadir
        self.tournaments: list[Tournament] = []

        if not datadir.exists():
            datadir.mkdir(parents=True, exist_ok=True)

        for filepath in datadir.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                        self.tournaments.append(Tournament.from_dict(data, filepath))
                except json.JSONDecodeError:
                    print(filepath, "is an invalid JSON file.")

    def _safe_filename(self, name: str) -> str:
        """
        Converts a tournament name into a safe filename by removing
        problematic characters and whitespace.
        """
        # Remove all characters except letters, numbers, hyphens, and underscores
        safe = re.sub(r"[^\w\-]", "", name)
        return safe.lower() + ".json"

    def create(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        venue: Optional[str] = None,
        num_rounds: int = 4,
    ) -> Tournament:
        """
        Create a new tournament and save it to disk.

        Args:
            name (str): Tournament name.
            start_date (date): Tournament start date.
            end_date (date): Tournament end date.
            venue (Optional[str]): Tournament venue.
            num_rounds (int): Total number of rounds.

        Returns:
            Tournament: The created and saved Tournament instance.
        """
        filepath: Path = self.data_folder / self._safe_filename(name)
        print(f"[DEBUG] Saving to file: {filepath.name}")

        tournament: Tournament = Tournament(
            name=name,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
            num_rounds=num_rounds,
            filepath=filepath,
        )
        tournament.save()
        self.tournaments.append(tournament)
        return tournament

    def get_all(self) -> list[Tournament]:
        """
        Return all loaded tournaments.
        """
        return self.tournaments
