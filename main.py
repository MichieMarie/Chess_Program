from commands.context import Context
from models.tournament_manager import TournamentManager
from models.club_manager import ClubManager
from screens import (
    EditTournamentView,
    TournamentView,
    PlayerRegistrationView,
    TournamentsMainView,
    AppMainMenu,
    MainMenu,
    ClubCreate,
    ClubView,
    PlayerView,
    PlayerEdit,
)
from screens.tournaments_main import CreateTournament
from screens.manage_tournament import (
    start_tournament,
    advance_round,
    tournament_report,
)
from screens.register_player import run as register_player_confirm


class MainApp:
    """The main controller for the chess program."""

    def __init__(self):
        self.context = Context("app-main")

    def run(self):
        while True:
            screen = self.context.screen

            if screen == "app-main":
                command = AppMainMenu().run()
                self.context = command()

            elif screen == "tournaments-main":

                source = getattr(self.context, "source", None)

                manager = TournamentManager()

                active_tournaments = [
                    t for t in manager.tournaments if t.status_label == "[Active]"
                ]

                if source == "main-menu" and len(active_tournaments) == 1:

                    # Only redirect from app main menu

                    self.context = Context(
                        "tournament-view", tournament=active_tournaments[0]
                    )

                else:

                    command = TournamentsMainView().run()

                    self.context = command()

            elif screen == "tournament-create":
                cmd = CreateTournament().get_command()
                self.context = cmd.execute()
                print(
                    self.context.screen,
                    getattr(self.context, "tournament", None),
                )

            elif screen == "tournament-view":
                tournament = getattr(self.context, "tournament", None)
                if tournament:
                    command = TournamentView(tournament).run()
                    self.context = command()

                else:
                    print("[ERROR] No tournament found in context.")
                    self.context = Context("tournaments-main")

            elif screen == "start-tournament":
                self.context = start_tournament(self.context.tournament)

            elif screen == "advance-round":
                self.context = advance_round(self.context.tournament)

            elif screen == "tournament-report":
                self.context = tournament_report(self.context.tournament)

            elif screen == "register-player":
                command = PlayerRegistrationView(self.context.tournament).run()
                self.context = command()

            elif screen == "register-player-confirm":

                command = register_player_confirm(
                    self.context.tournament, self.context.player
                )

                self.context = command()

            elif screen == "main-menu":
                manager = ClubManager()
                command = MainMenu(clubs=manager.clubs).run()
                self.context = command()

            elif screen == "club-create":
                command = ClubCreate().run()
                self.context = command()

            elif screen == "club-view":
                command = ClubView(**self.context.kwargs).run()
                self.context = command()

            elif screen == "player-view":
                command = PlayerView(**self.context.kwargs).run()
                self.context = command()

            elif screen in ("player-edit", "player-create"):
                command = PlayerEdit(**self.context.kwargs).run()
                self.context = command()
            elif screen == "edit-tournament":
                command = EditTournamentView(self.context.tournament).run()
                self.context = command()

            else:

                if self.context.screen is not None:

                    print(f"[!] Unknown screen: {screen}")

                break


if __name__ == "__main__":
    app = MainApp()
    app.run()
