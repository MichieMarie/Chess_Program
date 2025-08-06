# Castle Chess Management System
A Python-based application for managing chess clubs, players, and tournaments. The program is divided into two main sections:
- Tournament Management – Create and edit tournaments, register players, update progress, and generate reports at any stage.
- Club Management – Create clubs, add players, and update player or club information.

## Features
Castle Chess includes tools to manage chess tournaments and player data, with full offline functionality and data persistence.
### Tournament Management
Create new tournaments with name, venue, dates, and number of rounds
- Register players from club rosters
- Randomized first-round matchups; ranked matchmaking in later rounds
- Enter match results and advance rounds
- View tournament progress and generate browser-based reports
- Resume or review past tournaments at any time
### Club Management System
- Create and manage multiple clubs
- Add, view, or update players
- Each player includes a name, email, chess ID, and birthdate
- Club rosters available during tournament registration

## Project Structure
The application uses a modular structure, with separate directories for models, screens, and command logic.
- **models/**

  Contains core data classes such as Tournament, Match, Round, and related utilities.
- **commands/**
  Handles business logic for actions like registering players or advancing rounds.
- **screens/**

  Controls the user interface and flow of each screen.

  Each screen is broken into:
    - view.py – manages screen display and user input
    - Action-specific files such as ``` create.py```, ``` edit.py```, and ``` register_player.py```  define the command classes that handle user actions from the screen interface.
- **chess.py**

  Main entry point for running the application.
- **data/**

  Contains directories for club and tournaments JSON files.
- **flake8_report/**

  Stores the auto-generated flake8 HTML linting report.

## Prerequisites
This project requires Python 3.9 or higher.

It was developed using [Python 3.13.5](https://www.python.org/downloads/).

## Installation
Use Microsoft CMD or Apple Terminal for any command prompts shown below.
1. Clone this repository to your local machine:
```git clone https://github.com/MichieMarie/Chess_Program``` 
2. Set up a virtual environment
   - Navigate to the project folder: ```cd Chess_Program```
   - Create a virtual environment: ```python -m venv .venv```
   - Activate the virtual environment: 
     - Windows: ```.venv\Scripts\activate```
     - MacOS/Linux: ```source .venv/bin/activate```
3. Install Python packages*:
```pip install -r requirements.txt```

  These packages are mainly for development (e.g., flake8 and flake8-html) and are not required to run the app itself.
4. If not ready to run the script and you still need CMD, deactivate the virtual environment: ```deactivate```

## flake8 Setup and Report
This project uses [`flake8`](https://flake8.pycqa.org/en/latest/) and [`flake8-html`](https://pypi.org/project/flake8-html/) to ensure code quality and compliance with PEP 8.
### Setup
If you already installed the requirements in the Installation step, you're good to go.  
Otherwise, install `flake8` and `flake8-html` manually:

```pip install flake8 flake8-html```

### Generating the Report
To create an HTML report of code quality:
1. From the root of the project (e.g., `Chess_Program`), run:

```flake8 . --format=html --htmldir=flake8_report --max-line-length=119```

2. Open the generated report:
   - Navigate to the `flake8_report/` folder
   - Open `index.html` in your web browser to view the results

## Using the Program

When you launch the program, you'll be prompted to choose between **Tournament Management** and **Club Management**.

### Tournament Management
- If a single active tournament exists, the program will automatically take you to its management screen.
- From the tournaments menu, you can:
  - View active or past tournaments
  - Create a new tournament (name, venue, start/end dates in `DD-MM-YYYY` format, number of rounds)
- Once a tournament is created:
  - Register players from club rosters using search by name or chess ID
  - A tournament must have an **even number** of players before it can be started
  - Start the tournament to generate randomized first-round pairings
- During the tournament:
  - Enter results for each match (Player 1 win, Player 2 win, or Draw)
  - Advance rounds after confirming all results have been entered
- At any point, generate a tournament report, which opens in your web browser (no internet needed)

### Club Management
- View, create, or edit chess clubs
- Add players with the following required fields:
  - Name
  - Email
  - Chess ID (format: `AA#####`)
  - Birthdate
- Only players who are part of a club can be registered in a tournament

### Saving Progress
All changes are saved automatically in JSON files located in the `data/` folder. You can close and reopen the program without losing progress.

## How to Run

Follow these steps to launch the application:

1. Open a terminal (macOS/Linux) or command prompt (Windows).
2. Navigate to the project folder:
   ```cd path/to/Chess_Program```
3. Activate the virtual environment:
   - **Windows:**
     ```.venv\Scripts\activate```
   - **macOS/Linux:**
     ```source .venv/bin/activate```
4. Run the application:
   ```python chess.py```
5. Follow on-screen prompts to manage clubs, players, and tournaments.
6. To exit the program, type `X` when prompted on any screen that allows it.




