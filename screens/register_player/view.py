from pathlib import Path
import json

from commands import NoopCmd
from models import Tournament

from ..base_screen import BaseScreen


class PlayerRegistrationView(BaseScreen):
    """
    Screen for viewing club members and registering them for a tournament.

    Loads players from club JSON files and allows user to register a player
    by direct selection, search, or navigating to the club management screen.
    """

    def __init__(self, tournament: Tournament):
        self.tournament = tournament
        self.players: list[dict[str, str]] = []

        club_dir = Path("data/clubs")
        for club_file in club_dir.glob("*.json"):
            try:
                with open(club_file, "r") as f:
                    club_data = json.load(f)
                    club_name = club_data.get("name", "Unknown Club")
                    for player in club_data.get("players", []):
                        player["club_name"] = club_name
                        self.players.append(player)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"‼️ Failed to load club file: {club_file}")

    def display_players(self) -> None:
        print("\n♟️ Registration Page ♟️\n")
        print("Available players:")
        for i, p in enumerate(self.players, 1):
            print(f"{i}. {p['name']} ({p['chess_id']}) - {p['club_name']}")

    def display_menu(self) -> NoopCmd:
        """
        Prompts for the next action from the user.

        Options:
            Search by name or Chess ID
            Select player
            Navigate to club management system
            Return to view/manage tournament

        Returns:
            NoopCmd: The next command to execute.
        """
        while True:
            print()
            self.display_players()
            print()
            print("\nPlease select your action from the options below:")
            print("F - Search by name or Chess ID")
            print(
                "# - Enter the number of a player to register them for this tournament."
            )
            print("C - If player not found, add them via club management menu.")
            print(f"V - Return to view/manage {self.tournament.name}")
            print("T - Return to tournaments main menu")

            choice = self.input_string("Choice").strip().upper()

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.players):
                    selected = self.players[index]
                    if any(
                        p["chess_id"] == selected["chess_id"]
                        for p in self.tournament.players
                    ):
                        input(
                            f"✅ {selected['name']} is already registered. "
                            f"Press Enter to select a different player."
                        )
                        continue

                    return NoopCmd(
                        "register-player-confirm",
                        tournament=self.tournament,
                        player=selected,
                    )
                else:
                    print("❗ Invalid player number.")
                continue

            if choice == "C":
                print("\nSwitching to Club Management system to add a new player...\n")
                return NoopCmd("main-menu")

            if choice == "V":
                return NoopCmd("tournament-view", tournament=self.tournament)

            if choice == "T":
                return NoopCmd("tournaments-main")

            if choice == "F":
                while True:
                    query = (
                        self.input_string(
                            "♟️Enter Chess ID or part of name (or press Enter to cancel)"
                        )
                        .strip()
                        .lower()
                    )
                    if not query:
                        break

                    results = [
                        p
                        for p in self.players
                        if query in p["chess_id"].lower() or query in p["name"].lower()
                    ]

                    if not results:
                        print("\n❗ No players matched your search.\n")
                        continue

                    print("\nSearch Results:\n")
                    for i, p in enumerate(results, 1):
                        print(f"{i}. {p['name']} ({p['chess_id']}) - {p['club_name']}")

                    selection = self.input_string(
                        "#️⃣#️⃣ Enter number to select, or press Enter to cancel"
                    ).strip()
                    if not selection:
                        break

                    if selection.isdigit():
                        index = int(selection) - 1
                        if 0 <= index < len(results):
                            selected = results[index]
                            if any(
                                p["chess_id"] == selected["chess_id"]
                                for p in self.tournament.players
                            ):
                                input(
                                    f"✅ {selected['name']} is already registered. "
                                    f"Press Enter to select a different player."
                                )
                                continue

                            return NoopCmd(
                                "register-player-confirm",
                                tournament=self.tournament,
                                player=selected,
                            )
                    print(
                        "‼️Invalid input. Please choose a valid option from menu above."
                    )
        print("‼️ Unexpected exit from registration. Returning to tournament view.")
        return NoopCmd("tournament-view", tournament=self.tournament)
