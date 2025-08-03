from commands import Context, TournamentReportCmd
from models import Tournament


def run(tournament: Tournament) -> Context:
    """
    Runs the TournamentReportCmd to generate and display a tournament report.

    Args:
        tournament (Tournament): The tournament to report on.

    Returns:
        Context: Returns to the tournament view.
    """
    return TournamentReportCmd(tournament).execute()
