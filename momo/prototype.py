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

    def set_marks(self, marks_list: dict | list):
        """
        Set the marks of the prototype.

        Parameters:
        - marks_list (array-like, Iterable, dict): The marks to be set.

        Returns:
        None
        """
        if isinstance(marks_list, dict):
            self._set_marks_dict(marks_list)
        elif isinstance(marks_list, list):
            self._set_marks_list(marks_list)
        else:
            raise ValueError("The marks_list parameter must be a dictionary or a list.")


    def _set_marks_dict(self, marks_dict: dict):
        """
        Set the marks of the prototype from a dictionary.

        Parameters:
        - marks_dict (dict): The marks to be set.

        Returns:
        None
        """
        for outer_key, inner_dict in marks_dict.items():
            for inner_key, value in inner_dict.items():
                self[(outer_key, inner_key)] = value


    def _set_marks_list(self, marks_list: list):
        """
        Set the marks of the prototype from a list.

        Parameters:
        - marks_list (list): The marks to be set.

        Returns:
        None
        """
        self[:] = marks_list
