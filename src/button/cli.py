import os
import argparse
import importlib
import glob
import time

import colorama
from colorama import Fore, Back, Style
from tabulate import tabulate

from button.tasks import Task


class EnumerationTask(Task):
    def __init__(self, tasks):
        super().__init__("tasks", "display the list of tasks")
        self.tasks = tasks

    def add_arguments(self, parser):
        parser.add_argument("-t", "--tablefmt", type=str, help="table format", default="simple")

    def run(self, parsed):
        groups = {}
        for task in self.tasks:
            name, desc, group = task.name, task.desc, task.group
            if group not in groups:
                groups[group] = []
            groups[group].append((name, desc))

        print("Tasks:")
        for group, tasks in groups.items():
            if group is None:
                group = "default"
            print(f"\n{Fore.GREEN}[ {group} ]{Style.RESET_ALL}")
            print(tabulate(sorted(tasks, key=lambda x: x[0]), tablefmt=parsed.tablefmt))


def main():
    colorama.init()

    parser = argparse.ArgumentParser(description="button", add_help=False)
    parser.add_argument("--taskdir", type=str,
                        default=os.environ.get("BUTTON_TASKDIR", ".button"))
    parser.add_argument("--default", type=str,
                        default=os.environ.get("BUTTON_DEFAULT", "tasks"))
    parser.add_argument("--timing", action="store_false")
    parser.add_argument("--verbose", action="store_true")

    # load user-defined tasks from taskdir
    parsed, _ = parser.parse_known_args()
    tasks = []

    filenames = glob.glob("{}/*.py".format(parsed.taskdir))
    for fn in filenames:
        spec = importlib.util.spec_from_file_location("", fn)
        user_defined = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_defined)
        for task_cls in user_defined.tasks:
            tasks.append(task_cls())

    # define default task "tasks": enumerate tasks
    tasks.append(EnumerationTask(tasks))

    # add subparsers
    subparsers = parser.add_subparsers(title="subcommands")
    for task in tasks:
        task_parser = subparsers.add_parser(task.name, description=task.desc)
        task.add_arguments(task_parser)
        task_parser.set_defaults(func=task.run)

    parsed = parser.parse_args()
    if not hasattr(parsed, "func"):
        parsed = parser.parse_args([parsed.default])

    if hasattr(parsed, "func"):
        if parsed.verbose:
            print(f"[taskdir: {parsed.taskdir}]")
            task_self = parsed.func.__self__
            print(f"[task: {task_self.__class__.__name__}/{task_self.name}]")

        time_started = time.time()
        parsed.func(parsed)
        if not parsed.timing:
            elapsed_secs = time.time() - time_started
            print(f"\n(Task completed in {elapsed_secs:.4f} secs)")
