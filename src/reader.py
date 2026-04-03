import csv
import os
from interfaces import IOutputStrategy


class DataReader:
    def __init__(self, strategy: IOutputStrategy):
        self._strategy = strategy

    def process_dataset(self, file_path: str):
        # First, calculate the total number of records for cleaner logging
        with open(file_path, mode="r", encoding="utf-8") as f:
            # Subtract 1 to account for the header row
            total_records = sum(1 for line in f) - 1

        # Limit for testing purposes
        limit = 50
        print(
            f"Found {total_records} records in dataset. Processing the first {limit} for testing..."
        )

        data = []
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    if i >= limit:
                        break
                    data.append(row)

            # Pass the data to the selected strategy and execute
            self._strategy.write(data)

            # Return the count of processed records
            return len(data)

        except FileNotFoundError:
            print(f"Error: File not found at path {file_path}")
            return 0
