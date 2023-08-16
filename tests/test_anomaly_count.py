from anomaly_count import AnomalyCount
import pytest

class TestAnomalyCount:

    @pytest.fixture(scope="module")
    def anomaly_instance(self):
        return AnomalyCount()

    def test_connect_to_elastic_search(self, anomaly_instance):
        es = anomaly_instance.connect_to_elastic_search()
        assert es is not None, "Elasticsearch connection failed."

    def test_load_query_from_json(self, anomaly_instance):
        query = anomaly_instance.load_query_from_json('es_query.json')
        assert isinstance(query, dict), "Failed to load the query from JSON file."
        assert "aggs" in query, "Query does not have the expected structure."

    def test_execute_query(self, anomaly_instance):
        query = anomaly_instance.load_query_from_json('es_query.json')
        res = anomaly_instance.execute_query(anomaly_instance.index_name, query)
        assert "aggregations" in res, "Query execution failed or returned unexpected result."

    def test_process_data(self, anomaly_instance):
        query = anomaly_instance.load_query_from_json('es_query.json')
        res = anomaly_instance.execute_query(anomaly_instance.index_name, query)
        grouped_df = anomaly_instance.process_data(res)
        assert not grouped_df.empty, "Data processing failed or returned empty DataFrame."
        assert "anomaly" in grouped_df.columns, "Anomaly detection not applied to DataFrame."

    # For plotting, you might just ensure the function runs without error
    def test_plot_data(self, anomaly_instance):
        query = anomaly_instance.load_query_from_json('es_query.json')
        res = anomaly_instance.execute_query(anomaly_instance.index_name, query)
        grouped_df = anomaly_instance.process_data(res)
        anomaly_instance.plot_data(grouped_df)