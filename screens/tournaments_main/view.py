from commands import NoopCmd, TournamentListCmd
from models import Tournament

from ..base_screen import BaseScreen


class TournamentsMainView(BaseScreen):
    """
    Screen for viewing all tournaments and selecting an action.
    """

    def display(self) -> None:
        """
        Displays a list of tournaments and options to manage them.
        """
        context = TournamentListCmd().execute()
        tournaments: list[Tournament] = context.kwargs.get("tournaments", [])

        if not tournaments:
            print("\nNo tournaments found.\n")
        else:
            self.display_tournaments(tournaments)

    def display_tournaments(self, tournaments: list[Tournament]) -> None:
        # Kept separate to allow reuse and isolate display logic from control flow
        """
        Prints a list of tournaments with their name, venue, date range, and status.

        Args:
            tournaments (list[Tournament]): List of tournaments to display.
        """
        print("\nAvailable Tournaments:\n")
        for i, t in enumerate(tournaments, 1):
            start = t.start_date.strftime("%d-%b-%Y")
            end = t.end_date.strftime("%d-%b-%Y")
            print(f"{i}. {t.name} — {t.venue} ({start} to {end}) {t.status_label}")
            if t.is_overdue:
                print(
                    "   [!] Warning: Tournament has passed its end date but is not marked complete."
                )

    def get_command(self):
        """
        Prompts the user to select an action and returns the appropriate command.

        Returns:
            BaseCommand: The next command to execute.
        """
        context = TournamentListCmd().execute()
        tournaments: list[Tournament] = context.kwargs.get("tournaments", [])

        print("\nPlease select your action from the options below:")
        print("# - Enter the number of a tournament to view/manage it")
        print("N - Create a new tournament")
        print("B - Back to App Menu")

        while True:
            choice = self.input_string("Choice").strip().upper()

            if choice == "B":
                return NoopCmd("app-main")

            if choice == "N":
                return NoopCmd("tournament-create")

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(tournaments):
                    selected = tournaments[index]
                    return NoopCmd("tournament-view", tournament=selected)

            print(
                "Invalid input. Please enter a valid number (e.g. 1, 2, 3...), N, or B."
            )
