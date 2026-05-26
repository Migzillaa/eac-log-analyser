import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# === CONFIGURATION ===
# Put your ProcMon CSV file in the same folder as this script
CSV_FILE = "eac_process_create.CSV"

def load_procmon_csv(file_path):
    """Load ProcMon CSV data."""
    try:
        df = pd.read_csv(file_path)
        print("[+] CSV loaded successfully.")
        print(f"[+] Total rows loaded: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        return None
    except Exception as e:
        print(f"[!] Error loading CSV: {e}")
        return None

def summarise_operations(df):
    """Count ProcMon operation types."""
    if "Operation" not in df.columns:
        print("[!] Operation column not found.")
        return None

    summary = df["Operation"].value_counts().reset_index()
    summary.columns = ["Operation", "Count"]
    return summary

def summarise_processes(df):
    """Count events by process name."""
    if "Process Name" not in df.columns:
        print("[!] Process Name column not found.")
        return None

    summary = df["Process Name"].value_counts().reset_index()
    summary.columns = ["Process Name", "Event Count"]
    return summary

def export_results(operation_summary, process_summary):
    """Export summaries to CSV files."""
    output_folder = Path("analysis_output")
    output_folder.mkdir(exist_ok=True)

    if operation_summary is not None:
        operation_summary.to_csv(output_folder / "operation_summary.csv", index=False)

    if process_summary is not None:
        process_summary.to_csv(output_folder / "process_summary.csv", index=False)

    print("[+] Summary CSV files exported to analysis_output folder.")

def create_operation_chart(operation_summary):
    """Create a simple bar chart of operation counts."""
    if operation_summary is None or operation_summary.empty:
        print("[!] No operation data available for chart.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(operation_summary["Operation"], operation_summary["Count"])
    plt.xlabel("Operation Type")
    plt.ylabel("Count")
    plt.title("ProcMon Operation Counts During Fortnite / Easy Anti-Cheat Runtime")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_folder = Path("analysis_output")
    output_folder.mkdir(exist_ok=True)
    plt.savefig(output_folder / "operation_summary_chart.png")
    print("[+] Chart saved as analysis_output/operation_summary_chart.png")

def main():
    print("=== Easy Anti-Cheat ProcMon Log Analyser ===")

    df = load_procmon_csv(CSV_FILE)

    if df is None:
        return

    print("\nColumns found in CSV:")
    print(list(df.columns))

    operation_summary = summarise_operations(df)
    process_summary = summarise_processes(df)

    print("\n=== Operation Summary ===")
    print(operation_summary)

    print("\n=== Process Summary ===")
    print(process_summary)

    export_results(operation_summary, process_summary)
    create_operation_chart(operation_summary)

    print("\n[+] Analysis complete.")

if __name__ == "__main__":
    main()