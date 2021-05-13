from abc import ABC, abstractmethod

from .utils import execute_shell_command, execute_shell_script


class Task(ABC):
    def __init__(self, name, desc):
        """Init a task with a name and a description"""
        self.name = name
        self.desc = desc
        self.group = None

    def set_group(self, group):
        self.group = group

    @abstractmethod
    def add_arguments(self, parser):
        """Add a rule to parse arguments"""

    @abstractmethod
    def run(self, parsed):
        """Define a job this task will do"""


class ExecuteCommandTask(Task):
    def __init__(self, alias, desc, command, shell="bash"):
        super().__init__(alias, desc)
        self.command = command
        self.shell = shell

    def add_arguments(self, _parser):
        pass

    def run(self, parsed):
        if parsed.verbose:
            print(f"Command: {self.command}")
        retval, _ = execute_shell_command(self.command, self.shell)
        return retval


class ExecuteScriptTask(Task):
    def __init__(self, alias, desc, script, shell="bash"):
        super().__init__(alias, desc)
        self.script = script
        self.shell = shell

    def add_arguments(self, _parser):
        pass

    def run(self, parsed):
        if parsed.verbose:
            print(f"Parsed: {parsed.__dict__}")

        script = self.script.format(**parsed.__dict__)
        if parsed.verbose:
            print(f"Script: {script}")
        retval, _ = execute_shell_script(script, self.shell)
        return retval
