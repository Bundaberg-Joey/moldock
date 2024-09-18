from pydantic import BaseModel


class DockingJobRequest(BaseModel):
    uniprot_id: str = 'P63086'
    ligand_path: str
    s3_root: str
    server: str = "local"


class DockingJobResult(BaseModel):
    results_filepath: str


class SmokeTestResult(BaseModel):
    exit_status: str
    finished_at: str
    smoketest_pass: bool
