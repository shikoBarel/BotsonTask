from src.anomaly_count import AnomalyCount

if __name__ == "__main__":
    ac = AnomalyCount()
    
    query = ac.load_query_from_json('es_query.json')
    res = ac.execute_query(ac.index_name, query)  
    grouped_df = ac.process_data(res)
    ac.plot_data(grouped_df)

