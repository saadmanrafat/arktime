import time
import json
import os
from datetime import datetime, timedelta, UTC
from typing import Optional, Dict
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

TASKS_FILE = "tasks.json"


class TaskTimer:
    """
    A CLI timer for tracking time spent on tasks in UTC, saving durations as HH:MM:SS.
    """

    def __init__(self) -> None:
        self.current_task: Optional[str] = None
        self.start_time: Optional[float] = None
        self.paused: bool = True
        self.records: Dict[str, float] = self._load_records()

    def _now_utc(self) -> float:
        return time.time()

    def _format_utc(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, tz=UTC).isoformat()

    def _load_records(self) -> Dict[str, float]:
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    return {task: self._parse_duration(hms) for task, hms in raw.items()}
            except (json.JSONDecodeError, IOError):
                print(Fore.YELLOW + "Warning: Failed to read tasks file. Starting fresh.")
        return {}

    def _save_records(self) -> None:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump({task: self._format_duration(sec) for task, sec in self.records.items()}, f, indent=4)

    def start(self, task: str) -> None:
        if not self.paused:
            print(Fore.YELLOW + "A task is already running. Pause it first.")
            return

        self.current_task = task
        self.start_time = self._now_utc()
        self.paused = False
        print(Fore.GREEN + f"Started task: '{task}' at {self._format_utc(self.start_time)} UTC")

    def pause(self) -> None:
        if self.paused:
            print(Fore.YELLOW + "Timer is already paused.")
            return

        if self.current_task and self.start_time:
            now = self._now_utc()
            duration = now - self.start_time
            self.records[self.current_task] = self.records.get(self.current_task, 0.0) + duration
            print(Fore.CYAN + f"Paused '{self.current_task}' after {self._format_duration(duration)}")
            self._save_records()
        else:
            print(Fore.RED + "No task is currently running.")

        self._reset_timer()

    def _reset_timer(self) -> None:
        self.paused = True
        self.current_task = None
        self.start_time = None

    def report(self) -> None:
        print(Style.BRIGHT + Fore.MAGENTA + "\n=== Time Spent on Tasks (UTC) ===")
        for task, seconds in self.records.items():
            print(Fore.BLUE + f"{task}: {self._format_duration(seconds)}")
        print(Style.BRIGHT + Fore.MAGENTA + "=================================\n")

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """
        Convert seconds → HH:MM:SS string.
        """
        return str(timedelta(seconds=int(seconds)))

    @staticmethod
    def _parse_duration(hms: str) -> float:
        """
        Convert HH:MM:SS string → seconds (float).
        """
        try:
            h, m, s = map(int, hms.split(":"))
            return h * 3600 + m * 60 + s
        except Exception:
            return 0.0


def main() -> None:
    """
    Command-line interface for TaskTimer using match/case.
    """
    timer = TaskTimer()
    print(Style.BRIGHT + Fore.CYAN + "CLI Timer Started. Commands: start <task>, pause, report, exit")

    while True:
        try:
            cmd = input(Fore.WHITE + ">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(Fore.RED + "\nExiting.")
            break

        match cmd.split(maxsplit=1):
            case ["start", task]:
                timer.start(task)
            case ["pause"]:
                timer.pause()
            case ["report"]:
                timer.report()
            case ["exit"]:
                if not timer.paused:
                    timer.pause()
                timer.report()
                break
            case _:
                print(Fore.RED + "Unknown command. Use: start <task>, pause, report, exit")


if __name__ == "__main__":
    main()
