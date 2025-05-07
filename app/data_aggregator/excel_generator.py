import pandas as pd
import numpy as np
import os

CSV_DIR = "/spark_output/output_data"
EXCEL_DIR = "/excel_output/final_df.xlsx"

def aggregate_csv_to_excel(csv_dir, excel_path):
    all_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    combined_df = pd.DataFrame()
    #club new csv files together
    for file in all_files:
        file_path = os.path.join(csv_dir, file)
        df = pd.read_csv(file_path)
        if df.empty:
            print("The CSV contains only headers and no data.")
            continue
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    weighted_avg_sentiment = combined_df.groupby("link").apply(lambda x: np.average(x["sentiment"], weights=x["score"]), include_groups=False).reset_index(name="weighted_sentiment")
    print(weighted_avg_sentiment.head(3))
    weighted_avg_sentiment.to_csv("/final_csv/sentiment.csv")

    #write final pandas df to excel file
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode="w") as writer:
        weighted_avg_sentiment.to_excel(writer, index=False, sheet_name='weighted_mean')

    print(f"Data has been aggregated into {excel_path}")

if __name__ == "__main__":
    aggregate_csv_to_excel(CSV_DIR, EXCEL_DIR)
    