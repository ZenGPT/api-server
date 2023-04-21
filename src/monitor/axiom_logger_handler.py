
import logging
import traceback
from dotenv import load_dotenv
from monitor import axiom_client
load_dotenv()

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
    if not axiom_client.is_monitor_enable():
        return
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR|logging.WARNING) 
    logger.addHandler(AxiomLoggerHandler())