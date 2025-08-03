from commands import AdvanceRoundCmd, Context
from models import Tournament


def confirm_round_advance() -> bool:
    """
    Prompt the user to confirm advancing to the next round.

    Returns:
        bool: True if user confirms; False otherwise.
    """
    answer: str = input("Advance to next round? (y/n): ").strip().lower()
    return answer == "y"


def run(tournament: Tournament) -> Context:
    """
    Confirms and advances the tournament to the next round if possible.

    Args:
        tournament (Tournament): The tournament instance.

    Returns:
        Context: Resulting context from AdvanceRoundCmd, or back to view if canceled.
    """
    if confirm_round_advance():
        return AdvanceRoundCmd(tournament).execute()
    else:
        print("Round advancement canceled.")
        return Context("tournament-view", tournament=tournament)
