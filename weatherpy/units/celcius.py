from .unit import Unit

class Celcius(Unit):
    _unit_pretty = 'degrees Celcius'
    
    def __init__(
            self,
            value,
            min_value = None,
            max_value = None,
            quality_control = None
            ):
        super().__init__(self, value, min_value, max_value, quality_control)
