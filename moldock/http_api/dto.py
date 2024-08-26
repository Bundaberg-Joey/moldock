from pydantic import BaseModel


class DockingJobRequest(BaseModel):
    receptor_path: str
    ligand_path: str
    s3_root: str
    server: str = "local"


class DockingJobResult(BaseModel):
    results_filepath: str
