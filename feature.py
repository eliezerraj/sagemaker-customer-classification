# pip install imblearn
# #conda install -c conda-forge imbalanced-learn

import subprocess
import sys
import os
import tempfile
import numpy as np
import pandas as pd

# install libraries
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# load the requirements
def install_requirements():
    with open('/opt/ml/processing/input/req/requirements.txt', 'r') as f:
        for line in f.readlines():
            install(line.strip())

if __name__ == "__main__":

    base_dir = "/opt/ml/processing"

    install_requirements()

    # Read Data
    df = pd.read_csv(
        f"{base_dir}/input/customer_profile.csv"
    )

    print("-------------------- dataframe data  ----------------------------")
    print("shape : ", df.shape)

    #Cleaning and econding
    df_customer = df.filter(['CLIENTNUM',
                            'Customer_Age',
                            'Gender',
                            'Dependent_count',
                            'Education_Level',
                            'Marital_Status',
                            'Income_Category',
                            'Months_on_book'],
                            axis=1)

    print("-------------------- df_customera  ----------------------------")
    print(df_customer.head(3))

    education_map = {'Uneducated': 0,
                     'Unknown': 0,
                     'High School': 1,
                     'College': 2,
                     'Graduate': 3,
                     'Post-Graduate': 4,
                     'Doctorate': 5}

    income_map = {'Unknown': 0,
                  'Less than $40K': 1,
                  '$40K - $60K':2,
                  '$60K - $80K': 3,
                  '$80K - $120K':4,
                  '$120K +': 5}

    df_customer['Education_Level_Quality'] = df_customer['Education_Level'].map(education_map)
    df_customer['Income_Category_Quality'] = df_customer['Income_Category'].map(income_map)

    df_training = df_customer[['Customer_Age',
                               'Dependent_count',
                               'Education_Level_Quality',
                               'Income_Category_Quality']]

    print("-------------------- df_training  ----------------------------")
    print(df_training.head(3))

    # Save the Dataframes as csv files
    df_training.to_csv(f"{base_dir}/train/train_data.csv", header=True, index=False)

    print("## Processing completed. Exiting.")