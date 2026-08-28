class TransformationEngine:
    """
    Registry for data transformations. Follows the Strategy pattern.
    """
    def __init__(self):
        self.registry = {
            'rename_field': RenameFieldTransformation,
            'drop_field': DropFieldTransformation,
            'cast_type': CastTypeTransformation
        }

    def apply_transformations(self, data, transformations_config):
        """
        Applies a list of transformation configs to the data payload.
        """
        transformed_data = data
        for config in transformations_config:
            transform_type = config.get('type')
            if transform_type in self.registry:
                transformer = self.registry[transform_type](config)
                transformed_data = transformer.apply(transformed_data)
        return transformed_data


class BaseTransformation:
    def __init__(self, config):
        self.config = config

    def apply(self, data):
        raise NotImplementedError("Transformation subclasses must implement 'apply'")


class RenameFieldTransformation(BaseTransformation):
    def apply(self, data):
        old_name = self.config.get('old_name')
        new_name = self.config.get('new_name')
        if old_name in data:
            data[new_name] = data.pop(old_name)
        return data


class DropFieldTransformation(BaseTransformation):
    def apply(self, data):
        field = self.config.get('field')
        if field in data:
            del data[field]
        return data


class CastTypeTransformation(BaseTransformation):
    def apply(self, data):
        field = self.config.get('field')
        target_type = self.config.get('target_type')
        if field in data:
            try:
                if target_type == 'int':
                    data[field] = int(data[field])
                elif target_type == 'float':
                    data[field] = float(data[field])
                elif target_type == 'string':
                    data[field] = str(data[field])
            except (ValueError, TypeError):
                pass # In a real engine, we might log this or route to a dead-letter queue
        return data
