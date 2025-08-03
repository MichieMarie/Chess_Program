from pathlib import Path
import json

from models import Tournament
from commands import Context

from ..base_screen import BaseScreen


class PlayerRegistrationView(BaseScreen):
    """Screen for viewing club members and registering them for a tournament."""

    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.players: list[dict] = []

        club_dir = Path("data/clubs")
        for club_file in club_dir.glob("*.json"):
            try:
                with open(club_file, "r") as f:
                    club_data = json.load(f)
                    club_name = club_data.get("name", "Unknown Club")
                    for player in club_data.get("players", []):
                        # Include club name in each player dict
                        player["club_name"] = club_name
                        self.players.append(player)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"[!] Failed to load club file: {club_file}")

    def display_players(self) -> None:
        print("\nAvailable Players:\n")
        for i, p in enumerate(self.players, 1):
            print(f"{i}. {p['name']} ({p['chess_id']}) - {p['club_name']}")

    def get_command(self):
        """Prompts for the next action from the user."""
        while True:
            print()
            self.display_players()
            print()
            print("\nPlease select your action from the options below:")
            print("F - Search by name or Chess ID")
            print(
                "# - Enter the number of a player to register them for this tournament."
            )
            print("C - If player not found, add them via Club Management")
            print("V - Return to View/Manage Tournament")
            print("T - Return to Tournament Menu")

            choice = self.input_string("Choice").strip().upper()

            if choice == "C":
                print("\nSwitching to Club Management system to add a new player...\n")
                return NoopCmd("main-menu")

            if choice == "V":
                return Context("tournament-view", tournament=self.tournament)

            if choice == "T":
                return Context("tournaments-main")

            if choice == "F":
                while True:
                    query = (
                        self.input_string(
                            "Enter Chess ID or part of name (or press Enter to cancel)"
                        )
                        .strip()
                        .lower()
                    )
                    if not query:
                        break  # Cancel search

                    results = [
                        p
                        for p in self.players
                        if query in p["chess_id"].lower() or query in p["name"].lower()
                    ]

                    if not results:
                        print("\nNo players matched your search.\n")
                        continue  # Go back to the search input

                    print("\nSearch Results:\n")
                    for i, p in enumerate(results, 1):
                        print(f"{i}. {p['name']} ({p['chess_id']}) - {p['club_name']}")

                    selection = self.input_string(
                        "Enter number to select, or press Enter to cancel"
                    ).strip()
                    if not selection:
                        break  # Cancel selection

                    if selection.isdigit():
                        index = int(selection) - 1
                        if 0 <= index < len(results):
                            return Context(
                                "register-player-confirm",
                                tournament=self.tournament,
                                player=results[index],
                            )

                    print("Invalid input. Please choose a valid option.")
