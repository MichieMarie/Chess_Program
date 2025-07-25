import json
from pathlib import Path
from datetime import date
from typing import List, Optional

from .tournament import Tournament


class TournamentManager:
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

    def create(self, name: str) -> Tournament:
        filepath = self.data_folder / name.replace(" ", "")
        filepath = filepath.with_suffix(".json")
        today: date = date.today()

        # TODO: Replace hardcoded dates with user input from create_tournament.py
        tournament = Tournament(
            name=name, start_date=today, end_date=today, filepath=filepath
        )
        tournament.save()

        self.tournaments.append(tournament)
        return tournament

    def save(self, tournament: Tournament) -> None:
        tournament.save()

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
