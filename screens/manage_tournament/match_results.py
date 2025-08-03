from commands import Context, MatchResultsCmd
from models import Tournament


def run(tournament: Tournament) -> Context:
    """
    Prompts the user to enter match results for the current round and applies them.

    Args:
        tournament (Tournament): The tournament with the current round.

    Returns:
        Context: Updated context returning to the tournament view.
    """
    current_index = tournament.current_round_index

    if current_index < 0 or current_index >= len(tournament.rounds):
        print("\n[!] No active round to enter results for.")
        return Context("tournament-view", tournament=tournament)

    current_round = tournament.rounds[current_index]
    results = []

    print(f"\nEnter results for Round {current_index + 1} matches:\n")
    for i, match in enumerate(current_round.matches, 1):
        p1 = match._get_name(match.player1)
        p2 = match._get_name(match.player2)

        while True:
            result = input(f"{i}. {p1} vs {p2} — Winner (1/2/d): ").strip().lower()
            if result in {"1", "2", "d"}:
                results.append(result)
                break
            else:
                print("Invalid input. Please enter 1, 2, or d.")

    return MatchResultsCmd(tournament, results).execute()
