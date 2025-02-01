from .prototype import Prototype
from .system_models.system_models import MultiSystemModel


class MoMoModel:
    """
    Represents a MoMo (Multi-Object Multi-System) model.

    Args:
        system_models (MultiSystemModel | list | tuple | set): The system models used in the MoMo model.
        prototype (Prototype | None, optional): The prototype object. Defaults to None.
    """

    def __init__(
        self,
        system_models: MultiSystemModel | list | tuple | set,
        prototype: Prototype | None = None,
    ):
        """
        Initializes a MoMoModel instance.

        Args:
            system_models (MultiSystemModel | list | tuple | set): The system models used in the MoMo model.
            prototype (Prototype | None, optional): The prototype object. Defaults to None.
        """
        self._u = 0
        self.system_models = MultiSystemModel(system_models)
        self._init_prototype(prototype)

    def _init_prototype(self, value):
        """
        Initializes the prototype object.

        Args:
            value (Prototype | None): The prototype object or None.

        Raises:
            ValueError: If the prototype is not a Prototype or None instance.
            ValueError: If the prototype does not have the same index as the system models.
        """
        if value is None:
            self.prototype = self.system_models.get_prototype()
        elif isinstance(value, Prototype):
            if value.index.equals(self.system_models.get_prototype().index):
                self.prototype = value
            else:
                raise ValueError("The prototype must have the same index as the system models.")
        else:
            raise ValueError("The prototype must be a Prototype or None instance.")

    def get_prototype(self):
        """
        Returns the prototype object.

        Returns:
            Prototype: The prototype object.
        """
        return self.prototype

    def set_prototype(self, prototype):
        """
        Sets the prototype object.

        Args:
            prototype (Prototype): The prototype object.
        """
        self._init_prototype(prototype)

    @property
    def prototype_(self):
        """
        Prototype: The prototype object.
        """
        return self.get_prototype()

    @prototype_.setter
    def prototype_(self, prototype):
        self.set_prototype(prototype)

    def get_system_models(self):
        """
        Returns the system models.

        Returns:
            MultiSystemModel: The system models.
        """
        return self.system_models

    def set_system_models(self, system_models):
        """
        Sets the system models.

        Args:
            system_models (MultiSystemModel | list | tuple | set): The system models.
        """
        self.system_models = MultiSystemModel(system_models)
        self.prototype = self.system_models.get_prototype()

    @property
    def system_models_(self):
        """
        MultiSystemModel: The system models.
        """
        return self.get_system_models()

    @system_models_.setter
    def system_models_(self, system_models):
        self.set_system_models(system_models)

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, value: str|int|float):
        if isinstance(value, str):
            value = value.lower()
            if value == "sorensen_dice":
                self._u = 0
            elif value == "dice":
                self._u = 1
            else:
                raise ValueError("The value must be 'jaccard' or 'dice'.")

        elif isinstance(value, (int, float)):
            if 0 <= value <= 1:
                self._u = value
            else:
                raise ValueError("The value must be between 0 and 1.")

    def __calculate_similarity_measures(self, prototype, compared_system):
        """
        Calculates the similarity measures between the prototype and a compared system.

        Args:
            prototype (Prototype): The prototype object.
            compared_system (Series): The compared system.

        Returns:
            float: The similarity measure.
        """
        intersection_num = (prototype & compared_system).sum()
        card_prototype = prototype.sum()
        card_compared_system = compared_system.sum()
        u = self._u

        return 2 * intersection_num / ((1 + u) * (card_prototype + card_compared_system) - 2 * u * intersection_num)

    def get_similarity_measures(self):
        """
        Calculates the similarity measures between the prototype and all combinations of system models.

        Returns:
            dict: A dictionary containing the similarity measures for each combination.
        """
        similarity_measures = {}

        for combination, new_column in self.system_models.generate_combinations():
            similarity_measures[combination] = self.__calculate_similarity_measures(
                self.prototype, new_column
            )

        return similarity_measures


    def __str__(self):
        """
        Returns a string representation of the MoMoModel object.

        Returns:
            str: A string representation of the MoMoModel object.
        """
        output = f"Prototype:\n{self.prototype}\n\n"
        output += f"System Models:\n{self.system_models}"

        return output
