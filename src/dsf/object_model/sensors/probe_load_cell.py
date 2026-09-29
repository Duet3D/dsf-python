from ..model_collection import ModelCollection
from ..model_object import ModelObject
from ..utils import model_prop


class ProbeLoadCell(ModelObject):
    """Information about a load cell probe"""

    # Force measured by the load cell relative to the last tare (in g)
    force = model_prop("force", float, 0)

    # Scale of the load cell (in g per count)
    grams_per_count = model_prop("grams_per_count", float, 0)

    # Preload of the load cell at the last tare (in g)
    preload = model_prop("preload", float, 0)

    # Safe window for the preload (in g, low and high limit). Two equal values disable the check
    preload_window = model_prop("preload_window", ModelCollection[float], ModelCollection(float, [0.0, 0.0]))

    def __init__(self):
        super(ProbeLoadCell, self).__init__()
