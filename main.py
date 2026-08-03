import argparse
import sys

from pawpal_ai.agent import PawPalPlanningAgent
from pawpal_ai.io_utils import load_scenario, format_result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PawPal AI: reliable pet-care scheduling assistant"
    )
    parser.add_argument(
        "--input",
        default="data/sample_day.json",
        help="Path to a JSON scenario file.",
    )
    parser.add_argument(
        "--log",
        default="logs/agent_trace.md",
        help="Path where agent traces are appended.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        pets, tasks, start_hour, end_hour = load_scenario(args.input)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 1

    agent = PawPalPlanningAgent(log_path=args.log)
    result = agent.build_schedule(
        pets,
        tasks,
        available_start_hour=start_hour,
        available_end_hour=end_hour,
    )
    print(format_result(result))
    return 0 if result.status in {"success", "partial"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
