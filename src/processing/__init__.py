"""Processing module"""

from .normalizer import Normalizer
from .classifier import Classifier
from .pattern_detector import PatternDetector
from .aggregator import Aggregator

__all__ = [
    'Normalizer',
    'Classifier',
    'PatternDetector',
    'Aggregator'
]
