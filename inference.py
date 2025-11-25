import os
import pandas as pd
import pickle

INPUT_DIR = "/input/logs"
OUTPUT_FILE = "/output/alerts.csv"

def load_model():
    with open("/app/model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

def parse_logs():
    rows = []

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".log") or filename.endswith(".txt"):
            filepath = os.path.join(INPUT_DIR, filename)
            with open(filepath, "r", errors="ignore") as f:
                for line in f:
                    rows.append({"file": filename, "log": line.strip()})

    return pd.DataFrame(rows)

def infer(df, model):
    # simple dummy logic: mark as suspicious if line length > 40
    df["is_suspicious"] = df["log"].apply(lambda x: len(x) > 40)
    df["model_version"] = model.get("version", "unknown")
    return df

def main():
    if not os.path.exists(INPUT_DIR):
        print("Input directory missing! Make sure /input/logs is mounted.")
        return

    df = parse_logs()
    if df.empty:
        print("No logs found in /input/logs")
        return

    model = load_model()
    results = infer(df, model)

    os.makedirs("/output", exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print(f"[+] Alerts saved to {OUTPUT_FILE}")
    print(results.head())

if __name__ == "__main__":
    main()
