import pandas as pd

# Load the CSV file
df = pd.read_csv('input.csv')

# Change column 1 to the values of column 10
df.iloc[:, 0] = df.iloc[:, 9]

# Save the modified DataFrame back to a CSV file
df.to_csv('nome_games.csv', index=False)
