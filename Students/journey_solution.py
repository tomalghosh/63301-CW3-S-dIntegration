"""
This is a stub for COMP63301 Coursework 04.
Do not edit or delete any lines given in this file that are marked with a "(s)".
(you can move them to different lines as long as you do not change the overall structure)

Use the test zone at the bottom of this stub to test your code locally.

Place your code below the comments marked "#Your code here" and before the next method.

Remove the comments from the lines that save the CSV files to enable saving the files for use in subsequent questions.

Each method is documented to explain what functionality is to be placed within it.

NOTE: You can create as many more methods as you need. However, you need to add 
self as a parameter of the new method and to call it with the prefix self.name 

EXAMPLE:

    def clean(self,result):
        cleaned = [item[0] for item in result]
        return cleaned

"""

import pandas as pd#(s)
import os#(s)
from sklearn.preprocessing import OneHotEncoder#(s)

class Journey:#(s)
 
    # ---Section 1 --- #
 
    #(Question 1)
    def prepare_csv_data(self,df_1083,df_1415):#(s) 
        """
              
                Use the schema of the CSV file for Site 1083 as the reference schema. Standardise the column names, data types, and formats in the Site 1415 CSV file to match the reference schema. Ensure consistency in naming conventions, date/time formats, and categorical values.
                Merge the harmonised datasets from both sites into a single CSV file. The integrated file should contain all observations from both sites, structured according to the reference schema.
    
                Returns: Tuple: [('Site ID', 'Date', 'Lane', 'Lane Name', 'Direction', 'Direction Name', 'Class Scheme', 'Class', 'Class Name', 'Length (m)', 'Headway (s)', 'Gap (s)', 'Speed (mph)', 'Vehicle Id'), 
                                   (2005, '15/03/2020 14:25:07.123', 3, 'SB_OUT', 2, 'South', 2042, 4, 'Van', 5.8, nan, 1.789, 52.678, 9999),
                                   (2505, '03/08/2020 08:25:09.111', 3, 'SB_OUT', 2, 'South', 2042, 4, 'CAR', 5.8, nan, 0.809, 13.243, 8888), ...]
        
        """
        answers_dir = os.path.join(os.path.dirname(__file__), "student_answer_csvs")#(s)
        os.makedirs(answers_dir, exist_ok=True)#(s)
        output_path = os.path.join(answers_dir, "question1.csv")#(s)

        #Your code here

        ### Step 1 : Harmozine and Standardise Data

        # 1. Harmonize Direction Name
        # Standardise Site 1415's direction text to match Site 1083's "North" (if applicable)
        df_1415.loc[df_1415['Direction'] == 1, 'Direction Name'] = 'North'

        # 2. Harmonise Lane Names
        # Map Site 1415 lane designations to match the reference schema of Site 1083
        df_1415.loc[df_1415['Lane'] == 1, 'Lane Name'] = 'NB_NS'
        df_1415.loc[df_1415['Lane'] == 2, 'Lane Name'] = 'NB_MID'
        df_1415.loc[df_1415['Lane'] == 3, 'Lane Name'] = 'NB_OS'

        # 3. Standardise Date Formats (DD/MM/YYYY HH:MM:SS.mmm)
        df_1083['Date'] = pd.to_datetime(df_1083['Date'])
        df_1415['Date'] = pd.to_datetime(df_1415['Date'])

        df_1083['Date'] = df_1083['Date'].dt.strftime('%d/%m/%Y %H:%M:%S.%f').str[:-3]
        df_1415['Date'] = df_1415['Date'].dt.strftime('%d/%m/%Y %H:%M:%S.%f').str[:-3]

        ### Step 2 : Merge the Dataset 
        df_merged = pd.concat([df_1083, df_1415], ignore_index=True)

        # Sort the data Chronologically by Date
        df_merged = df_merged.sort_values(by='Date').reset_index(drop=True)
        
        #  Remove comment from next line to save the dataframe as a CSV file for use in the next question.
        df_merged.to_csv(output_path, index=False)#(s)

        ### Step 3 : Return Output Format (Headers + first 10 rows as tuples)
        columns = tuple(df_merged.columns)
        top_10_rows = list(df_merged.head(10).itertuples(index=False, name=None))
        return [columns] + top_10_rows

        #Your code here

        pass

    #(Question 2)
    def prepare_csv_json_data(self,df_q1,collection):#(s)
        """
                Integrate the traffic and weather datasets. A key for integration needs to be identified for this purpose. Ensure both fields (used as key for the integration) are properly formatted and aligned in terms of date/time granularity.
                To enable integration, check whether aggregation of any of the involved datasets needs to be performed and perform it, if necessary. 
                
                For each time interval:
                    Compute averages for all relevant numeric columns (e.g., Headway, Gap, Speed).
                    Replace individual vehicle-level data with these aggregated values.
                    Count the number of vehicles and include this as a Vehicle Count column.

                Harmonise categorical values where necessary:
                For example, merge directional values such as ‘North’ and ‘Northeast’ into a single category called ‘NorthernQuadrant’, and assign it a code of ‘1’.
        
                Returns: Tuple: [ ('local_time', 'StartSite ID', 'EndSite ID', 'Direction', 'Direction Name', 'AVG Headway (s)', 'AVG Gap (s)', 'AVG Speed (mph)', 'Vehicle Count', 'city', 'position', 'weather_conditions', 'temperature', 'pressure', 'wind_speed', 'humidity'),
                                 ('01/01/2020 00:00:00.000', 1000, 2000, 1, 'NorthernQuadrant', 15.500000, 14.700000, 39.876543, 500, 'SampleCity', '16.2228,-1.2150', 'Clear', 10.0, 1012, 4.0, 65), 
                                 ('03/08/2018 18:20:03.000', 1111, 1515, 1, 'NorthQuadrant', 28.316009, 28.118414, 36.563302, 516, 'Leicester', '11.4808,-2.2300', 'Snow', 2.6, 992, 0.7, 77), ,...]
        """
        answers_dir = os.path.join(os.path.dirname(__file__), "student_answer_csvs")#(s)
        os.makedirs(answers_dir, exist_ok=True)#(s)
        output_path = os.path.join(answers_dir, "question2.csv")#(s) 

        
        #Your code here

        ### Step 1: Load Weather Data from MongoDB Collection
        weather_docs = list(collection.find({}))
        df_weather = pd.DataFrame(weather_docs)
        if '_id' in df_weather.columns:
            df_weather = df_weather.drop(columns=['_id'])

        ### Step 2: Align Date/Time Granularity
        df_q1['dt'] = pd.to_datetime(df_q1['Date'], format='%d/%m/%Y %H:%M:%S.%f')
        df_q1['hour_key'] = df_q1['dt'].dt.strftime('%d/%m/%Y %H:00:00.000')

        # Ensure df_weather has local_time parsed to match hourly format
        df_weather['dt'] = pd.to_datetime(df_weather['local_time'])
        df_weather['hour_key'] = df_weather['dt'].dt.strftime('%d/%m/%Y %H:00:00.000')
        
        # Drop raw 'local_time' from weather temporarily to avoid collision suffix (_x / _y) during merge
        df_weather = df_weather.drop(columns=['local_time'])

        ### Step 3: Categorical Harmonisation
        df_q1['Direction Name'] = df_q1['Direction Name'].replace({
            'North': 'NorthernQuadrant', 
            'NorthEast': 'NorthernQuadrant', 
            'Northeast': 'NorthernQuadrant'
        })
        df_q1['Direction'] = 1

        ### Step 4: Data Aggregation by Hour & Direction
        agg_rules = {
            'Headway (s)': 'mean',
            'Gap (s)': 'mean',
            'Speed (mph)': 'mean',
            'Vehicle Id': 'count'
        }
        
        df_agg = df_q1.groupby(['hour_key', 'Direction', 'Direction Name']).agg(agg_rules).reset_index()
        df_agg = df_agg.rename(columns={
            'hour_key': 'local_time',
            'Headway (s)': 'AVG Headway (s)',
            'Gap (s)': 'AVG Gap (s)',
            'Speed (mph)': 'AVG Speed (mph)',
            'Vehicle Id': 'Vehicle Count'
        })
        
        # Round numeric averages to exactly 6 decimal places
        df_agg['AVG Headway (s)'] = df_agg['AVG Headway (s)'].round(6)
        df_agg['AVG Gap (s)'] = df_agg['AVG Gap (s)'].round(6)
        df_agg['AVG Speed (mph)'] = df_agg['AVG Speed (mph)'].round(6)

        ### Step 5: Left Join with Weather Data
        df_merged = pd.merge(df_agg, df_weather, left_on='local_time', right_on='hour_key', how='left')
        
        df_merged.insert(1, 'StartSite ID', 1083)
        df_merged.insert(2, 'EndSite ID', 1415)

        desired_cols = [
            'local_time', 'StartSite ID', 'EndSite ID', 'Direction', 'Direction Name',
            'AVG Headway (s)', 'AVG Gap (s)', 'AVG Speed (mph)', 'Vehicle Count',
            'city', 'position', 'weather_conditions', 'temperature', 'pressure', 'wind_speed', 'humidity'
        ]
        
        existing_cols = [c for c in desired_cols if c in df_merged.columns]
        df_merged = df_merged[existing_cols]
        df_merged = df_merged.sort_values(by='local_time').reset_index(drop=True)

        #  Remove comment from next line to save the dataframe as a CSV file for use in the next question.
        df_merged.to_csv(output_path, index=False)#(s)

        ### Step 6: Return column names and first 10 rows as tuples
        columns = tuple(df_merged.columns)
        top_10_rows = list(df_merged.head(10).itertuples(index=False, name=None))
        return [columns] + top_10_rows
    
        #Your code here

        pass

    #(Question 3)
    def prepare_csv_relational_data(self,conn,df_q2):#(s) 
        """
            Extract the relevant site and distance data from the SQLite database, specifically for the route from origin site 1083 to destination site 1415. It is worth pointing out that the distance data values appearing in the database are given in km.
            Join this data with the CSV file resulting from Task 2. The result should be a single CSV file that includes all previously integrated traffic and weather data, along with the distance between the two sites.
         
            Returns: Tuple: [('local_time', 'StartSite ID', 'EndSite ID', 'Distance', 'Direction', 'Direction Name', 'AVG Headway (s)', 'AVG Gap (s)', 'AVG Speed (mph)', 'Vehicle Count', 'city', 'position', 'weather_conditions', 'temperature', 'pressure', 'wind_speed', 'humidity'),
                              ('01/01/2020 00:00:00.000', 1000, 2000, 2.500000, 1, 'NorthQuadrant', 15.000000, 14.800000, 40.123456, 500, 'SampleCity', '00.0000,00.0000', 'Clear', 10.0, 1010, 5.0, 60),
                              ('09/15/2019 14:30:00.000', 1157, 1389, 2.034512, 0, 'EasternQuadrant', 29.782145, 29.615907, 35.482199, 472, 'Leeds', '53.8008,-1.5491', 'Rain', 3.1, 987, 0.5, 81), ....]
        """
        answers_dir = os.path.join(os.path.dirname(__file__), "student_answer_csvs")#(s)
        os.makedirs(answers_dir, exist_ok=True)#(s)
        output_path = os.path.join(answers_dir, "question3.csv")#(s) 

        #Your code here

        ### Step 1: Extract Distance Data from SQLite Database
        query = "SELECT * FROM DistanceBetweenSites WHERE StartSiteID = 1083 AND EndSiteID = 1415"
        df_db = pd.read_sql(query, conn)

        ### Step 2: Convert km to miles and round to 6 decimal places
        distance_km = df_db['Distance'].iloc[0] if not df_db.empty else 0.0
        distance_miles = round(distance_km * 0.621371, 6)

        ### Step 3: Merge Distance with Task 2 DataFrame
        df_merged = df_q2.copy()
        
        # Insert Distance column just after EndSite ID (Index 3 or 4th column) as it is required in the output format
        df_merged.insert(3, 'Distance', distance_miles)

        # Ensure exact column order specified for Question 3
        desired_cols = [
            'local_time', 'StartSite ID', 'EndSite ID', 'Distance', 'Direction', 'Direction Name',
            'AVG Headway (s)', 'AVG Gap (s)', 'AVG Speed (mph)', 'Vehicle Count',
            'city', 'position', 'weather_conditions', 'temperature', 'pressure', 'wind_speed', 'humidity'
        ]
        
        existing_cols = [c for c in desired_cols if c in df_merged.columns]
        df_merged = df_merged[existing_cols]
        df_merged = df_merged.sort_values(by='local_time').reset_index(drop=True)

        #  Remove comment from next line to save the dataframe as a CSV file for use in the next question.
        df_merged.to_csv(output_path, index=False, float_format="%.6f")#(s)

        ### Step 4: Return column names and first 10 rows as tuples

        columns = tuple(df_merged.columns)
        top_10_rows = list(df_merged.head(10).itertuples(index=False, name=None))
        return [columns] + top_10_rows

        #Your code here

        pass
        

    #(Question 4)
    def prepare_final_data(self,df_q3,JT_archive):#(s) 
        """
            Join the CSV file from Question 3 with the journey time archive file. A join key needs to be identified for this purpose.
            The result should be a single CSV file that is going to be build that includes all previously integrated traffic, weather, and site data, along with the corresponding Journey Time values.
            
            Returns: Tuple:  [('local_time', 'StartSite ID', 'EndSite ID', 'Journey Time', 'Distance', 'Direction', 'Direction Name', 'AVG Headway (s)', 'AVG Gap (s)', 'AVG Speed (mph)', 'Vehicle Count', 'city', 'position', 'weather_conditions', 'temperature', 'pressure', 'wind_speed', 'humidity'),
                             ('01/01/2020 00:00:00.000', 1000, 2000, 2.500000, 1, 'NorthQuadrant', 15.000000, 14.800000, 40.123456, 500, 'SampleCity', '00.0000,00.0000', 'Clear', 10.0, 1010, 5.0, 60, 0.1000),
                             ('11/23/2019 09:15:00.000', 1128, 1392, 2.045783, 0, 'WesternQuadrant', 21.487923, 21.264812, 37.104827, 812, 'Liverpool', '53.4084,-2.9916', 'Light Snow', -0.8, 1004, 4.3, 68, 0.0472), .... ]
        """
        answers_dir = os.path.join(os.path.dirname(__file__), "student_answer_csvs")#(s)
        os.makedirs(answers_dir, exist_ok=True)#(s)
        output_path = os.path.join(answers_dir, "question4.csv")#(s) 

        #Your code here

        ### Step 1: Load Journey Time Archive
        if isinstance(JT_archive, str):
            df_jt = pd.read_csv(JT_archive)
        else:
            df_jt = JT_archive.copy()

        ### Step 2: Standardise Time Format for Merging
        df_q3['dt'] = pd.to_datetime(df_q3['local_time'], format='%d/%m/%Y %H:%M:%S.%f', errors='coerce')
        if df_q3['dt'].isna().all():
            df_q3['dt'] = pd.to_datetime(df_q3['local_time'])
        df_q3['join_key'] = df_q3['dt'].dt.strftime('%d/%m/%Y %H:00:00.000')

        df_jt['dt'] = pd.to_datetime(df_jt['local_time'], errors='coerce')
        if df_jt['dt'].isna().all():
            df_jt['dt'] = pd.to_datetime(df_jt['local_time'])
        df_jt['join_key'] = df_jt['dt'].dt.strftime('%d/%m/%Y %H:00:00.000')

        df_jt_clean = df_jt.drop(columns=['local_time', 'dt'], errors='ignore')

        ### Step 3: Merge with Question 3 DataFrame
        df_merged = pd.merge(
            df_q3.drop(columns=['dt'], errors='ignore'), 
            df_jt_clean, 
            on='join_key', 
            how='left'
        )

        df_merged = df_merged.drop(columns=['join_key'], errors='ignore')

        ### Step 4: Insert Journey Time at Index 3 (immediately after EndSite ID column)
        if 'Journey Time' in df_merged.columns:
            jt_col = df_merged.pop('Journey Time')
            df_merged.insert(3, 'Journey Time', jt_col)

        desired_cols = [
            'local_time', 'StartSite ID', 'EndSite ID', 'Journey Time', 'Distance', 'Direction', 'Direction Name',
            'AVG Headway (s)', 'AVG Gap (s)', 'AVG Speed (mph)', 'Vehicle Count',
            'city', 'position', 'weather_conditions', 'temperature', 'pressure', 'wind_speed', 'humidity'
        ]
        
        existing_cols = [c for c in desired_cols if c in df_merged.columns]
        df_merged = df_merged[existing_cols]
        df_merged = df_merged.sort_values(by='local_time').reset_index(drop=True)

        #  Remove comment from next line to save the dataframe as a CSV file for use in the next question.
        df_merged.to_csv(output_path, index=False, float_format="%.6f")#(s)

        ### Step 5: Return column names and first 10 rows as tuples
        columns = tuple(df_merged.columns)
        top_10_rows = list(df_merged.head(10).itertuples(index=False, name=None))
        return [columns] + top_10_rows

        #Your code here

        pass
      
    #(Question 5)
    def result_and_encode_data(self,df_q4):#(s)
        """
         	Apply one-hot encoding to the weather_conditions column in your dataset. This process will automatically convert each unique weather condition into a separate binary feature, allowing the model to interpret categorical weather data numerically.
            After encoding, select the following columns as input features for your machine learning model.
         
            Returns: Tuple:( ('local_time', 'StartSite ID', 'EndSite ID', 'Distance', 'AVG Speed (mph)', 'AVG Headway (s)', 'AVG Gap (s)', 'Vehicle Count', 'city', 'position', 'temperature', 'pressure', 'wind_speed', 'humidity', 'Journey Time', 'weather_Clear', 'weather_Cloudy', 'weather_Fog', 'weather_Heavy Rain', 'weather_Light Rain', 'weather_Mist', 'weather_Partly Cloudy', 'weather_Snow'),
                            ('01/01/2020 00:00:00.000', 1000, 2000, 2.500000, 40.123456, 15.000000, 14.500000, 500, 'SampleCity', '00.0000,00.0000', 10.0, 1010, 5.0, 60, 0.1000, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                           ('10/12/2019 09:30:00.000', 1142, 1388, 2.037654, 37.214589, 21.583421, 21.302774, 796, 'Leeds', '53.8008,-1.5491', -0.9, 1003, 4.6, 67, 0.0483, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0), ..)

        """

        ohe = OneHotEncoder(sparse_output=False, drop=None) #(s)
        
        #Your code here

        ### Step 1: Apply One-Hot encoding to weather_conditions
        encoded_weather = ohe.fit_transform(df_q4[['weather_conditions']])
        encoded_col_names = ohe.get_feature_names_out(['weather_conditions'])
        
        df_encoded = pd.DataFrame(encoded_weather, columns=encoded_col_names, index=df_q4.index)
        df_concat = pd.concat([df_q4, df_encoded], axis=1)

        ### Step 2: Define Target Feature Columns
        expected_features = [
            'local_time', 'StartSite ID', 'EndSite ID', 'Distance', 'AVG Speed (mph)', 
            'AVG Headway (s)', 'AVG Gap (s)', 'Vehicle Count', 'city', 'position', 
            'temperature', 'pressure', 'wind_speed', 'humidity', 'Journey Time', 
            'weather_Clear', 'weather_Cloudy', 'weather_Fog', 'weather_Heavy Rain', 
            'weather_Light Rain', 'weather_Mist', 'weather_Partly Cloudy', 'weather_Snow'
        ]

        # Ensure any weather columns not present in the dataframe are initialized with 0.0
        for col in expected_features:
            if col not in df_concat.columns:
                df_concat[col] = 0.0

        ### Step 3: Select Features and Sort Chronologically
        df_final = df_concat[expected_features].copy()
        df_final = df_final.sort_values(by='local_time').reset_index(drop=True)

        ### Step 4: Return column names and first 10 rows as tuples
        columns = tuple(df_final.columns)
        top_10_rows = list(df_final.head(10).itertuples(index=False, name=None))
        return [columns] + top_10_rows

        #Your code here
        
        pass

