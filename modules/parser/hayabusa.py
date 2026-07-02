import os
import subprocess
import pandas as pd

def run_hayabusa(evtx_path, output_dir, tool_path):

    os.makedirs(output_dir, exist_ok=True)

    evtx_path = os.path.abspath(evtx_path)
    tool_path = os.path.abspath(tool_path)

    output_file = os.path.join(output_dir, "hayabusa_timeline.csv")
    output_file = os.path.abspath(output_file)

    cmd = [
         tool_path,
        "csv-timeline",
        "-f", evtx_path,
        "-o", output_file,
        "-w",                 # or --no-wizard
        "-C"                  # overwrite output if it exists
]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=False,
        cwd=os.path.dirname(tool_path)
    )

    # DEBUG (IMPORTANT)
    if result.stderr:
        print("HAYABUSA ERROR:", result.stderr.decode(errors="ignore"))

    if not os.path.exists(output_file):
        return []

    df = pd.read_csv(output_file, encoding="utf-8", errors="ignore").fillna("")

    results = []

    for _, row in df.iterrows():
        results.append({
            "timestamp": row.get("Timestamp", ""),
            "event_id": str(row.get("EventID", "")),
            "provider": row.get("Provider", ""),
            "level": row.get("Level", ""),
            "rule": row.get("RuleTitle", ""),
            "message": row.get("Message", "")
        })

    return results