import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from sklearn.preprocessing import StandardScaler


class Featurizer:
    def __init__(self, smiles):
        """
        Initialize the Featurizer with training SMILES strings.
        Calculate descriptors and fit a scaler to the training data.
        """

        self.descriptors = self._calculate_descriptors(smiles)
        self.scaler = StandardScaler()
        self.scaler.fit(self.descriptors)

    def _calculate_descriptors(self, smiles):
        """
        Calculate molecular descriptors for a list of SMILES strings.
        Returns a pandas DataFrame with the descriptors.
        """
        mols = [Chem.MolFromSmiles(s) for s in smiles]
        descriptors = {
            'mol_wt': [rdMolDescriptors.CalcExactMolWt(mol) for mol in mols],
            'logp': [
                rdMolDescriptors.CalcCrippenDescriptors(mol)[0] for mol in mols
                ],
            'num_heavy_atoms': [
                rdMolDescriptors.CalcNumHeavyAtoms(mol) for mol in mols
                ],
            'num_HBD': [rdMolDescriptors.CalcNumHBD(mol) for mol in mols],
            'num_HBA': [rdMolDescriptors.CalcNumHBA(mol) for mol in mols],
            'aromatic_rings': [
                rdMolDescriptors.CalcNumAromaticRings(mol) for mol in mols
                ]
        }
        return pd.DataFrame(descriptors)

    def featurize(self, smiles):
        """
        Featurize a list of SMILES strings by calculating and standardizing
        molecular descriptors.
        Returns a pandas DataFrame with scaled descriptors.
        """
        descriptors = self._calculate_descriptors(smiles)
        scaled_descriptors = self.scaler.transform(descriptors)
        # Standardize the descriptors
        return pd.DataFrame(scaled_descriptors, columns=descriptors.columns)