# ---Test Zone --- #

"""
Remove the comments below to test your solution locally. Once the solution is finalised, reapply the comments as they are currently.
"""

from pymongo.mongo_client import MongoClient
import sqlite3

if __name__ == '__main__':

    # Build paths to the CSV files in the parent folder
    df_1083_path = os.path.join(os.path.dirname(__file__), "rawpvr_2018-02-01_28d_1083.csv")
    df_1415_path = os.path.join(os.path.dirname(__file__), "rawpvr_2018-02-01_28d_1415.csv")

    #You can place any ad-hoc testing here
    my_instance = Journey()
    df_1083  = pd.read_csv(df_1083_path)
    df_1415 = pd.read_csv(df_1415_path)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print(df_1083.dtypes)
    print(df_1415.dtypes)
    print(df_1083.head(10))
    print(df_1415.head(10))
    
    print(df_1083[["Lane", "Lane Name"]].drop_duplicates().sort_values(by="Lane"))
    print(df_1415[["Lane", "Lane Name"]].drop_duplicates().sort_values(by="Lane"))

    print(df_1083[["Direction", "Direction Name"]].drop_duplicates().sort_values(by="Direction"))
    print(df_1415[["Direction", "Direction Name"]].drop_duplicates().sort_values(by="Direction"))

    print(df_1083[["Class", "Class Name"]].drop_duplicates().sort_values(by="Class"))
    print(df_1415[["Class", "Class Name"]].drop_duplicates().sort_values(by="Class"))


    print("Original 1083 rows:", len(df_1083))
    print("Original 1415 rows:", len(df_1415))
    print("Expected Merged rows:", len(df_1083) + len(df_1415))

    print("Question 1")
    print(my_instance.prepare_csv_data(df_1083,df_1415))

    # local mongoDB db, DO NOT CHANGE
    uri = "mongodb://localhost:27017/"

    # Create a new client and connect to the server
    client = MongoClient(uri)

    db = client["coursework4"]
    collection = db["February2018"]

    df_q1_path = os.path.join(os.path.dirname(__file__), "student_answer_csvs/question1.csv")
    df_q1 = pd.read_csv(df_q1_path)

    print("Question 2")
    print(my_instance.prepare_csv_json_data(df_q1,collection))

    df_q2_path = os.path.join(os.path.dirname(__file__), "student_answer_csvs/question2.csv")
    df_q2 = pd.read_csv(df_q2_path)

    ORIGINAL_DB = "coursework4.db"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    original_db_path = os.path.join(base_dir, ORIGINAL_DB)
    conn = sqlite3.connect(original_db_path)

    print("Question 3")
    print(my_instance.prepare_csv_relational_data(conn,df_q2))

    conn.close()

    df_q3_path = os.path.join(os.path.dirname(__file__), "student_answer_csvs/question3.csv")
    JT_archive_path = os.path.join(os.path.dirname(__file__), "JTarchive_1083to1415_Tues_Sun_00-23hours_01-28_Feb_2018.csv")

    df_q3 = pd.read_csv(df_q3_path)
    JT_archive = pd.read_csv(JT_archive_path)

    print("Question 4")
    print(my_instance.prepare_final_data(df_q3,JT_archive))

    df_q4_path = os.path.join(os.path.dirname(__file__), "student_answer_csvs/question4.csv")

    df_q4 = pd.read_csv(df_q4_path)

    print("Question 5")
    print(my_instance.result_and_encode_data(df_q4))





