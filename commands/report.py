import webbrowser
from pathlib import Path

from models import Tournament

from .base import BaseCommand
from .context import Context


class TournamentReportCmd(BaseCommand):
    """
    Command to generate a tournament report in HTML format and open it in the browser.

    The report includes player standings and round-by-round match results.
    Users can print or save the report as a PDF using their browser.
    """

    def __init__(self, tournament: Tournament):
        self.tournament = tournament

    def build_players_info(self) -> str:
        """
        Builds a 2-column HTML table displaying player info and scores.

        Returns:
            str: The HTML string representing the players table.
        """
        rows = []
        players = sorted(
            self.tournament.players,
            key=lambda p: scores.get(p["chess_id"], 0.0),
            reverse=True,
        )
        scores = self.tournament.player_scores()

        for i in range(0, len(players), 2):
            row_cells = []
            for j in range(2):
                if i + j < len(players):
                    p = players[i + j]
                    cell = f"""
                        <td>
                            <strong>{p['name']}</strong><br>
                            From {p['club_name']}<br>
                            Tournament points: {scores.get(p['chess_id'], 0.0)}
                        </td>
                    """
                else:
                    cell = "<td></td>"
                row_cells.append(cell)
            rows.append("<tr>" + "".join(row_cells) + "</tr>")

        return f'<table class="player-table">{"".join(rows)}</table>'

    def build_rounds_info(self) -> str:
        """
        Creates headers for each round including "Final Round Match Results" for the last round.
        Builds a 3-column HTML table displaying match outcomes.

        Returns:
            str: The HTML string representing the match results.
        """
        rounds_html = []
        total_rounds = len(self.tournament.rounds)

        for idx, rnd in enumerate(self.tournament.rounds):
            if idx == total_rounds - 1:
                header = "<h2>Final Round Match Results</h2>"
            else:
                header = f"<h2>Round {idx + 1} of {total_rounds} Match Results</h2>"

            match_cells = []
            for match in rnd.matches:
                p1 = match.player1.name
                p2 = match.player2.name
                if match.winner == "draw":
                    content = f"{p1}<br>{p2}<br><em>Result: Draw</em>"
                elif match.winner == "player1":
                    content = f"{p1} - W<br>{p2}"
                elif match.winner == "player2":
                    content = f"{p1}<br>{p2} - W"
                else:
                    content = f"{p1}<br>{p2}"
                match_cells.append(f"<td>{content}</td>")

            # group matches into rows of 3
            rows = [
                "<tr>" + "".join(match_cells[i : i + 3]) + "</tr>"
                for i in range(0, len(match_cells), 3)
            ]
            round_table = f'<table class="round-table">{"".join(rows)}</table>'
            rounds_html.append(header + round_table)

        return "".join(rounds_html)

    def build_html_report(self) -> str:
        """
        Builds the full HTML report as a string with embedded styles and tournament data.

        Returns:
            str: The complete HTML string of the report.
        """
        rounds_html = self.build_rounds_info()
        player_html = self.build_players_info()

        return f"""
        <html>
        <head>
        <style>
            body {{
                font-family: "Times New Roman", serif;
                font-size: 12pt;
            }}
            h1 {{
                font-size: 20pt;
                text-align: center;
            }}
            h2 {{
                font-size: 16pt;
                text-align: center;
            }}
            h4 {{
                font-size: 14pt;
                text-align: center;
            }}
            .player-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 40px;
            }}
            .player-table td {{
                vertical-align: top;
                text-align: center;
                padding: 10px;
            }}
            .round-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 40px;
            }}
            .round-table td {{
                width: 33%;
                vertical-align: top;
                padding: 15px;
                border: none;
            }}
            .print-instruction {{
                text-align: center;
                font-style: italic;
                margin-top: 20px;
            }}
        </style>
        </head>
        <body>
            <h1>♛♞♝ <strong>{self.tournament.name}</strong> ♝♞♛</h1>
            <h2>at {self.tournament.venue}</h2>
            <h4>{self.tournament.start_date.strftime('%B %d, %Y')} to {self.tournament.end_date.strftime('%B %d, %Y')}</h4>
            <div class="print-instruction">To save or print this report, press Ctrl+P (or Cmd+P on Mac).</div>
            <h2>Players</h2>
            {player_html}
            {rounds_html}
        </body>
        </html>
        """

    def execute(self) -> Context:
        """
        Generates the HTML report and opens it in the user's default web browser.

        Returns:
            Context: Returns to the tournament view screen.
        """
        html = self.build_html_report()
        reports_dir = Path("data/reports")
        reports_dir.mkdir(exist_ok=True)
        filepath = reports_dir / f"{self.tournament.name.replace(' ', '_')}_report.html"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open(filepath.as_uri())
        print("The tournament report has been opened in your browser.")
        print("Press Ctrl+P (or Cmd+P) to print or save it as a PDF.")
        return Context("tournament-view", tournament=self.tournament)
