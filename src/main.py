import json
import os
import sys

# Importing our classes
from interfaces import IOutputStrategy
from strategies import ConsoleStrategy, FileStrategy, RedisStrategy, KafkaStrategy
from reader import DataReader


def get_strategy() -> IOutputStrategy:
    """
    Factory method: reads config.json and creates the corresponding strategy object.
    """
    # Build path to the configuration file (one level up from src)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "config.json")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at path: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Get the strategy name from config (default is 'console')
    strategy_name = config.get("output_strategy", "console").lower()

    if strategy_name == "console":
        return ConsoleStrategy()

    elif strategy_name == "file":
        # Get the output file name from config
        output_name = config.get("output_file_name", "result.json")
        output_path = os.path.join(base_dir, "output", output_name)
        return FileStrategy(output_path)

    elif strategy_name == "redis":
        return RedisStrategy()

    elif strategy_name == "kafka":
        return KafkaStrategy()

    else:
        print(
            f"Warning: Strategy '{strategy_name}' is not supported. Using Console instead."
        )
        return ConsoleStrategy()


def main():
    print("=== STARTING DATA PROCESSING PIPELINE ===")

    # Define the path to the dataset
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(
        base_dir, "data", "Bureau_of_Fire_Prevention_Inspections.csv"
    )

    try:
        # 1. Initialize strategy via config
        current_strategy = get_strategy()

        # 2. Create Reader object (Context)
        processor = DataReader(current_strategy)

        # 3. Execute main logic
        processed_count = processor.process_dataset(dataset_path)

        # 4. Final report
        if processed_count and processed_count > 0:
            print("---")
            print(f"RESULT: Pipeline completed successfully.")
            print(f"Total records processed: {processed_count}")
        else:
            print("---")
            print("Warning: Pipeline finished, but no data was processed.")

    except Exception as e:
        print(f"\n[CRITICAL PIPELINE ERROR]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
