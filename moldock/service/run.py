import time

from metaflow import  Runner, Flow

from moldock.service import workflow


class LocalDockingSoftware:
    
    def dock_ligands(self, receptor_path:str, ligand_path: str):
        with Runner(workflow.__file__, show_output=True, environment='local')\
            .run(
                receptor_path=receptor_path,
                ligand_path=ligand_path,
                ) as running:
                print(f'{running.run} completed on')
        
        return Flow("DockingFlow").latest_run.data.results_path
        
                
                
class AwsBatchDockingSoftware:
    
    def dock_ligands(self, receptor_path:str, ligand_path: str):
        with Runner(workflow.__file__, show_output=True)\
            .run(
                receptor_path=receptor_path,
                ligand_path=ligand_path,
                ) as running:
                print(f'{running.run} completed on')
        
        latest_run = Flow("DockingFlow").latest_run

        while not latest_run.finished:
            print("Waiting for docking flow to finish")
            time.sleep(10)
            latest_run = Flow("DockingFlow").latest_run

        return latest_run.data.results_path
