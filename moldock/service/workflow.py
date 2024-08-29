from metaflow import FlowSpec, step, Parameter, batch


class DockingFlow(FlowSpec):

    receptor_path = Parameter(
        "receptor_path", type=str, help="Path to receptor pdb file"
    )
    ligand_path = Parameter("ligand_path", type=str, help="Path to ligand sdf file")
    s3_root = Parameter("s3_root", type=str, help="S3 directory to write results to")

    @batch(image='crh201/moldock:latest', cpu=4)
    @step
    def start(self):
        import os
        from moldock.core.smina import Smina
        from moldock.service.utils import download_s3_uri, upload_s3_uri

        # Download input files from S3
        receptor_file = download_s3_uri(self.receptor_path)
        ligand_file = download_s3_uri(self.ligand_path)

        # Run molecular docking
        smina = Smina()
        smina.specify_receptor(receptor_file)
        output_path = smina.dock_ligand(ligand_file)

        # Upload for processing in next step
        self.docking_output_uri = os.path.join(self.s3_root, output_path)
        print(self.docking_output_uri)
        upload_s3_uri(self.docking_output_uri)

        self.next(self.end)

    @batch(image='crh201/moldock:latest', cpu=1)
    @step
    def end(self):
        import os
        from moldock.service.utils import download_s3_uri, upload_s3_uri
        from rdkit.Chem import PandasTools, MolToSmiles

        # Download and read using rdkit tools
        docking_output_file = download_s3_uri(self.docking_output_uri)
        df = PandasTools.LoadSDF(docking_output_file, molColName="_Molecule")

        if "smiles" not in [c.lower() for c in df.columns]:
            df["smiles"] = [MolToSmiles(mol) for mol in df["_Molecule"].tolist()]

        df["minimizedAffinity"] = df["minimizedAffinity"].astype(float)
        df = df.groupby(["smiles"], as_index=False)[["minimizedAffinity"]].mean()
        df.to_csv("averaged_affinity.csv", index=False)
        self.results_path = os.path.join(self.s3_root, "averaged_affinity.csv")
        upload_s3_uri(self.results_path)


if __name__ == "__main__":
    DockingFlow()
