"""
Tautomer Standardization Tool
Part of the Cheminformatics Series: Heterocyclic Analysis
"""

from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
import pandas as pd

def generate_standardized_dataset(df, smiles_column='Raw_SMILES'):
    """
    Processes a DataFrame of SMILES to identify and standardize tautomers.
    """
    work_df = df.copy()
    mols_obj = work_df[smiles_column].apply(Chem.MolFromSmiles)
    enumerator = rdMolStandardize.TautomerEnumerator()

    # 1. Enumerate and Standardize
    tautomer_lists = mols_obj.apply(lambda x: enumerator.Enumerate(x) if x else None)
    work_df['Standardized_SMILES'] = mols_obj.apply(
        lambda x: Chem.MolToSmiles(enumerator.Canonicalize(x)) if x else None
    )

    # 2. Deduplicate
    cleaned_df = work_df.drop_duplicates(subset=['Standardized_SMILES']).copy()

    # 3. Generate Metadata
    cleaned_df['Tautomers_count'] = tautomer_lists.apply(lambda x: len(x) if x else 0)
    cleaned_df['Has_tautomers'] = cleaned_df['Tautomers_count'].apply(lambda x: 'Yes' if x > 1 else 'No')

    return cleaned_df
"""
