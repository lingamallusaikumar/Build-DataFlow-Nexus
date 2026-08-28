import math

class AnomalyDetector:
    """
    Statistical anomaly detection module. 
    In production, this can be swapped with ML models like IsolationForest or Autoencoders.
    """
    @staticmethod
    def detect_z_score_anomalies(data_list, column, threshold=3.0):
        values = [row[column] for row in data_list if isinstance(row.get(column), (int, float))]
        if not values:
            return []
            
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance) if variance > 0 else 1.0
        
        anomalies = []
        for row in data_list:
            val = row.get(column)
            if isinstance(val, (int, float)):
                z_score = abs(val - mean) / std_dev
                if z_score > threshold:
                    anomalies.append(row)
        return anomalies
