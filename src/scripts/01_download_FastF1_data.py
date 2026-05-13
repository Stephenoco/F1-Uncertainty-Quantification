import os
import fastf1
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

fastf1.Cache.enable_cache('../data/cacheF1/') # session data can be quite large (50-100MB) so caching is recommended by FastF1

# Whatever year is needed to be downloaded
year = 2022
sessions_to_load = ['R']


def load_and_save_all_sessions(year, race_num):
    """Load all sessions for a race weekend."""

    for session_type in sessions_to_load:
        try:
            session = fastf1.get_session(year, race_num, session_type)
            session.load()

            # Creating path
            race_name = session.event['EventName'].replace(' ', '_')
            output_dir = f"../data/raw/{session.event['EventName']}/{year}"
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(
                output_dir,
                f"{race_num:02d}_{race_name}_{session_type}_laps.csv"
            )

            # Saving laps, what is contained in laps can be found here (https://theoehrly-fast-f1.mintlify.app/core-concepts/lap-timing#available-lap-data)
            session.laps.to_csv(output_path, index=False)

            print(f"Saved: {race_name} - {session_type}")

        except Exception as e:
            print(f"Failed {race_num} {session_type}: {e}")


# Then use it
with ThreadPoolExecutor(max_workers=3) as executor:
    list(executor.map(
        lambda race_num: load_and_save_all_sessions(year, race_num),
        range(1, 23)
    ))