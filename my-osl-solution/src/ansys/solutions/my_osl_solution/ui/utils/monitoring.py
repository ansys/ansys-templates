# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

from pathlib import Path
from typing import Union


def read_log_file(log_file: Union[Path, str]) -> list:

    logs = []

    log_file = Path(log_file)

    if log_file.exists():
        with open(log_file, "r") as file:
            for line in file:
                if len(line.strip().rstrip("\n").replace(" ", "")) > 0:
                    logs.append(line.strip().rstrip("\n"))
    else:
        raise FileNotFoundError(f"Unable to find log file {log_file}.")

    return logs
