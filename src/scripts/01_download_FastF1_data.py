import fastf1
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Use pathlib for cache directory
project_root = Path(__file__).resolve().parent.parent
cache_dir = project_root / 'data' / 'cacheF1'
cache_dir.mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache(str(cache_dir))  # Must convert to string for FastF1

# Whatever year to download
year = 2025
sessions_to_load = ['R']


def load_and_save_all_sessions(year, race_num):
    """Load all sessions for a race weekend."""

    for session_type in sessions_to_load:
        try:
            session = fastf1.get_session(year, race_num, session_type)
            session.load(weather=True)

            # Get race name
            race_name = session.event['EventName'].replace(' ', '_')

            # Build output directory with pathlib for compatibility with both Mac and Windows
            output_dir = project_root / 'data' / 'raw' / str(year) / race_name

            # Create directory
            output_dir.mkdir(parents=True, exist_ok=True)

            # Build output file paths
            output_path = output_dir / f"{race_num:02d}_{race_name}_{session_type}_laps.csv"
            output_path_weather = output_dir / f"{race_num:02d}_{race_name}_{session_type}_weather.csv"

            # Save laps and weather from each race
            session.laps.to_csv(output_path, index=False)
            session.weather_data.to_csv(output_path_weather, index=False)

            print(f"Saved: {race_name} - {session_type}")

        except Exception as e:
            print(f"Failed: {race_num} {session_type}: {e}")


# Download races
with ThreadPoolExecutor(max_workers=3) as executor:
    list(executor.map(
        lambda race_num: load_and_save_all_sessions(year, race_num),
        range(1, 25)  # 2025 will have 24 races
    ))