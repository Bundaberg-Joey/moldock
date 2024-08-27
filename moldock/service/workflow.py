from metaflow import FlowSpec, step, Parameter


class DockingFlow(FlowSpec):

    receptor_path = Parameter(
        "receptor_path", type=str, help="Path to receptor pdb file"
    )
    ligand_path = Parameter("ligand_path", type=str, help="Path to ligand sdf file")
    s3_root = Parameter("s3_root", type=str, help="S3 directory to write results to")

    @step
    def start(self):
        import os

        if not (
            os.path.exists(self.receptor_path) and os.path.exists(self.ligand_path)
        ):
            raise ValueError(
                f"Either receptor or ligand specified not available at locations."
            )

        self.next(self.dock)

    @step
    def dock(self):
        from metaflow import S3
        from moldock.core.smina import Smina

        # TODO : download S3 files here for receptor and ligand

        smina = Smina()
        smina.specify_receptor(self.receptor_path)
        output_path = smina.dock_ligand(self.ligand_path)

        with S3(s3_root=self.s3_root) as s3:
            s3.put([("s3_key", output_path)])

        self.next(self.end)

    @step
    def end(self):
        from metaflow import S3
        from rdkit.Chem import PandasTools, MolToSmiles

        with S3(s3_root=self.s3_root) as s3:
            path = s3.get("s3_path_upload_to_before").path
            df = PandasTools.LoadSDF(path, molColName="_Molecule")

        if "smiles" not in [c.lower() for c in df.columns]:
            df["smiles"] = [MolToSmiles(mol) for mol in df["_Molecule"].tolist()]

        df = df.groupby(["smiles"])[["minimizedAffinity"]].mean()

        with S3(s3_root=self.s3_root) as s3:
            s3.put(key="filename", obj=df.to_csv())

        self.results_path = "full path to results in s3"


if __name__ == "__main__":
    DockingFlow()
