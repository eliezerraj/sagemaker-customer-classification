# pip install imblearn
# #conda install -c conda-forge imbalanced-learn

import subprocess
import sys
import os
import tempfile
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# install libraries
def install(package):
    print("===> Installing package: ", package)
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# load the requirements
def install_requirements():
    with open('/opt/ml/processing/input/req/requirements.txt', 'r') as f:
        for line in f.readlines():
            install(line.strip())

if __name__ == "__main__":
    print("-------------------- main ----------------------------")
    print("Sagemaker Pipeline version 30/04/2024-v1.0")

    base_dir = "/opt/ml/processing"

    install_requirements()

    # Read Data
    df = pd.read_csv(
        f"{base_dir}/input/customer_profile.csv"
    )

    print("-------------------- dataframe data  ----------------------------")
    print("1. shape : ", df.shape)

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

    print("-------------------- scaling dataframe  -----------------------")

    scaler = StandardScaler()
    df_data_scaled = scaler.fit_transform(df_training).astype('float32')

    print("-------------------- save scaler model -----------------------")
    # Shows scikit-learn version
    import sklearn
    import s3fs
    print("2. sklearn version: ", sklearn.__version__)

    bucket_name = "eliezerraj-908671954593-dataset/customer"
    location_scaler = 's3://{}'.format(bucket_name)

    fs = s3fs.S3FileSystem()
    output_file = os.path.join(location_scaler, "scaler.joblib")

    with fs.open(output_file, 'wb') as f:
        joblib.dump(scaler, f)

    print("3. model saved :", output_file)

    print("-------------------- df_data_scaled  ----------------------------")
    print(df_data_scaled)

    # Save the Dataframes as csv files
    # convert array into dataframe
    print("-------------------- saving dataset  ----------------------------")
    df_data_scaled_final = pd.DataFrame(df_data_scaled).astype('float32')
    df_data_scaled_final.to_csv(f"{base_dir}/train/train_data.csv",
                                header=False,
                                index=False)

    print("location_customer_encoded_data :", location_scaler)

    df_training.to_csv(f"{location_scaler}/customer_encoded_data.csv",
                       header=True,
                       index=False)

    print("Processing completed. Exiting.")