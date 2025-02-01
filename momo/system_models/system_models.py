import pandas as pd
from itertools import product
from momo.prototype import Prototype
from momo.system_models.__item_apender import _FeaturesAppender, _AlternativesAppender


class SystemModel:
    """Represents a system model."""

    def __init__(self, name: str, data=None, features=None, alternatives=None):
        """
        Initializes a SystemModel instance.

        Args:
            name (str): The name of the system model.
            data (list or None): The data for the system model.
            features (list or None): The list of features for the system model.
            alternatives (list or None): The list of alternatives for the system model.
        """
        self._init_name(name)
        self._validate_as_list_string(features, "features")
        self._validate_as_list_string(alternatives, "alternatives")

        self._validate_meanshures_of_data_features_alternatives(data, features, alternatives)

        self.data = pd.DataFrame(data=data, index=features, columns=alternatives)
        self.__features_appender = _FeaturesAppender(self.data)
        self.__alternatives_appender = _AlternativesAppender(self.data)


    def _init_name(self, name):
        """
        Initializes the name attribute of the SystemModel instance.

        Args:
            name: The name of the system model.

        Raises:
            ValueError: If the name parameter is not a string.
        """
        if not isinstance(name, str):
            raise ValueError("The name parameter must be a string.")
        self.name = name


    def _validate_meanshures_of_data_features_alternatives(self, data, features, alternatives):
        """
        Validates the dimensions of the data, features, and alternatives.

        Args:
            data: The data for the system model.
            features: The list of features for the system model.
            alternatives: The list of alternatives for the system model.

        Raises:
            ValueError: If the dimensions of the data, features, and alternatives do not match.
        """
        if data is not None:
            if features is not None and len(data) != len(features):
                raise ValueError("The number of rows in data must match the length of features.")
            if alternatives is not None and len(data[0]) != len(alternatives):
                raise ValueError("The number of columns in data must match the length of alternatives.")


    def _validate_as_list_string(self, value, name):
        """
        Validates that a value is a list of strings.

        Args:
            value: The value to validate.
            name: The name of the value.

        Raises:
            ValueError: If the value is not a list of strings.
        """
        if value is not None and not all(isinstance(v, str) for v in value):
            raise ValueError(f"All elements of {name} must be strings.")


    def _validate_as(self, value, name, expected_type):
        """
        Validates that a value is of the expected type.

        Args:
            value: The value to validate.
            name: The name of the value.
            expected_type: The expected type of the value.

        Raises:
            ValueError: If the value is not of the expected type.
        """
        if not isinstance(value, expected_type):
            raise ValueError(f"The {name} parameter must be of type {expected_type.__name__}.")


    def _validate_length(self, value, name, expected_length):
        """
        Validates the length of a value.

        Args:
            value: The value to validate.
            name: The name of the value.
            expected_length: The expected length of the value.

        Raises:
            ValueError: If the value does not have the expected length.
        """
        if value is not None and len(value) != expected_length:
            raise ValueError(f"The {name} parameter must have a length of {expected_length}.")



    def add_feature(self, feature_name: str, alternatives: list | dict):
        """
        Adds a feature to the system model.

        Args:
            feature_name (str): The name of the feature.
            alternatives (list or dict): The list or dictionary of alternatives for the feature.
        """
        self.__features_appender.data_frame = self.data  # Refresh the pointed data.
        self.data = self.__features_appender.add_item(feature_name, alternatives)


    def add_alternative(self, alternative_name, features : list | dict):
        """
        Adds an alternative to the system model.

        Args:
            alternative_name: The name of the alternative.
            features (list or dict): The list or dictionary of features for the alternative.
        """
        self.__alternatives_appender.data_frame = self.data  # Refresh the pointed data.
        self.data = self.__alternatives_appender.add_item(alternative_name, features)


    def remove_feature(self, feature_name):
        """
        Removes a feature from the system model.

        Args:
            feature_name: The name of the feature to remove.

        Raises:
            ValueError: If the feature does not exist.
        """
        self._validate_as(feature_name, "feature_name", str)

        if feature_name not in self.data.index:
            raise ValueError(f"Feature '{feature_name}' does not exist.")

        self.data = self.data.drop(index=feature_name)


    def remove_alternative(self, alternative_name):
        """
        Removes an alternative from the system model.

        Args:
            alternative_name: The name of the alternative to remove.

        Raises:
            ValueError: If the alternative does not exist.
        """
        self._validate_as(alternative_name, "alternative_name", str)

        if alternative_name not in self.data.columns:
            raise ValueError(f"Alternative '{alternative_name}' does not exist.")

        self.data = self.data.drop(columns=alternative_name)



    def get_features(self):
        """
        Returns a tuple of the features in the system model.

        Returns:
            tuple: The features in the system model.
        """
        return tuple(self.data.index)

    @property
    def features(self):
        """
        Returns the features property of the system model's data.

        Returns:
            pandas.DataFrame.index: The features property of the system model's data.
        """
        return self.get_features()


    def get_alternatives(self):
        """
        Returns a tuple of the alternatives in the system model.

        Returns:
            tuple: The alternatives in the system model.
        """
        return tuple(self.data.columns)

    @property
    def alternatives(self):
        """
        Returns the alternatives property of the system model's data.

        Returns:
            pandas.DataFrame.columns: The alternatives property of the system model's data.
        """
        return self.get_alternatives()

    @property
    def loc(self):
        """
        Returns the loc property of the system model's data.

        Returns:
            pandas.DataFrame.loc: The loc property of the system model's data.
        """
        return self.data.loc


    def __getitem__(self, key):
        """
        Returns the value at the specified key in the system model's data.

        Args:
            key: The key to retrieve the value for.

        Returns:
            Any: The value at the specified key in the system model's data.
        """
        return self.data[key]


    def __setitem__(self, key, value):
        """
        Sets the value at the specified key in the system model's data.

        Args:
            key: The key to set the value for.
            value: The value to set.
        """
        self.data[key] = value


    def __str__(self):
        """
        Returns a string representation of the system model.

        Returns:
            str: A string representation of the system model.
        """
        return f'"{self.name}"\n{self.data}'



