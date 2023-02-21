import subprocess
from modules.main.decorators import default_decorator


@default_decorator(errormessage='running command error')
def run_command(text: str):
    text = text.split(' ')
    data = subprocess.run(text)
    return {'message': data.stdout}


run_command('ls -l')
