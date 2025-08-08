from commands import NoopCmd
from models import Tournament
from ..base_screen import BaseScreen


class EditTournamentView(BaseScreen):
    """
    Screen for editing tournament details before it begins.
    Allows updating name, venue, start/end dates, removing players, or deleting the tournament.
    """

    def __init__(self, tournament: Tournament):
        self.tournament = tournament

    def display(self) -> None:
        """
        Displays tournament details and tournament edit options.
        """
        print(f"\n♟️Editing Tournament: {self.tournament.name}♟️")
        print(f"Venue: {self.tournament.venue}")
        print(
            f"Dates: {self.tournament.start_date.strftime('%d-%b-%Y')} "
            f"to {self.tournament.end_date.strftime('%d-%b-%Y')}"
        )
        print(f"\nRegistered Players: {len(self.tournament.players)}")
        for i, p in enumerate(self.tournament.players, 1):
            print(f"{i}. {p['name']} ({p['chess_id']}) - {p['club_name']}")

    def display_menu(self) -> NoopCmd:
        """
        Prompts the user to select an action and returns the appropriate command.

        Edit options include tournament name, venue, start/end dates, number of rounds,
        removing a registered player, or deleting the tournament.

        Returns:
            NoopCmd: The next command to execute.
        """
        while True:
            print("\nPlease select your action from the options below:")
            print("N - Change tournament name")
            print("L - Change venue name")
            print("D - Change start/end dates")
            print("R - Change number of rounds")
            print("P - Remove a registered player")
            print("X - Delete the tournament")
            print(f"V - Return to view/manage {self.tournament.name}")

            choice = self.input_string("Choice").strip().upper()

            if choice == "N":
                new_name = self.input_string(
                    "New tournament name", default=self.tournament.name
                )
                self.tournament.name = new_name
                self.tournament.save()

            elif choice == "L":
                new_venue = self.input_string(
                    "New venue", default=self.tournament.venue
                )
                self.tournament.venue = new_venue
                self.tournament.save()

            elif choice == "R":
                new_rounds = self.input_rounds(
                    "Number of rounds", default=str(self.tournament.num_rounds)
                )
                self.tournament.num_rounds = new_rounds
                self.tournament.save()

            elif choice == "D":
                new_start = self.input_tournament_dates(prompt="New start date")
                new_end = self.input_tournament_dates(prompt="New end date")
                self.tournament.start_date = new_start
                self.tournament.end_date = new_end
                self.tournament.save()

            elif choice == "P":
                if not self.tournament.players:
                    print("\n❎ No players to remove.")
                else:
                    for i, p in enumerate(self.tournament.players, 1):
                        print(f"{i}. {p['name']} ({p['chess_id']}) - {p['club_name']}")
                    selection = self.input_string(
                        "#️⃣#️⃣ Enter number to remove, or press Enter to cancel"
                    ).strip()
                    if selection.isdigit():
                        index = int(selection) - 1
                        if 0 <= index < len(self.tournament.players):
                            removed = self.tournament.players.pop(index)
                            self.tournament.save()
                            print(f"✅ {removed['name']} has been removed.")

            elif choice == "X":
                confirm = self.input_string(
                    "‼️ Are you sure you want to delete this tournament? Type YES to confirm"
                ).strip()
                if confirm == "YES":
                    path = self.tournament.filepath
                    if path and path.exists():
                        path.unlink()
                        print("✅ Tournament deleted.")
                    else:
                        print("‼️ Tournament file not found.")
                    return NoopCmd("tournaments-main")

            elif choice == "V":
                return NoopCmd("tournament-view", tournament=self.tournament)

            else:
                print("❗ Invalid input. Choose from one of the options above.")
