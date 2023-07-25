class Unit():
    def __init__(
            self,
            unitCode: str,
            value: float,
            maxValue: float = None,
            minValue: float = None,
            qualityControl: str = None
    ):
        self._unit_code = unitCode
        self._value = value
        self._max_value = maxValue
        self._min_value = minValue
        self._quality_control = qualityControl
    
    # Getters and setters
    # TODO: add properties for pretty representations of unit code (e.g km/h instead of wmoUnit:km_h-1)
    @property
    def unit_code(self):
        return self._unit_code
    @property
    def value(self):
        return self._value
    @property
    def max_value(self):
        return self._max_value
    @property
    def min_value(self):
        return self._min_value
    @property
    def quality_control(self):
        return self._quality_control

    # Dunder methods
    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name} ({self.unit_code}, {self.value}, {self.max_value}, {self.min_value}, {self.quality_control})'
    def __str__(self): # Allow the unit to be represented directly as a number
        return str(self.value)
    def __float__(self):
        return float(self.value)
    def __int__(self):
        return round(self.value)
    # TODO: Add dunder methods to enable some math functions like addition and subtraction
    # TODO: Add dunder methods to enable comparison