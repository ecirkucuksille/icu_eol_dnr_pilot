"""Check factual reporting fields without inventing study history."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "docs/study_reporting_metadata.json").read_text())
pending = [k for k, v in data.items() if v is None]
if pending:
    print("AUTHOR INFORMATION REQUIRED")
    print("\n".join(pending))
    raise SystemExit(1)
if not data["public_data_sharing_authorization_confirmed"]:
    raise SystemExit("Data-sharing statement requires author confirmation")
if not (data["n_eligible"] >= data["n_invited"] >= data["n_participated"]):
    raise SystemExit("Recruitment counts are inconsistent")
print("Reporting fields filled; verify against the official study records.")
