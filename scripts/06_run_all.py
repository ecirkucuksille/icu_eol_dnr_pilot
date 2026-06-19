from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "01_validate_data.py",
    "02_derive_variables.py",
    "03_descriptive_analysis.py",
    "04_inferential_analysis.py",
    "05_make_figures.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n>>> Running {script}")
        subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=True)
    print("\nAll analyses completed successfully.")


if __name__ == "__main__":
    main()
