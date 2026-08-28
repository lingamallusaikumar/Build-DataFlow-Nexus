from app.connectors.base.postgres_connector import PostgresConnector
from app.connectors.rest_connector import RestAPIConnector
from app.connectors.mongodb_connector import MongoDBConnector
from app.connectors.file_connector import FileConnector

class ConnectorRegistry:
    """
    Factory class to dynamically instantiate the correct connector based on type.
    """
    _connectors = {
        'postgres': PostgresConnector,
        'rest_api': RestAPIConnector,
        'mongodb': MongoDBConnector,
        'file': FileConnector
    }

    @classmethod
    def get_connector(cls, connector_type, config):
        connector_class = cls._connectors.get(connector_type)
        if not connector_class:
            raise ValueError(f"Unsupported connector type: {connector_type}")
        return connector_class(config)
        
    @classmethod
    def register_connector(cls, connector_type, connector_class):
        cls._connectors[connector_type] = connector_class
