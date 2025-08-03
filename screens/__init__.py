from .clubs import ClubCreate, ClubView
from .edit_tournament import EditTournamentView
from .main_menu import MainMenu
from .players import PlayerEdit, PlayerView
from .register_player import PlayerRegistrationView
from .tournaments_main import TournamentsMainView, CreateTournament


__all__ = [
    "ClubCreate",
    "ClubView",
    "CreateTournament",
    "EditTournamentView",
    "MainMenu",
    "PlayerRegistrationView",
    "PlayerView",
    "TournamentsMainView",
]
