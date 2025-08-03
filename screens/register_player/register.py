from commands import Context
from models import Tournament


def run(tournament: Tournament, player: dict) -> Context:
    """
    Registers a player to a tournament, if not already registered.

    Args:
        tournament (Tournament): The tournament instance.
        player (dict): The selected player dictionary with name, chess_id, and club_name.

    Returns:
        Context: Redirect to the tournament view screen.
    """
    # Check if player is already registered
    if any(p["chess_id"] == player["chess_id"] for p in tournament.players):
        print(f"{player['name']} is already registered.")
    else:
        tournament.players.append(player)
        tournament.save()
        print(f"{player['name']} has been registered for {tournament.name}.")

    return Context("tournament-view", tournament=tournament)
