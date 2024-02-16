from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import logging
from datetime import datetime


class LoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file_path = 'appointment/logfiles/logfile.log'

    def __call__(self, request):
        self.log_request(request)
        response = self.get_response(request)
        return response

    def log_request(self, request):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        method = request.method
        path = request.path
        log_message = f"[{timestamp}] {method} {path}\n"
        try:
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(log_message)
        except Exception as e:
            print(f"Error writing to log file: {e}")
