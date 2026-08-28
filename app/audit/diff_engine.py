class AuditDiffEngine:
    """
    Computes the exact changes between two JSON states to store in the Audit Log.
    """
    @staticmethod
    def calculate_diff(old_state: dict, new_state: dict) -> dict:
        diff = {
            'added': {},
            'removed': {},
            'modified': {}
        }
        
        old_keys = set(old_state.keys()) if old_state else set()
        new_keys = set(new_state.keys()) if new_state else set()
        
        # Added keys
        for key in new_keys - old_keys:
            diff['added'][key] = new_state[key]
            
        # Removed keys
        for key in old_keys - new_keys:
            diff['removed'][key] = old_state[key]
            
        # Modified keys
        for key in old_keys.intersection(new_keys):
            if old_state[key] != new_state[key]:
                diff['modified'][key] = {
                    'from': old_state[key],
                    'to': new_state[key]
                }
                
        return diff
