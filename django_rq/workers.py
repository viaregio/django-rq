from django.conf import settings

from rq import Worker
from rq.utils import import_attribute

from .queues import get_queues


def get_exception_handlers():
    """
    Custom exception handlers could be defined in settings.py:
    RQ = {
        'EXCEPTION_HANDLERS': ['path.to.handler'],
    }
    """
    RQ = getattr(settings, 'RQ', {})
    exception_handlers = []
    for path in RQ.get('EXCEPTION_HANDLERS', []):
        handler = import_attribute(path)
        exception_handlers.append(handler)
    return exception_handlers


def get_worker(*queue_names):
    """
    Returns a RQ worker for all queues or specified ones.
    """
    queues = get_queues(*queue_names)
    return Worker(queues,
                  connection=queues[0].connection,
                  exception_handlers=get_exception_handlers() or None)
