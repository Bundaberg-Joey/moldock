from pydantic import BaseModel


class DockingJobRequest(BaseModel):
    receptor_path: str
    ligand_path: str
    s3_root: str
    server: str = "local"


class DockingJobResult(BaseModel):
    results_filepath: str


class SmokeTestResult(BaseModel):
    result: str
    finished_at: str
    expected_result: str
    smoketest_pass: bool
