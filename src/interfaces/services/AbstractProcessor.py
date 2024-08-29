from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod


class AbstractProcessor(ABC):

    @abstractmethod
    def process(
        self,
        image_base64: str, 
        parameters_dict: Dict[str, Any]
    ) -> Tuple[int, str]:
        raise NotImplementedError()