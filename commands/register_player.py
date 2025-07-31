import json
from pathlib import Path
from typing import List

from models import Player, Tournament

from .base import BaseCommand
from .context import Context


class RegisterPlayerCmd(BaseCommand):
    """
    Command to register a player to an active tournament by searching club records.

    Attributes:
        tournament (Tournament): The tournament players are registering into.
    """

    def __init__(self, tournament: Tournament) -> None:
        """
        Initialize the command with the given tournament.

        Args:
            tournament (Tournament): The tournament being updated.
        """
        self.tournament: Tournament = tournament

    def player_search(self) -> Context:
        """
        Search for a player by name or chess ID, then register them to the tournament. Saves tournament player
        registration to data/tournament.

        Returns:
            Context: The updated tournament view after successful registration.

        If no players are found, the user may choose to go to the club registration screen.
        """
        search: str = input("Enter player name or chess ID to search: ").strip().lower()

        if not search:
            print("No search entered. Returning to tournament view.")
            return Context("tournament-view", tournament=self.tournament)

        player_matches: List[Player] = []
        clubs_dir: Path = Path("data/clubs")

        for filepath in clubs_dir.glob("*.json"):
            with open(filepath) as f:
                data = json.load(f)
                club_name = data.get("name", "Unknown Club")
                for p_data in data.get("players", []):
                    if (
                        search in p_data["name"].lower()
                        or search == p_data["chess_id"].lower()
                    ):
                        player = Player(
                            name=p_data["name"],
                            email=p_data["email"],
                            chess_id=p_data["chess_id"],
                            birthday=p_data["birthday"],
                            club_name=club_name,
                        )
                        player_matches.append(player)

        if not player_matches:
            print("No players found.")
            answer: str = (
                input("Would you like to register a new player to a club? (y/n): ")
                .strip()
                .lower()
            )
            if answer == "y":
                return Context("club-create")
            return Context("tournament-view", tournament=self.tournament)

        print("\nMatching players:")
        for i, player in enumerate(player_matches, 1):
            print(f"{i}. {player.name} ({player.chess_id})")

        choice: str = input(
            "Enter the number of the player to register, or press Enter to cancel: "
        ).strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(player_matches)):
            print("Registration cancelled.")
            return Context("tournament-view", tournament=self.tournament)

        selected_player: Player = player_matches[int(choice) - 1]

        if any(
            p["chess_id"] == selected_player.chess_id for p in self.tournament.players
        ):
            print(f"{selected_player.name} is already registered.")
        else:
            self.tournament.players.append(
                Tournament.tournament_registrant(selected_player)
            )

            print(f"{selected_player.name} is registered for {self.tournament.name}.")
            self.tournament.save()

        return Context("tournament-view", tournament=self.tournament)

    def execute(self) -> Context:
        """
        Executes the player registration flow.

        Returns:
            Context: The tournament view after search and registration.
        """
        return self.player_search()
