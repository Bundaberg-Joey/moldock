from pydantic import BaseModel


class DockingJobRequest(BaseModel):
    receptor_path: str
    ligand_path: str
    server: str='local'


class DockingJobResult(BaseModel):
    results_filepath: str    
        