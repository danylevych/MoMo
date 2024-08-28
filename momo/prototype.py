import pandas as pd


class Prototype(pd.Series):
    """
    A custom subclass of pd.Series representing a prototype.

    Parameters:
    - data (array-like, Iterable, dict, or scalar): The data to be stored in the prototype.
    - index (array-like or Index (1d)): The index labels associated with the data.

    Inherits all the functionality of pd.Series.
    """

    def __init__(self, data=None, index=None):
        """
        Initialize a new Prototype object.

        Parameters:
        - data (array-like, Iterable, dict, or scalar): The data to be stored in the prototype.
        - index (array-like or Index (1d)): The index labels associated with the data.
        """
        super().__init__(data=data, index=index)

    def set_marks(self, marks_list):
        """
        Set the marks of the prototype.

        Parameters:
        - marks_list (array-like, Iterable, dict, or scalar): The marks to be set.

        Returns:
        None
        """
        self[:] = pd.Series(data=marks_list, index=self.index)
