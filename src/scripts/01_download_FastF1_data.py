import fastf1
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd

# Use pathlib for cache directory
project_root = Path(__file__).resolve().parent.parent
cache_dir = project_root / 'data' / 'cacheF1'
cache_dir.mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache(str(cache_dir))  # Must convert to string for FastF1

# Whatever year to download
year = 2022
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

            # Download telemetry data
            print(f"Saved: {race_name} - {session_type}")

        except Exception as e:
            print(f"Failed: {race_num} {session_type}: {e}")

def download_telemetry(year, race_num):
    for session_type in sessions_to_load:
        session = fastf1.get_session(year, race_num, session_type)
        session.load(laps=True, weather=False, telemetry=True)

        race_name = session.event['EventName'].replace(' ', '_')
        print(f"Loading {race_name}...")

        raw_dir = project_root / 'data' / 'raw' / str(year)

        rows = []
        total = len(session.laps)

        for i, (_, lap) in enumerate(session.laps.iterlaps()):
            if (i + 1) % 50 == 0:
                print(f"Processing lap {i+1}/{total}")
            try:
                tel = lap.get_telemetry()
                rows.append({
                    'Driver': lap['Driver'],
                    'LapNumber': lap['LapNumber'],
                    'AvgGapAhead': tel['DistanceToDriverAhead'].mean(),
                    'MinGapAhead': tel['DistanceToDriverAhead'].min(),
                    'AvgThrottle': tel['Throttle'].mean(),
                    'AvgBrake': tel['Brake'].mean(),
                    'AvgSpeed': tel['Speed'].mean(),
                })
            except Exception:
                continue

        df = pd.DataFrame(rows)

        # Match folder naming convention e.g. Australian_Grand_Prix
        output_path = raw_dir / race_name / f'{race_num:02d}_{race_name}_telemetry.csv'

        if not output_path.parent.exists():
            print(f"Folder not found for {race_name}, skipping save")
            return

        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} laps: {output_path.name}")

# Download race laps, weather and telemetry data
with ThreadPoolExecutor(max_workers=3) as executor:
    list(executor.map(
        lambda race_num: (load_and_save_all_sessions(year, race_num)),
        range(1, 24),
    ))

for race in range(1,24): # Set range to number of races
    try:
        download_telemetry(year, race)
    except Exception as e:
        print(f"Failed: {race} - {e}")
