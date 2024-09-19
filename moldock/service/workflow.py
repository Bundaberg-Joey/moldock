from metaflow import FlowSpec, step, Parameter


class DockingFlow(FlowSpec):

    uniprot_id = Parameter(
        "uniprot_id", type=str, help="Uniprot accession id"
    )
    ligand_path = Parameter("ligand_path", type=str, help="Path to ligand sdf file")
    s3_root = Parameter("s3_root", type=str, help="S3 directory to write results to")

    @step
    def start(self):
        import os
        from moldock.core.smina import Smina
        from moldock.core.protein import get_pdb_from_alphafold
        from moldock.service.utils import download_s3_uri, upload_s3_uri

        # Download ligand file(s) from S3
        ligand_file = download_s3_uri(self.ligand_path)
        
        # Get protein PDB file from alphafold API and write to file
        with open('receptor.pdb', 'w') as f:
            f.write(get_pdb_from_alphafold(self.uniprot_id))
        
        # Run molecular docking
        smina = Smina()
        smina.specify_receptor('receptor.pdb')
        output_path = smina.dock_ligand(ligand_file)

        # Upload for processing in next step
        self.docking_output_uri = os.path.join(self.s3_root, output_path)
        print(self.docking_output_uri)
        upload_s3_uri(self.docking_output_uri)

        self.next(self.end)

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
