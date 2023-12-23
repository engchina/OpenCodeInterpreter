import pandas as pd

# Load the uploaded CSV file into a Pandas DataFrame
df = pd.read_csv('D:\\Users\\thinkpad\\AppData\\Local\\Temp\\gradio\\20e273176b0e98123efb36c3de6efd68c0a9c4d6\\analytic_ai.csv')

# Print the 15-25 rows of the DataFrame, including the header
print(df.iloc[14:25])