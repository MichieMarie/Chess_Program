import re
from abc import ABC, abstractmethod
from datetime import datetime


class BaseScreen(ABC):
    """Abstract class for screen interaction"""

    @abstractmethod
    def get_command(self):
        """Child classes must implement this method. It must return a Command."""
        pass

    def input_string(self, prompt="", default=None, empty=False):
        """
        Utility function: get a string from the screen.
        If default is provided and the user provides an empty response, then the default value is used.
        If empty is True, a user cannot provide an empty response.
        """

        prompt = prompt + "? "

        if default:
            prompt += f"[{default}] "

        while True:
            value = input(prompt)

            if not value and default:
                value = default

            if not empty:
                return value
            if empty and value:
                return value

    def input_email(self, **kwargs):
        """Utility function to get an email address"""

        # https://stackoverflow.com/a/201378
        mail_rgxp = (
            r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+"
            r"(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
            r'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]'
            r'|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@'
            r"(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
            r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\["
            r"(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}"
            r"(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|"
            r"[a-z0-9-]*[a-z0-9]:"
            r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]"
            r"|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]"
        )
        message = "Please provide a valid email address!"
        return self.input_regexp(mail_rgxp, message, **kwargs)

    def input_regexp(self, regexp, error_message, **kwargs):
        """Utility function to get a string matching a regular expression"""
        while True:
            value = self.input_string(**kwargs)
            if re.match(regexp, value):
                return value

            print(error_message)

    def input_chess_id(self, **kwargs):
        """Utility function to get a Chess ID string"""
        chess_rgxp = r"[A-Z]{2}[0-9]{5}"
        message = "Please provide a valid Chess ID (XXNNNNN)!"
        return self.input_regexp(chess_rgxp, message, **kwargs)

    def input_birthday(self, **kwargs):
        """Utility function to get a date string"""
        while True:
            value = self.input_string(**kwargs)
            try:
                dt = datetime.strptime(value, "%d-%m-%Y")
                if dt > datetime.now():
                    raise ValueError
                return value
            except ValueError:
                print("Please provide a valid date (dd-mm-yyyy)!")

    def input_tournament_dates(self, **kwargs) -> datetime:
        """
        Prompts the user for a valid date in dd-mm-yyyy format.

        Returns:
            datetime: A valid parsed datetime (00:00 time).
        """
        while True:
            value: str = self.input_string(**kwargs)
            try:
                return datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                print("❗Please enter a valid date in the format dd-mm-yyyy.")

    def input_rounds(
        self, prompt="Enter number of rounds (default is 4):", default="4"
    ) -> int:
        """
        Prompts the user for a valid whole number > 0 to represent number of rounds.

        Returns:
            int: The validated number of rounds.
        """
        while True:
            value = self.input_string(prompt=prompt, default=default).strip()

            if value == "" or value == "0":
                return int(default)

            try:
                num = int(value)
                if num > 0:
                    return num
                else:
                    print("#️⃣ Please enter a number greater than 0.")
            except ValueError:
                print(
                    "#️⃣#️⃣ Please enter a valid whole number (e.g., 3). No letters or decimals."
                )

    def run(self):
        """Main method to 'run' the screen - displays a message and gets a command"""
        message = getattr(self, "display", None)

        if message and callable(message):
            message = message()

        if message:
            print(str(message))

        print("")
        return self.get_command()
