from requests import get, Response


def _confirm_status_code(response: Response, code=200) -> None:
    """Confirm status code is 200, raises exception otherwise.
    """
    if response.status_code != code:
        raise Exception(F'Response returned non 200 status code: {response.content}')


def get_pdb_from_alphafold(uniprot_accession: str) -> str:
    """Retrieves PDB for specified uniprot accession code.
    PDB loaded from alphafold api.

    Parameters
    ----------
    uniprot_accession : str
        valid uniprot  accession code

    Returns
    -------
    str
        pdb file as string
    """
    uniprot_response = get(F'https://alphafold.ebi.ac.uk/api/prediction/{uniprot_accession}')
    _confirm_status_code(uniprot_response)
        
    pdb_response = get(uniprot_response.json()[0]['pdbUrl'])
    _confirm_status_code(pdb_response)
    
    return pdb_response.text