class MultiSystemModel:
    """Represents a multi-system model."""

    def __init__(self, system_models: list | tuple | set | None = None):
        """
        Initializes a MultiSystemModel instance.

        Args:
            system_models (list or tuple or set or None): The list, tuple, or set of system models.
        """
        self.systems = {}

        if isinstance(system_models, MultiSystemModel):
            self.systems = system_models.systems
        elif isinstance(system_models, list):
            self._constructor_from_list(system_models)
        elif isinstance(system_models, tuple):
            self._constructor_from_tuple(system_models)
        elif isinstance(system_models, set):
            self._constructor_from_set(system_models)
        elif system_models is None:
            pass # Do nothing
        else:
            raise ValueError("The system_models parameter must be a list, tuple or set.")


    def _constructor_from_list(self, system_models):
        """
        Constructs the MultiSystemModel instance from a list of system models.

        Args:
            system_models (list): The list of system models.

        Raises:
            ValueError: If any element in the list is not a SystemModel instance.
        """
        if all(isinstance(system, SystemModel) for system in system_models):
            for system in system_models:
                self.add_system(system)
        else:
            raise ValueError("All elements in the list must be SystemModel instances.")


    def _constructor_from_tuple(self, system_models):
        """
        Constructs the MultiSystemModel instance from a tuple of system models.

        Args:
            system_models (tuple): The tuple of system models.

        Raises:
            ValueError: If any element in the tuple is not a SystemModel instance.
        """
        if all(isinstance(system, SystemModel) for system in system_models):
            for system in system_models:
                self.add_system(system)
        else:
            raise ValueError("All elements in the tuple must be SystemModel instances.")


    def _constructor_from_set(self, system_models):
        """
        Constructs the MultiSystemModel instance from a set of system models.

        Args:
            system_models (set): The set of system models.

        Raises:
            ValueError: If any element in the set is not a SystemModel instance.
        """
        if all(isinstance(system, SystemModel) for system in system_models):
            for system in system_models:
                self.add_system(system)
        else:
            raise ValueError("All elements in the set must be SystemModel instances.")


    def add_system(self, system_model: SystemModel):
        """
        Adds a system model to the multi-system model.

        Args:
            system_model (SystemModel): The system model to add.

        Raises:
            ValueError: If the system_model parameter is not a SystemModel instance.
        """
        if not isinstance(system_model, SystemModel):
            raise ValueError("The system_model parameter must be a SystemModel instance.")

        self.systems[system_model.name] = system_model


    def add_systems(self, system_models: list | tuple | set):
        """
        Adds multiple system models to the multi-system model.

        Args:
            system_models (list or tuple or set): The list, tuple, or set of system models.

        Raises:
            ValueError: If the system_models parameter is not a list, tuple, or set.
        """
        if not isinstance(system_models, (list, tuple, set)):
            raise ValueError("The system_models parameter must be a list, tuple or set.")

        for system in system_models:
            self.add_system(system)


    def remove_system(self, system_name):
        """
        Removes a system model from the multi-system model.

        Args:
            system_name: The name of the system model to remove.

        Raises:
            ValueError: If the system model does not exist.
        """
        if self.__has_system(system_name):
            del self.systems[system_name]
        else:
            raise ValueError(f"System '{system_name}' does not exist.")


    def __has_system(self, system_name):
        """
        Checks if a system model exists in the multi-system model.

        Args:
            system_name: The name of the system model to check.

        Returns:
            bool: True if the system model exists, False otherwise.
        """
        return system_name in self.systems


    def get_system_names(self):
        """
        Returns a tuple of the names of the system models in the multi-system model.

        Returns:
            tuple: The names of the system models.
        """
        return tuple(self.systems.keys())


    def get_all_combinations(self):
        """
        Returns a DataFrame containing all combinations of alternatives from the system models.

        Returns:
            pandas.DataFrame: The DataFrame containing all combinations of alternatives.
        """
        system_names = list(self.systems.keys())
        system_data = [self.systems[name].data for name in system_names]

        related_features = self.get_features_related_to_system()
        alternatives_name = list(product(*[data.columns for data in system_data]))

        result_df = pd.DataFrame(index=related_features)

        # Fill the DataFrame with combinations
        for combination in alternatives_name:
            result_df[combination] = 0

            for system_name, system_df in zip(system_names, system_data):
                for feature in system_df.index:
                    if related_feature := self.__get_related_feature(feature, related_features):
                        value = system_df.loc[feature, combination[system_names.index(system_name)]]
                        result_df.at[related_feature, combination] = value

        return result_df


    def generate_combinations(self):
        """
        Generates all possible combinations of alternatives for the system models in the multi-system model.

        Yields:
            tuple: A tuple of alternatives for each system model.
        """
        system_names = list(self.systems.keys())
        system_data = [self.systems[name].data for name in system_names]
        related_features = self.get_features_related_to_system()

        for combination in product(*[data.columns for data in system_data]):
            new_column = pd.Series(0, index=related_features)

            for idx, (system_name, system_df) in enumerate(zip(system_names, system_data)):
                for feature in system_df.index:
                    if related_feature := self.__get_related_feature(feature, related_features):
                        value = system_df.loc[feature, combination[idx]]
                        new_column[related_feature] = value

            yield tuple(combination), new_column


    def __get_related_feature(self, feature, related_features):
        """
        Returns the related feature for a given feature.

        Args:
            feature: The feature to find the related feature for.
            related_features: The tuple of related features.

        Returns:
            str: The related feature.

        Raises:
            ValueError: If the feature is not related to any system.
        """
        for related_feature in related_features:
            if feature in related_feature:
                return related_feature

        raise ValueError(f"Feature {feature} is not related to any system.")


    def get_features_related_to_system(self):
        """
        Returns a tuple of features related to each system in the multi-system model.

        Returns:
            tuple: The features related to each system.
        """
        systems = self.get_system_names()
        features = [self.systems[name].data.index for name in systems]

        related_features = []

        for system, feature_list in zip(systems, features):
            for feature in feature_list:
                    related_features.append((system, feature))

        return tuple(related_features)


    def get_all_features(self):
        """
        Returns a tuple of all features in the multi-system model.

        Returns:
            tuple: All features in the multi-system model.
        """
        all_features = list()
        for system_data in self.systems.values():
            all_features.extend(system_data.data.index.to_list())
        return tuple(all_features)


    def get_prototype(self):
        """
        Returns a Prototype instance based on the multi-system model.

        Returns:
            Prototype: The Prototype instance.
        """
        if not self.systems:
            return Prototype()

        related_features = self.get_features_related_to_system()
        prototype = Prototype(data=[0 for _ in related_features], index=related_features)
        return prototype
    #
    # =====================================================================

    def __str__(self):
        """
        Returns a string representation of the multi-system model.

        Returns:
            str: A string representation of the multi-system model.
        """
        return self.get_all_combinations().__str__()
