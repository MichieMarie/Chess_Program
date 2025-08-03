from commands import NoopCmd
from models import Tournament
from models.match import PLAYER1, PLAYER2, DRAW

from ..base_screen import BaseScreen


class TournamentView(BaseScreen):
    """
    Screen for viewing and managing a tournament.
    Adjusts output and commands based on tournament status.
    """

    def __init__(self, tournament: Tournament):
        self.tournament = tournament

    def display_header(self) -> None:
        """Prints basic tournament information."""
        print(f"\n{self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(
            f"Dates: {self.tournament.start_date.strftime('%d-%b-%Y')} to {self.tournament.end_date.strftime('%d-%b-%Y')}"
        )

    def display_players(self) -> None:
        """Prints registered players with club and tournament points, sorted by score."""
        print("\n👥 Registered Players:\n")

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
            print(f"{i}. {name} ({cid})")
            print(f"   Club: {club}")
            print(f"   Points: {pts}\n")

    def display_current_matches(self) -> None:
        """Displays match pairings and results for the current round."""
        current_index = self.tournament.current_round_index

        if current_index < 0 or current_index >= len(self.tournament.rounds):
            print("\n[!] No current round to display.")
            return

        rnd = self.tournament.rounds[current_index]
        print(f"\n🕹️ Matches for Round {current_index + 1}:\n")

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
        """Displays tournament info, players, rounds, and matches based on state."""
        self.display_header()
        self.display_players()

        if self.tournament.is_complete or self.tournament.current_round_index == -1:
            print(f"\nTotal rounds: {self.tournament.num_rounds}")
        else:
            round_num = self.tournament.current_round_index + 1
            print(f"\nRound {round_num} of {self.tournament.num_rounds}")
            self.display_current_matches()

    def get_command(self):
        """Prompts for the next action based on tournament status."""
        print()  # Spacing after match/player display
        print("\nPlease select your action from the options below:")

        if self.tournament.is_complete:
            print("R - Generate a Tournament Report")
            print("T - Return to Tournament Menu")
            print("B - Return to App Menu")

        elif self.tournament.current_round_index == -1:
            print("P - Register a Player")
            print("E - Edit the tournament")
            print("S - Start the Tournament")
            print("R - Generate a Tournament Report")
            print("T - Return to Tournament Menu")
            print("B - Return to App Menu")

        else:
            print("# - Update a Match")
            print("A - Advance to the Next Round")
            print("R - Generate a Tournament Report")
            print("T - Return to Tournament Menu")
            print("B - Return to App Menu")

        choice = self.input_string("Choice").strip().upper()

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
        if choice == "#" and not self.tournament.is_complete:
            return NoopCmd("match-results", tournament=self.tournament)
        if choice == "T":
            return NoopCmd("tournaments-main")
        if choice == "B":
            return NoopCmd("app-main")

        print("Invalid input. Please choose a valid option.")
        return NoopCmd("tournament-view", tournament=self.tournament)
