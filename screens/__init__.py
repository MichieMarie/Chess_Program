from .clubs import ClubCreate, ClubView
from .main_menu import MainMenu
from .players import PlayerEdit, PlayerView
from .register_player import PlayerRegistration, PlayerRegistrationView
from .tournaments_main import TournamentsMainView, CreateTournament

__all__ = [
    "ClubCreate",
    "ClubView",
    "CreateTournament",
    "MainMenu",
    "PlayerRegistration",
    "PlayerRegistrationView",
    "PlayerView",
    "TournamentsMainView",
]
