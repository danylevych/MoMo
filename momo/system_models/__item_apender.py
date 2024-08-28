from abc import ABC, abstractmethod
import pandas as pd



class _ItemAppender(ABC):
    def __init__(self, date_frame):
        self.data_frame = date_frame

    def add_item(self, item_name, item_values):
        self._check_item_name(item_name)
        self._check_item_values(item_name, item_values)
        return self.data_frame


    def _check_item_name(self, item_name):
        if not isinstance(item_name, str):
            raise ValueError("The item name must be a string.")


    def _check_item_values(self, item_name, item_values):
        if isinstance(item_values, list):
            self._add_list(item_name, item_values)
        elif isinstance(item_values, dict):
            self._add_dict(item_name, item_values)
        else:
            raise ValueError("The item values must be a list or a dictionary.")


    def _check_lenght_dict(self, left, right, what):
        if len(left) > len(right) and len(right):
            raise ValueError(f"The length of the item values must be less or equal to the number of {what}.")


    def _check_keys(self, keys, right):
        if not len(right):
            return

        for key in keys:
            if key not in right:
                raise ValueError("The key '{key}' not the right keys.")


    @abstractmethod
    def _add_list(self, item_name, item_values):
        pass


    @abstractmethod
    def _add_dict(self, item_name, item_values):
        pass



class _FeaturesAppender(_ItemAppender):
    def _add_list(self, item_name, item_values):
        if len(item_values) != len(self.data_frame.columns):
            raise ValueError("The length of the item values must be equal to the number of alternatives.")

        row = pd.DataFrame(data=[item_values], index=[item_name], columns=self.data_frame.columns)
        self.data_frame = pd.concat([self.data_frame, row], axis=0)


    def _add_dict(self, item_name, item_values):
        self._check_lenght_dict(list(item_values.keys()), self.data_frame.columns.to_list(), "alternatives")
        self._check_keys(item_values.keys(), self.data_frame.columns)

        if not self.data_frame.empty:
            item_values =  {key: item_values.get(key, 0) for key in self.data_frame.columns}

        row = pd.DataFrame(item_values, index=[item_name])
        self.data_frame = pd.concat([self.data_frame, row], axis=0)



class _AlternativesAppender(_ItemAppender):
    def _add_list(self, item_name, item_values):
        if len(item_values) != len(self.data_frame.index.to_list()):
            raise ValueError("The length of the item values must be equal to the number of features.")

        column = pd.Series(data=item_values, index=self.data_frame.index)
        self.data_frame[item_name] = column


    def _add_dict(self, item_name, item_values):
        self._check_lenght_dict(list(item_values.keys()), self.data_frame.index.to_list(), "features")
        self._check_keys(item_values.keys(), self.data_frame.index)

        if not self.data_frame.empty:
            item_values =  {key: item_values.get(key, 0) for key in self.data_frame.index}

        self.data_frame[item_name] = item_values
