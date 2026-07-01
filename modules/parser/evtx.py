import subprocess
import os
import pandas as pd

def run_evtxecmd(evtx_path, output_dir, tool_path):

    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        tool_path,
        "-f", evtx_path,
        "--csv", output_dir
    ]

    subprocess.run(cmd, capture_output=True, text=True)

    files = [f for f in os.listdir(output_dir) if f.endswith(".csv")]

    if not files:
        return []

    latest_csv = os.path.join(output_dir, files[0])

    df = pd.read_csv(latest_csv)

    # normalize column safety
    df = df.fillna("")

    events = []

    for _, row in df.iterrows():

        events.append({
            "event_id": str(row.get("EventID", "")),
            "provider": str(row.get("Provider", "")),
            "level": str(row.get("Level", "")),
            "message": str(row.get("Message", "")),
            "timestamp": str(row.get("TimeCreated", ""))
        })

    return events