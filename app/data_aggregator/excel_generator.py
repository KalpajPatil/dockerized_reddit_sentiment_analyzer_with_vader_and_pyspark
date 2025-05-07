import pandas as pd
import os

CSV_DIR = "/spark_output/output_data"
EXCEL_DIR = "/excel_output/final_df.xlsx"

def aggregate_csv_to_excel(csv_dir, excel_path):
    all_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    
    combined_df = pd.DataFrame()

    #read file if already exists
    if os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path, sheet_name='Aggregated Data')
        combined_df = existing_df

    #club new csv files together
    for file in all_files:
        file_path = os.path.join(csv_dir, file)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    group_by_df = combined_df.groupby(["title","link"]).agg(average_Sentiment = ("sentiment","mean")).reset_index()

    final_df = group_by_df

    #write final pandas df to a csv file
    final_df.to_csv("/final_csv/sentiment.csv")

    #write final pandas df to excel file
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Aggregated Data')

    print(f"Data has been aggregated into {excel_path}")

if __name__ == "__main__":
    aggregate_csv_to_excel(CSV_DIR, EXCEL_DIR)
    