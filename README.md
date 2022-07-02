# Thyroid_Disease_Detection
This Repository Contains the ML Prediction Api for Thyroid Disease Detection.

Detailed EDA is uploaded in the file Thyroid Detection EDA and Preprocessing.pdf

Repository has the Following Api.
1. /eda ==> this Api will process the data and Perform some EDA activity such as cleaning the data , checking for the null values, changing the categerocal values into the ordinal values and label encoding, cleaning the output varaiable  etc.
2. /preprocessing ==> this Api will process the data to find the missing values drop the non required columns, and do the feature scalling and get the cluster of the data and save the clustering model into Models folder
3. /train ==> trains the model on the data for 3 algorithm RandomForest, KNN, ExtraTreeClassifier

4. /Predict ==> which predict that the data the person is having thyroid or not. Below are the input send to the api from the form, PFB the same input 
Age:29
Sex:F
On_Thyroxine:f
Query_On_Thyroxine:f
On_Antithyroid_Medication:f
Sick:t
Pregnant:t
Thyroid_Surgery:f
I131_treatment:f
Query_Hypothyroid::t
Query_Hyperthyroid:f
Lithium:f
Goitre:t
Tumor:f
Hypopituitary:f
Psych:f
TSH_Measured:f
TSH:0.05
T3_Measured:f
T3:3.4
TT4_Measured:t
TT4:210
T4U_Measured:t
T4U:1.05
FTI_Measured:f
FTI:199
TBG_Measured:f
TBG:?
Referral_Source::dsfs


To Run the project please refer to the Commands.txt for Refrence 
