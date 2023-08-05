class Unit:
    _unit_pretty = '' # This functionality should be filled out in subclasses 
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
    @property
    def unit_code(self):
        return self._unit_code
    @property
    def unit_pretty(self):
        return self._unit_pretty
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

    # Representation dunders
    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name} ({self.unit_code}, {self.value}, {self.max_value}, {self.min_value}, {self.quality_control})'
    def __str__(self):
        """Calling str() on a Unit subclass will return the 'beautified'
        representation of the unit, e.g. '40 km/h'. If you wish to convert the
        raw value into a string, call str(object.value)"""
        return f'{str(self.value)} {self.unit_pretty}'
    def __float__(self):
        return float(self.value)
    def __int__(self):
        return round(self.value)
    
    # Comparison dunders
    def __eq__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return True if self.value == other.value else False
    def __ne__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return True if self.value != other.value else False
    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return True if self.value < other.value else False
    def __le__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return True if self.value <= other.value else False
    def __gt__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return True if self.value > other.value else False
    def __ge__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return True if self.value >= other.value else False
        
    # Math dunders
    def __add__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return self.value + other.value
    def __sub__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return self.value - other.value
    def __mul__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return self.value * other.value
    def __truediv__(self, other):
        if type(other) != type(self):
            raise TypeError(f'Incompatible unit types {type(self).__name__} and {type(other).__name__}')
        else:
            return self.value / other.value
