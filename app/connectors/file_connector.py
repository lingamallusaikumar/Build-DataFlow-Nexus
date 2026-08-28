from app.connectors.base.connector_interface import BaseConnector
import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)

class FileConnector(BaseConnector):
    """
    Handles CSV and Excel data streams.
    In a real environment, this might connect to AWS S3 or Google Cloud Storage to fetch the file bytes.
    """
    def connect(self):
        # Config would contain S3 buckets or local mount paths
        pass

    def test_connection(self):
        # Test bucket access
        return True

    def fetch_data(self, file_bytes, file_type='csv'):
        try:
            if file_type == 'csv':
                df = pd.read_csv(io.BytesIO(file_bytes))
            elif file_type == 'excel':
                df = pd.read_excel(io.BytesIO(file_bytes))
            else:
                raise ValueError("Unsupported file type")
                
            # Replace NaNs with None for JSON serialization
            df = df.where(pd.notnull(df), None)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Failed to parse file: {e}")
            raise

    def push_data(self, file_path, data, file_type='csv'):
        df = pd.DataFrame(data)
        if file_type == 'csv':
            df.to_csv(file_path, index=False)
        elif file_type == 'excel':
            df.to_excel(file_path, index=False)
        return True
