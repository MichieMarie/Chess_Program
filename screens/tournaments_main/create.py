from datetime import datetime

from commands import CreateTournamentCmd

from ..base_screen import BaseScreen


class CreateTournament(BaseScreen):
    """
    Screen for entering tournament details and triggering tournament creation.

    Prompts the user step-by-step to enter all required tournament details,
    including name, venue, start/end dates, and number of rounds.
    """

    display: str = "Follow the input prompts to create a new tournament."

    def get_command(self) -> CreateTournamentCmd:
        """
        Gather input from the user and return a tournament creation command.

        Returns:
            CreateTournamentCmd: A command object ready for execution.
        """
        attrs: list[tuple[str, str, callable]] = [
            ("name", "Tournament name", self.input_string),
            ("venue", "Venue", self.input_string),
            ("start_date", "Start date", self.input_tournament_dates),
            ("end_date", "End date", self.input_tournament_dates),
            ("rounds", "Enter number of rounds (default is 4):", self.input_rounds),
        ]

        data: dict[str, str | int | datetime | None] = {}
        for key, prompt, func in attrs:
            kwargs: dict[str, str] = {"prompt": prompt}
            if func == self.input_rounds:
                data[key] = func(prompt=prompt)  # only pass prompt
            else:
                data[key] = func(**kwargs)

        while data["end_date"] < data["start_date"]:
            print("‼️End date cannot be before start date.")
            data["end_date"] = self.input_tournament_dates(prompt="End date")

        return CreateTournamentCmd(
            name=data["name"],
            venue=data["venue"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            num_rounds=data["rounds"],
        )
