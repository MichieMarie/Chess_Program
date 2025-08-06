from commands import NoopCmd
from models import Tournament
from models.match import PLAYER1, PLAYER2, DRAW
from screens.match.update_result import run as update_match_result_screen

from ..base_screen import BaseScreen


class TournamentView(BaseScreen):
    """
    Screen for viewing and managing a tournament.

    Displays header, players, current matches, and contextual options.
    Command behavior adjusts based on tournament status (not started, in progress, or complete).
    """

    def __init__(self, tournament: Tournament):
        """
        Initialize the tournament view with the given tournament.

        Args:
            tournament (Tournament): The tournament to manage.
        """
        self.tournament = tournament

    def display_header(self) -> None:
        """Prints basic tournament information."""
        print(f"\n{self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(
            f"Dates: {self.tournament.start_date.strftime('%d-%b-%Y')} "
            f"to {self.tournament.end_date.strftime('%d-%b-%Y')}"
        )

    def display_players(self) -> None:
        """Prints registered players with club and tournament points, sorted by score."""
        print("\n👑 Registered Players 👑\n")

        scores = self.tournament.player_scores()
        players = sorted(
            self.tournament.players,
            key=lambda player: scores.get(player["chess_id"], 0.0),
            reverse=True,
        )

        for i, p in enumerate(players, 1):
            name = p["name"]
            cid = p["chess_id"]
            club = p["club_name"]
            pts = scores.get(cid, 0.0)
            print(f"{i}. {name} ({cid}) from {club} | Tournament Points: {pts}")

    def display_current_matches(self) -> None:
        """Displays match pairings and results for the current round."""
        current_index = self.tournament.current_round_index

        if current_index < 0 or current_index >= len(self.tournament.rounds):
            print("\n‼️ No current round to display.")
            return

        rnd = self.tournament.rounds[current_index]
        print(f"\n♟️️ Matches for Round {current_index + 1} ♟️\n")

        for i, match in enumerate(rnd.matches, 1):
            p1 = match._get_name(match.player1)
            p2 = match._get_name(match.player2)

            if match.winner == DRAW:
                print(f"{i}. {p1} vs {p2}")
                print("   Result: Draw\n")
            elif match.winner == PLAYER1:
                print(f"{i}. {p1} (W) vs {p2}\n")
            elif match.winner == PLAYER2:
                print(f"{i}. {p1} vs {p2} (W)\n")
            else:
                print(f"{i}. {p1} vs {p2}")
                print("   Result: [Not yet played]\n")

    def display(self) -> None:
        """
        Displays tournament overview including header, player standings, and match results.

        Content and format adjust based on tournament status.
        """
        self.display_header()
        self.display_players()

        if self.tournament.is_complete or self.tournament.current_round_index == -1:
            print(f"\nTotal rounds: {self.tournament.num_rounds}")
        else:
            round_num = self.tournament.current_round_index + 1
            print(f"\nRound {round_num} of {self.tournament.num_rounds}")
            self.display_current_matches()

    def get_command(self) -> NoopCmd:
        """
        Prompts the user to select an action based on tournament status.

        Options vary depending on whether the tournament has not started, is in progress,
        or has been completed. May include registering players, editing details,
        advancing rounds, updating match results, or generating a report.

        Returns:
            NoopCmd: The next command to execute.
        """
        print()
        print("\nPlease select your action from the options below:")

        if self.tournament.is_complete:
            print("R - Generate a tournament report")
            print("T - Return to the tournaments main menu")
            print("B - Return to program main menu")

        elif self.tournament.current_round_index == -1:
            print("P - Register a player")
            print("E - Edit the tournament")
            print("S - Start the tournament")
            print("R - Generate a tournament report")
            print("T - Return to the tournaments main menu")
            print("B - Return to program main menu")

        else:
            print("# - Enter the number of a match to enter or update result")
            print(f"A - Advance {self.tournament.name} to the next round")
            print("R - Generate a tournament report")
            print("T - Return to the tournaments main menu")
            print("B - Return to the program main menu")

        choice = self.input_string("Choice").strip().upper()

        if choice.isdigit():
            match_index = int(choice) - 1
            update_match_result_screen(self.tournament, match_index)
            return NoopCmd("tournament-view", tournament=self.tournament)

        if choice == "E" and self.tournament.current_round_index == -1:
            return NoopCmd("edit-tournament", tournament=self.tournament)
        if choice == "P" and self.tournament.current_round_index == -1:
            return NoopCmd("register-player", tournament=self.tournament)
        if choice == "S" and self.tournament.current_round_index == -1:
            return NoopCmd("start-tournament", tournament=self.tournament)
        if choice == "R":
            return NoopCmd("tournament-report", tournament=self.tournament)
        if choice == "A" and not self.tournament.is_complete:
            return NoopCmd("advance-round", tournament=self.tournament)
        if choice == "T":
            return NoopCmd("tournaments-main")
        if choice == "B":
            return NoopCmd("app-main")

        print("‼️ Invalid input. Please choose a valid option.")
        return NoopCmd("tournament-view", tournament=self.tournament)
