from abc import ABC, abstractmethod
import pandas as pd


class _ItemAppender(ABC):
    """
    Abstract base class for appending items to a data frame.
    """

    def __init__(self, data_frame):
        """
        Initializes the _ItemAppender object.

        Args:
            data_frame (pandas.DataFrame): The data frame to append items to.
        """
        self.data_frame = data_frame

    def add_item(self, item_name, item_values):
        """
        Adds an item to the data frame.

        Args:
            item_name (str): The name of the item.
            item_values (list or dict): The values of the item.

        Returns:
            pandas.DataFrame: The updated data frame.
        """
        self._check_item_name(item_name)
        self._check_item_values(item_name, item_values)
        return self.data_frame

    def _check_item_name(self, item_name):
        """
        Checks if the item name is a string.

        Args:
            item_name (str): The name of the item.

        Raises:
            ValueError: If the item name is not a string.
        """
        if not isinstance(item_name, str):
            raise ValueError("The item name must be a string.")

    def _check_item_values(self, item_name, item_values):
        """
        Checks if the item values are a list or a dictionary.

        Args:
            item_name (str): The name of the item.
            item_values (list or dict): The values of the item.

        Raises:
            ValueError: If the item values are not a list or a dictionary.
        """
        if isinstance(item_values, list):
            self._add_list(item_name, item_values)
        elif isinstance(item_values, dict):
            self._add_dict(item_name, item_values)
        else:
            raise ValueError("The item values must be a list or a dictionary.")

    def _check_length_dict(self, left, right, what):
        """
        Checks if the length of the item values is less than or equal to the number of alternatives or features.

        Args:
            left (list): The left side of the comparison.
            right (list): The right side of the comparison.
            what (str): The type of values being compared (alternatives or features).

        Raises:
            ValueError: If the length of the item values is greater than the number of alternatives or features.
        """
        if len(left) > len(right) and len(right):
            raise ValueError(f"The length of the item values must be less or equal to the number of {what}.")

    def _check_keys(self, keys, right):
        """
        Checks if the keys in the item values are valid.

        Args:
            keys (list): The keys in the item values.
            right (list): The valid keys.

        Raises:
            ValueError: If any key in the item values is not a valid key.
        """
        if not len(right):
            return

        for key in keys:
            if key not in right:
                raise ValueError(f"The key '{key}' is not a valid key.")

    @abstractmethod
    def _add_list(self, item_name, item_values):
        """
        Abstract method for adding item values as a list.

        Args:
            item_name (str): The name of the item.
            item_values (list): The values of the item.
        """
        pass

    @abstractmethod
    def _add_dict(self, item_name, item_values):
        """
        Abstract method for adding item values as a dictionary.

        Args:
            item_name (str): The name of the item.
            item_values (dict): The values of the item.
        """
        pass


class _FeaturesAppender(_ItemAppender):
    """
    Class for appending features to a data frame.
    """

    def _add_list(self, item_name, item_values):
        """
        Adds feature values as a list to the data frame.

        Args:
            item_name (str): The name of the feature.
            item_values (list): The values of the feature.

        Raises:
            ValueError: If the length of the item values is not equal to the number of alternatives.
        """
        if len(item_values) != len(self.data_frame.columns):
            raise ValueError("The length of the item values must be equal to the number of alternatives.")

        row = pd.DataFrame(data=[item_values], index=[item_name], columns=self.data_frame.columns)
        self.data_frame = pd.concat([self.data_frame, row], axis=0)

    def _add_dict(self, item_name, item_values):
        """
        Adds feature values as a dictionary to the data frame.

        Args:
            item_name (str): The name of the feature.
            item_values (dict): The values of the feature.

        Raises:
            ValueError: If the length of the item values is not less than or equal to the number of alternatives.
            ValueError: If any key in the item values is not a valid key.
        """
        self._check_length_dict(list(item_values.keys()), self.data_frame.columns.to_list(), "alternatives")
        self._check_keys(item_values.keys(), self.data_frame.columns)

        if not self.data_frame.empty:
            item_values = {key: item_values.get(key, 0) for key in self.data_frame.columns}

        row = pd.DataFrame(item_values, index=[item_name])
        self.data_frame = pd.concat([self.data_frame, row], axis=0)


class _AlternativesAppender(_ItemAppender):
    """
    Class for appending alternatives to a data frame.
    """

    def _add_list(self, item_name, item_values):
        """
        Adds alternative values as a list to the data frame.

        Args:
            item_name (str): The name of the alternative.
            item_values (list): The values of the alternative.

        Raises:
            ValueError: If the length of the item values is not equal to the number of features.
        """
        if len(item_values) != len(self.data_frame.index.to_list()):
            raise ValueError("The length of the item values must be equal to the number of features.")

        column = pd.Series(data=item_values, index=self.data_frame.index)
        self.data_frame[item_name] = column

    def _add_dict(self, item_name, item_values):
        """
        Adds alternative values as a dictionary to the data frame.

        Args:
            item_name (str): The name of the alternative.
            item_values (dict): The values of the alternative.

        Raises:
            ValueError: If the length of the item values is not less than or equal to the number of features.
            ValueError: If any key in the item values is not a valid key.
        """
        self._check_length_dict(list(item_values.keys()), self.data_frame.index.to_list(), "features")
        self._check_keys(item_values.keys(), self.data_frame.index)

        if not self.data_frame.empty:
            item_values = {key: item_values.get(key, 0) for key in self.data_frame.index}

        self.data_frame[item_name] = item_values
