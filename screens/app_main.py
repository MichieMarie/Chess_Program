from commands import ExitCmd, NoopCmd

from .base_screen import BaseScreen


class AppMainMenu(BaseScreen):
    """
    Main menu screen for the full application.

    Presents users with top-level options:
    - Manage tournaments
    - Manage clubs and players
    - Exit the application
    """

    def __init__(self) -> None:
        """Initialize the main menu screen."""
        pass

    def display(self) -> str:
        """
        Display a welcome message when this screen is launched.

        Returns:
            str: Welcome message to display.
        """
        return "\n ♟️ Welcome to the Chess Tournament Manager ♟️\n"

    def get_command(self) -> ExitCmd | NoopCmd:
        """
        Prompt the user for a top-level action.

        Returns:
            ExitCmd | NoopCmd: A command directing navigation to the
            tournament manager, club manager, or exiting the app.
        """
        while True:
            print("What would you like to do?")
            print("Type T to access tournament management system.")
            print("Type C to access club and player management system.")
            print("Type X to exit.")
            value: str = self.input_string().strip().upper()

            if value.upper() == "T":
                return NoopCmd("manage-tournaments")
            elif value.upper() == "C":
                return NoopCmd("manage-clubs")
            elif value.upper() == "X":
                return ExitCmd()
            else:
                print("Invalid input. Please enter T, C, or X.")
