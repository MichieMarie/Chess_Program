from commands import Context, StartTournamentCmd
from models import Tournament


def run(tournament: Tournament) -> Context:
    """
    Runs the StartTournament command and returns the resulting context.

    Args:
        tournament (Tournament): The tournament to start.

    Returns:
        Context: Redirect to tournament-view with updated state.
    """
    return StartTournamentCmd(tournament).execute()
