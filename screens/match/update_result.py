from commands import MatchResultsCmd, Context
from models import Tournament


def run(tournament: Tournament, match_index: int) -> Context:
    """
    Prompts the user to enter the result of a match in the current round.

    Args:
        tournament (Tournament): The active tournament instance.
        match_index (int): Index of the match to update.

    Returns:
        Context: Updated tournament context after result is applied.

    User Options:
        1 - Player 1 wins
        2 - Player 2 wins
        d - Draw
    """
    current_index = tournament.current_round_index

    if current_index < 0 or current_index >= len(tournament.rounds):
        print("‼️ No active round to update.")
        return Context("tournament-view", tournament=tournament)

    matches = tournament.rounds[current_index].matches

    if not (0 <= match_index < len(matches)):
        print("‼️ Invalid match number.")
        return Context("tournament-view", tournament=tournament)

    match = matches[match_index]
    p1 = match._get_name(match.player1)
    p2 = match._get_name(match.player2)

    while True:
        result = (
            input(f"Result for {p1} (p1) vs {p2} (p2). Select winner/draw: 1/2/draw")
            .strip()
            .lower()
        )
        if result in {"1", "2", "d"}:
            return MatchResultsCmd(tournament, {match_index: result}).execute()
        else:
            print("‼️ Invalid input. Please enter 1, 2, or d.")
