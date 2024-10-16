import pandas as pd
import datetime

def release_unix_to_common_csv(read_file_path, initial_limit=0, end_limit=0, write_file_path=''):
    # Load data from the CSV file into a DataFrame
    all_games_data = pd.read_csv(read_file_path)

    # Determine the range of games to process based on the limits
    if end_limit > 0:
        all_games_data = all_games_data.iloc[initial_limit:end_limit]
    else:
        all_games_data = all_games_data.iloc[initial_limit:]  # Process all games from the initial limit onward

    # Convert the Unix timestamp to 'YYYY-MM-DD' format for 'first_release_date', if needed
    if 'first_release_date' in all_games_data.columns:
        def convert_unix_to_date(value):
            try:
                # Check if the value is numeric (likely a Unix timestamp)
                return pd.to_datetime(value, unit='s').strftime('%Y-%m-%d') if pd.to_numeric(value, errors='coerce') else value
            except (ValueError, TypeError):
                # Return the original value if conversion fails (likely already in 'YYYY-MM-DD' format)
                return value

        all_games_data['first_release_date'] = all_games_data['first_release_date'].apply(convert_unix_to_date)

    # If write_file_path is provided, write the updated data back to a CSV file
    if write_file_path:
        all_games_data.to_csv(write_file_path, index=False)

# Example usage:
release_unix_to_common_csv('games.csv', initial_limit=0, end_limit=1001, write_file_path='updated_games.csv')
