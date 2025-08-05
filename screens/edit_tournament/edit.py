from commands import NoopCmd

from models import Tournament

from .view import EditTournamentView


def run(tournament: Tournament) -> NoopCmd:
    """
    Launches the tournament editing screen.

    Args:
        tournament (Tournament): The tournament to edit.

    Returns:
        NoopCommand: The next command based on user input.
    """
    return EditTournamentView(tournament).run()
