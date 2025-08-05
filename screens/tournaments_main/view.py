from commands import BaseCommand, NoopCmd, TournamentListCmd
from models import Tournament

from ..base_screen import BaseScreen


class TournamentsMainView(BaseScreen):
    """
    Screen for viewing all tournaments and selecting an action.
    """

    def __init__(self) -> None:
        context = TournamentListCmd().execute()
        self.tournaments: list[Tournament] = context.kwargs.get("tournaments", [])

    def display(self) -> None:
        """
        Displays a list of tournaments and options to manage them.
        """
        if not self.tournaments:
            print("\nNo tournaments available.\n")
        else:
            self.display_tournaments(self.tournaments)

    def display_tournaments(self, tournaments: list[Tournament]) -> None:
        """
        Prints a list of tournaments with their name, venue, date range, and status.

        Args:
            tournaments (list[Tournament]): List of tournaments to display.
        """
        print("\n♟️Tournaments Menu♟️")
        print("\nAvailable Tournaments:\n")
        for i, t in enumerate(tournaments, 1):
            start = t.start_date.strftime("%d-%b-%Y")
            end = t.end_date.strftime("%d-%b-%Y")
            print(f"{i}. {t.name} — {t.venue} ({start} to {end}) {t.status_label}")
            if t.is_overdue:
                print(
                    f"‼️ Warning: {t.name} has ended, but one or more rounds remain open."
                )
                print("   Complete by submitting match results or advancing the round.")

    def get_command(self) -> BaseCommand:
        """
        Prompts the user to select an action and returns the appropriate command.

        Options:
            Select a tournament.
            Create a new tournament.
            Return to program menu.

        Returns:
            BaseCommand: The next command to execute.
        """
        print("\nPlease select your action from the options below:")
        print()
        print("# - Enter the number of a tournament to view/manage it")
        print("N - Create a new tournament")
        print("B - Return to program main menu")

        while True:
            choice = self.input_string("Choice").strip().upper()

            if choice == "B":
                return NoopCmd("app-main")

            if choice == "N":
                return NoopCmd("tournament-create")

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.tournaments):
                    selected = self.tournaments[index]
                    return NoopCmd("tournament-view", tournament=selected)

            print(
                "‼️ Invalid input. Please enter a valid number (e.g. 1, 2, 3...), N, or B."
            )
