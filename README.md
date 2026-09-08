# General_projects

A collection of small, standalone Python projects covering data tools, simple apps, and games — built for practice and experimentation. The repo includes a `.devcontainer` setup for a consistent, ready-to-code environment.

Each project lives in its own subfolder with its own script(s) and (where relevant) its own README.

## Projects

| Project | Description | Stack |
|---|---|---|
| `Csv_analyser/` | A tool for loading and analyzing CSV files — summarizing, and exploring tabular data. | Python, pandas, streamlit and matplotlib |
| `Stock_price_viewer/` | An app/script for fetching and viewing stock price data. | Python, requests, yfinance, matplotlib, plotly and pandas |
| `python_terminal_game/` | A terminal-based game built in Python. | Python and numpy |
| `Weather_dashboard/` | A dashboard for viewing current or historical weather data. | Python, requests, streamlit and pandas |

## Dev Environment
This repo includes a [`.devcontainer`](./.devcontainer) configuration, so it can be opened directly in a container with all dependencies pre-installed — works with VS Code's Dev Containers extension or GitHub Codespaces.

```bash
git clone https://github.com/Pranav10261/General_projects.git
cd General_projects
# Open in VS Code and select "Reopen in Container"
# or launch a GitHub Codespace directly from the repo
```

## Repo Structure
```
General_projects/
├── .devcontainer/
│   └── devcontainer.json
├── csv_analyser/
|   ├── csv_analyser.py
|   ├── sample_data.csv
|   ├── requirements.txt
|   └── README.md
├── stock_price_viewer/
|   ├── stock_price.py
|   └── README.md
├── python_terminal_game/
│   ├── game.py
|   ├──save_data.json
|   └── README.md
├── weather_dashboard/
│   ├── Weather_dash.py
|   ├── requirements.txt
|   └── README.md
└── README.md          # you are here
```

## How to Use
Each project is self-contained — `cd` into the folder you want and run its script directly.

```bash
cd <project-folder>
pip install -r requirements.txt   # if present
python <main-script>.py
```

## Purpose
These projects are for practicing:
- Working with real-world APIs and data (stocks, weather, CSVs)
- Building small interactive Python programs
- Setting up reproducible dev environments with `.devcontainer`

## Author
Pranav K — [Pranav10261](https://github.com/Pranav10261)
