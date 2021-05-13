import os
import shlex
import subprocess
import tempfile


def execute_shell_command(command, shell="bash", preserve_output=False):
    lines = []
    cmd = f"{shell} -c '{command}'"
    p = subprocess.Popen(shlex.split(cmd),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        line_utf8 = line.decode('utf-8').rstrip()
        print(line_utf8)
        if preserve_output:
            lines.append(line_utf8)
    retval = p.poll()
    return retval, lines

def execute_shell_script(commands, shell="bash", preserve_output=False):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file_ptr:
        file_ptr.write(commands)
        filename = file_ptr.name
    try:
        cmd = f"{shell} {filename}"
        return execute_shell_command(cmd, shell, preserve_output)
    finally:
        os.remove(filename)
