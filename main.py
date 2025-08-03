from commands import Context
from screens import (
    EditTournamentView,
    TournamentView,
    PlayerRegistrationView,
    TournamentsMainView,
    AppMainMenu,
)
from screens.tournaments_main import CreateTournament
from screens.manage_tournament import (
    start_tournament,
    advance_round,
    match_results,
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

            # Screens with UI logic
            if screen == "app-main":
                self.context = AppMainMenu().run()

            elif screen == "tournaments-main":
                self.context = TournamentsMainView().run()

            elif screen == "tournament-create":
                cmd = CreateTournament().get_command()
                self.context = cmd.execute()

            elif screen == "tournament-view":
                self.context = TournamentView(self.context.tournament).run()

            elif screen == "start-tournament":
                self.context = start_tournament(self.context.tournament)

            elif screen == "advance-round":
                self.context = advance_round(self.context.tournament)

            elif screen == "match-results":
                self.context = match_results(self.context.tournament)

            elif screen == "tournament-report":
                self.context = tournament_report(self.context.tournament)

            elif screen == "register-player":
                self.context = PlayerRegistrationView(self.context.tournament).run()

            elif screen == "register-player-confirm":
                self.context = register_player_confirm(
                    self.context.tournament, self.context.player
                )

            elif screen == "edit-tournament":
                self.context = EditTournamentView(self.context.tournament).run()

            elif screen == "exit":
                print("Goodbye!")
                break

            else:
                print(f"[!] Unknown screen: {screen}")
                break


if __name__ == "__main__":
    app = MainApp()
    app.run()
