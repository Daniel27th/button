import datetime
from button.tasks import Task, CommandExecTask

class DisplayDateTask(CommandExecTask):
    def __init__(self):
        super().__init__('date', 'display current datetime', 'date')
        self.set_group('shell')

class MultipleCommandsTask(CommandExecTask):
    def __init__(self):
        script = '''
        MYVAR="hello"
        echo $MYVAR, world
        find ~
        '''
        super().__init__('script', 'executes multiple commands', script)
        self.set_group('shell')

class Epoch2DateTask(Task):
    def __init__(self):
        super().__init__('epoch2date', 'convert epoch to date')

    def add_arguments(self, parser):
        parser.add_argument('epoch', type=int, help='unix epoch value')

    def run(self, parsed):
        print(datetime.datetime.fromtimestamp(parsed.epoch).isoformat())

tasks = [DisplayDateTask, MultipleCommandsTask, Epoch2DateTask]
