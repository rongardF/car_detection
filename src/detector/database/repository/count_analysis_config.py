
# local imports
from ..model import CountAnalysisConfig
from .base_repository import BaseRepository


class CountAnalysisConfigRepository(BaseRepository[CountAnalysisConfig]):
    
    def __init__(self, engine):
        super().__init__(engine, CountAnalysisConfig)