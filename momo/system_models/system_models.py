import pandas as pd
from itertools import product
from momo.prototype import Prototype
from momo.system_models.__item_apender import _FeaturesAppender, _AlternativesAppender


class SystemModel:
    #
    # =================================================================================
    # Constructors

    def __init__(self, name: str, data=None, features=None, alternatives=None):
        self._init_name(name)
        self._validate_as_list_string(features, "features")
        self._validate_as_list_string(alternatives, "alternatives")

        self._validate_meanshures_of_data_features_alternatives(data, features, alternatives)

        self.data = pd.DataFrame(data=data, index=features, columns=alternatives)
        self.__features_appender = _FeaturesAppender(self.data)
        self.__alternatives_appender = _AlternativesAppender(self.data)


    def _init_name(self, name):
        if not isinstance(name, str):
            raise ValueError("The name parameter must be a string.")
        self.name = name
    #
    # =================================================================================

    # =================================================================================
    # Validating methods

    def _validate_meanshures_of_data_features_alternatives(self, data, features, alternatives):
        if data is not None:
            if features is not None and len(data) != len(features):
                raise ValueError("The number of rows in data must match the length of features.")
            if alternatives is not None and len(data[0]) != len(alternatives):
                raise ValueError("The number of columns in data must match the length of alternatives.")


    def _validate_as_list_string(self, value, name):
        if value is not None and not all(isinstance(v, str) for v in value):
            raise ValueError(f"All elements of {name} must be strings.")


    def _validate_as(self, value, name, expected_type):
        if not isinstance(value, expected_type):
            raise ValueError(f"The {name} parameter must be of type {expected_type.__name__}.")


    def _validate_length(self, value, name, expected_length):
        if value is not None and len(value) != expected_length:
            raise ValueError(f"The {name} parameter must have a length of {expected_length}.")
    #
    # =================================================================================

    # =================================================================================
    # Add Methods
    def add_feature(self, feature_name: str, alternatives: list | dict):
        self.__features_appender.data_frame = self.data  # Refresh the pointed data.
        self.data = self.__features_appender.add_item(feature_name, alternatives)

    def add_alternative(self, alternative_name, features : list | dict):
        self.__alternatives_appender.data_frame = self.data  # Refresh the pointed data.
        self.data = self.__alternatives_appender.add_item(alternative_name, features)
    #
    # =================================================================================

    # =================================================================================
    # Remove Methods
    def remove_feature(self, feature_name):
        self._validate_as(feature_name, "feature_name", str)

        if feature_name not in self.data.index:
            raise ValueError(f"Feature '{feature_name}' does not exist.")

        self.data = self.data.drop(index=feature_name)


    def remove_alternative(self, alternative_name):
        self._validate_as(alternative_name, "alternative_name", str)

        if alternative_name not in self.data.columns:
            raise ValueError(f"Alternative '{alternative_name}' does not exist.")

        self.data = self.data.drop(columns=alternative_name)
    #
    # =================================================================================

    def get_features(self):
        return tuple(self.data.index)


    def get_alternatives(self):
        return tuple(self.data.columns)


    @property
    def loc(self):
        return self.data.loc


    def __getitem__(self, key):
        return self.data[key]


    def __setitem__(self, key, value):
        self.add_alternative(key, value)


    def __str__(self):
        return f'"{self.name}"\n{self.data}'



class MultiSystemModel:
    #
    # =====================================================================
    # Constructors

    def __init__(self, system_models: list | tuple | set | None = None):
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
        if all(isinstance(system, SystemModel) for system in system_models):
            for system in system_models:
                self.add_system(system)
        else:
            raise ValueError("All elements in the list must be SystemModel instances.")


    def _constructor_from_tuple(self, system_models):
        if all(isinstance(system, SystemModel) for system in system_models):
            for system in system_models:
                self.add_system(system)
        else:
            raise ValueError("All elements in the tuple must be SystemModel instances.")


    def _constructor_from_set(self, system_models):
        if all(isinstance(system, SystemModel) for system in system_models):
            for system in system_models:
                self.add_system(system)
        else:
            raise ValueError("All elements in the set must be SystemModel instances.")
    #
    # =====================================================================

    # =====================================================================
    # Add Methods

    def add_system(self, system_model: SystemModel):
        if not isinstance(system_model, SystemModel):
            raise ValueError("The system_model parameter must be a SystemModel instance.")

        self.systems[system_model.name] = system_model


    def add_systems(self, system_models: list | tuple | set):
        if not isinstance(system_models, (list, tuple, set)):
            raise ValueError("The system_models parameter must be a list, tuple or set.")

        for system in system_models:
            self.add_system(system)
    #
    # =====================================================================

    # =====================================================================
    # Remove Methods

    def remove_system(self, system_name):
        if self.__has_system(system_name):
            del self.systems[system_name]
        else:
            raise ValueError(f"System '{system_name}' does not exist.")


    def __has_system(self, system_name):
        return system_name in self.systems
    #
    # =====================================================================

    # =====================================================================
    # Getters

    def get_system_names(self):
        return tuple(self.systems.keys())


    def get_all_combinations(self):
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


    def __get_related_feature(self, feature, related_features):
        for related_feature in related_features:
            if feature in related_feature:
                return related_feature

        raise ValueError(f"Feature {feature} is not related to any system.")


    def get_features_related_to_system(self):
        systems = self.get_system_names()
        features = [self.systems[name].data.index for name in systems]

        related_features = []

        for system, feature_list in zip(systems, features):
            for feature in feature_list:
                    related_features.append((system, feature))

        return tuple(related_features)


    def get_all_features(self):
        all_features = list()
        for system_data in self.systems.values():
            all_features.extend(system_data.data.index.to_list())
        return tuple(all_features)


    def get_prototype(self):
        if not self.systems:
            return Prototype()

        related_features = self.get_features_related_to_system()
        prototype = Prototype(data=[0 for _ in related_features], index=related_features)
        return prototype
    #
    # =====================================================================
