import streamlit as st
import pickle
import pandas as pd
from FeaturizerClass import Featurizer

st.image(
    'data/streamlit/cat.webp',
)
st.title('☆ THE Solubility Prediction App ☆')
st.write('Predict the solubility of molecules based on their SMILES strings.')

# Load the pre-trained model and featurizer
with open('data/streamlit/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('data/streamlit/feat.pkl', 'rb') as f2:
    featurizer = pickle.load(f2)

# Input SMILES from user
smiles = st.text_area(
    '**Enter one or more SMILES strings (one per line):**', ''
    )

if st.button('**I want to know**'):  # Execute when the button is clicked
    if not smiles.strip():
        st.write(":red[Enter at least one valid SMILES string to proceed!]")
        st.stop()

    # Process the SMILES strings
    smiles_list = smiles.strip().split('\n')  # Split by newlines

    try:
        # Create a DataFrame from the input
        dfsmiles = pd.DataFrame({'SMILES': smiles_list})

        # Featurize and predict
        smile_pred = featurizer.featurize(dfsmiles['SMILES'])
        predictions = model.predict(smile_pred)

        # Display the results in a table
        result_df = pd.DataFrame({
            'SMILES': smiles_list,
            'Predicted Solubility': predictions
        })
        st.write(result_df)

    except Exception as e:
        st.write(f":red[Error occurred: {e}]")
