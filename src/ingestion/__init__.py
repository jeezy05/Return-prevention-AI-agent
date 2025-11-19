"""Data ingestion module"""

from .amazon_parser import AmazonParser
from .website_parser import WebsiteParser
from .chat_parser import ChatParser
from .review_parser import ReviewParser
from .log_parser import LogParser
from .qc_parser import QCParser

__all__ = [
    'AmazonParser',
    'WebsiteParser',
    'ChatParser',
    'ReviewParser',
    'LogParser',
    'QCParser'
]
