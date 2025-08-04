from commands.context import Context
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

            elif screen == "edit-tournament":
                command = EditTournamentView(self.context.tournament).run()
                self.context = command()

            elif screen == "exit":
                print("Goodbye!")
                break

            else:
                print(f"[!] Unknown screen: {screen}")
                break


if __name__ == "__main__":
    app = MainApp()
    app.run()
