# Teamfight-Tactics stats

![Python 3.13.5](https://img.shields.io/badge/python-3.7.4-blue.svg)

"This is a full-stack project designed to display user statistics for matches played in Teamfight Tactics (TFT).<br />
<br />
Data is extracted using a Python script that interacts with the official Riot Games API, and is then ingested into a SQL Server database.
The data pipeline is fully automated, with an option for manual refresh if needed.
The graphical user interface (GUI) is built using the Streamlit package."

## API key
You also need to have an API key from Riot. You can get it by creating an account here: <https://developer.riotgames.com/>.
To use the Riot api you must also agree to their terms of use found at https://developer.riotgames.com/terms

## Design

**Backend**: `Python` wrapper for the Riot API <br />
**Frontend**: Using the Streamlit package for `Python` <br />
**Data**: _Provided using the Riot API_

### Future (optional) features
**Backend**: Data ingestion with an SQL Server connector in python

## Disclaimer
This is an unofficial, community-built Python wrapper around the Riot Games API. This project is **not endorsed, sponsored, certified, or otherwise affiliated** with Riot Games, Inc.
Riot Games, along with game titles such as *League of Legends*, *Valorant*, and all associated logos and trademarks, remain the exclusive property of Riot Games, Inc. This wrapper follows Riot’s fan‑project policy and API Terms & Policies, and is intended for **non‑commercial community use**.
<br />
This project isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
