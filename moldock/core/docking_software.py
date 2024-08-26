import subprocess

class CliExecutionError(Exception):
    pass


def execute_cli_command(command: str, **kwargs):    
    try:
        process_result = subprocess.run(str(command).split(), **kwargs)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
        raise CliExecutionError(F'{command} failed to run : {e}')
    
    return (r.decode('utf-8') for r in (process_result.stdout, process_result.stderr))



class Smina:
    
    def __init__(self, exhaustiveness: int=8, num_modes: int=9, cpu: int=1):
        self._base_command = F'smina --exhaustiveness {int(exhaustiveness)} --num_modes {int(num_modes)} --cpu {cpu}'
        self._receptor = None
        self._ready_to_dock = False
        
    def specify_receptor(self, receptor_path: str):
        self._receptor = receptor_path
        self._ready_to_dock = True
        
    def dock_ligand(self, ligand_sdf_path):
        if self._ready_to_dock:
            output_path = F"{ligand_sdf_path.split('.')[0]}.docked.sdf"
            command = F'{self._base_command} --receptor {self._receptor} --ligand {ligand_sdf_path} --autobox_ligand {self._receptor} --out {output_path}'
            execute_cli_command(command)
            return output_path
        raise Exception('Receptor not specified, unbable to dock ligand(s)')
