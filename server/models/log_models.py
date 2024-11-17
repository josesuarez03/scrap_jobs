from datetime import datetime
from bson import ObjectId

class Log:
    def __init__(self, route, method, status_code, message, error=None, execution_time=None):
        self.timestamp = datetime.now()
        self.route = route
        self.method = method
        self.status_code = status_code
        self.message = message
        self.error = error
        self.execution_time = execution_time
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "route": self.route,
            "method": self.method,
            "status_code": self.status_code,
            "message": self.message,
            "error": self.error,
            "execution_time": self.execution_time
        }