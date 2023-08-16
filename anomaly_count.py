from elasticsearch import Elasticsearch
from decouple import config
import pandas as pd
from sklearn.ensemble import IsolationForest
import json
import matplotlib.pyplot as plt

class AnomalyCount:

    def __init__(self):
        self.es = self.connect_to_elastic_search()
        self.index_name = config('ELASTICSEARCH_INDEX_NAME')

    def connect_to_elastic_search(self):
        es = Elasticsearch(
            [config('ELASTICSEARCH_URL')],
            basic_auth=(config('ELASTICSEARCH_USER'), config('ELASTICSEARCH_PASS'))
        )
        return es

    def load_query_from_json(self, file_path):
        with open(file_path, 'r') as f:
            query = json.load(f)
        return query

    def execute_query(self, index_name, query):
        res = self.es.search(index=index_name, body=query)
        return res

    def process_data(self, res):
        # insert aggregated result to DataFrame
        buckets = res['aggregations']['group_by_User_Geo']['buckets']
        df_data = []

        for bucket in buckets:
            user_geo = bucket['key']
            for bot_bucket in bucket['group_by_Bot_Name']['buckets']:
                bot_name = bot_bucket['key']
                count = bot_bucket['doc_count']
                df_data.append({'User_Geo': user_geo, 'Bot_Name': bot_name, 'event_rate': count})

        grouped_df = pd.DataFrame(df_data)

        # Anomaly Detection using Isolation Forest - detect the top 10 precent outliers
        clf = IsolationForest(contamination=0.10)
        grouped_df['anomaly'] = clf.fit_predict(grouped_df[['event_rate']])
        
        return grouped_df

    def plot_data(self, grouped_df):
        # Visualization
        grouped_df['Geo_Bot'] = grouped_df['User_Geo'] + " - " + grouped_df['Bot_Name']

        plt.figure(figsize=(15, 7))
        plt.plot(grouped_df['Geo_Bot'], grouped_df['event_rate'], 'o', color='blue', label='Normal')

        # Highlight the anomalies
        anomalies = grouped_df[grouped_df['anomaly'] == -1]
        plt.scatter(anomalies['Geo_Bot'], anomalies['event_rate'], color='red', label='Anomaly', s=100, edgecolor='black')

        plt.xlabel('User Geo - Bot Name')
        plt.ylabel('Event Rate')
        plt.title('Event Rates by User Geo and Bot Name')
        plt.legend()
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


