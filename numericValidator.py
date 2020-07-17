import tkinter


class NumericEntry(tkinter.Entry):
    """
    Numeric entry are a class of value entries which do not allow non-numeric values to be entered
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.configure(validate='all', validatecommand=(self.register(self._numeric_validator), "%P"))

    @staticmethod
    def _numeric_validator(value):
        """
        Verifies that the value is a valid floating point number
        :param value: String value to be checked
        :return: True if valid otherwise false
        """
        if value == '':
            # Allow complete deletion
            return True
        try:
            float(value)
            return True
        except ValueError:
            # If conversion fails then the value is not a valid float
            return False
