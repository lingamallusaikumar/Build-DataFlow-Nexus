from app.pipelines.dag_parser import DAGParser

class PipelineValidator:
    """
    Validates a pipeline configuration before saving or executing.
    """
    @staticmethod
    def validate_config(config):
        errors = []
        
        if not config.get('nodes'):
            errors.append("Pipeline must contain at least one node.")
            return False, errors
            
        try:
            parser = DAGParser(config)
            order = parser.topological_sort()
            
            # Check for disconnected nodes (nodes with 0 in-degree and 0 out-degree, unless it's the only node)
            if len(parser.nodes) > 1:
                for node in parser.nodes:
                    nid = node['id']
                    if parser.in_degree[nid] == 0 and len(parser.adj_list[nid]) == 0:
                        errors.append(f"Node {nid} is disconnected from the pipeline.")
                        
        except ValueError as e:
            errors.append(str(e))
            
        return len(errors) == 0, errors
