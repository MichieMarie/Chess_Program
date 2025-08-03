from .view import EditTournamentView


def run(tournament):
    return EditTournamentView(tournament).run()
