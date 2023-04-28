import logging
import sys
import traceback
from monitor import axiom_client
class AxiomLoggerHandler(logging.Handler):
    def emit(self, record):
        exc_text = None
        if record.exc_info:
            exc_text = "".join(traceback.format_exception(*record.exc_info))
        event = {
            "name": record.name,
            "levelname": record.levelname,
            "pathname": record.pathname,
            "filename": record.filename,
            "module": record.module,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "created": record.created,
            "msecs": record.msecs,
            "relativeCreated": record.relativeCreated,
            "thread": record.thread,
            "threadName": record.threadName,
            "process": record.process,
            "message": record.getMessage(),
            "exc_info": exc_text,
        }
        try:
            axiom_client.ingest_logging(event)
        except Exception as e:
            print(f"error happen when sending:{event}, details:{e}")
        
def init():  
    open_global_exception()
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    logger.addHandler(AxiomLoggerHandler())

def log_exception():
    logging.getLogger().error("An exception occurred", exc_info=True)

def open_global_exception():
    sys.excepthook = handle_global_exception  

def handle_global_exception(exc_type, exc_value, exc_traceback):
    logging.getLogger().error("Unhandled exception", exc_info=True)
    