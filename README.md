# Guide

- [Installation](#installation)
- [Modules](#modules)
    - [model](#model)
    - [prototype](#prototype)
    - [system_models](#system_models)
- [Author](#author)


## Installation

To install the package, run the following command:

```bash
pip install momo-morphological-modeling
```

## Modules

The package contains the following modules:

- `model`: Contains the main classes for the morphological modeling `MoMoModel`.
- `prototype`: Contains the classes for the prototype of morphological modeling `Prototype`.
- `system_models`: Contains the classes for the system models `SystemModel` and `MultySystemModel`.

---

### model

The `model` module contains the main classes for the morphological modeling. The main class is `MoMoModel` which is used to create a morphological model and to perform the morphological analysis.

### MoMoModel

The `MoMoModel` class represents a **Multi-Object Multi-System Model** designed to manage multiple system models and a prototype for similarity calculations. It integrates the `Prototype` and `MultiSystemModel` classes, enabling users to perform operations on system models and calculate similarity measures between them.

#### Key Features
- Supports initialization with multiple system models and an optional prototype.
- Automatically generates a prototype based on the system models if not provided.
- Allows for similarity measure calculations between the prototype and combinations of system models.
- Built-in integration with `Prototype` and `MultiSystemModel`.

---

##### Initialization Parameters

| Parameter       | Type                           | Description                                                                                  |
|-----------------|--------------------------------|----------------------------------------------------------------------------------------------|
| `system_models` | `MultiSystemModel`, `list`, `tuple`, `set` | The system models used in the `MoMoModel`.                                                  |
| `prototype`     | `Prototype`, `None` (optional) | The prototype object to compare with system models. Defaults to `None`.                     |

---

##### Methods Overview

| Method                                | Description                                                                                  |
|---------------------------------------|----------------------------------------------------------------------------------------------|
| `get_prototype()`                     | Returns the current prototype.                                                              |
| `set_prototype(prototype)`            | Sets a new prototype.                                                                       |
| `prototype_` (property)                | Gets or sets the prototype.                                                                 |
| `get_system_models()`                 | Returns the current system models.                                                          |
| `set_system_models(system_models)`    | Sets new system models and updates the prototype accordingly.                                |
| `system_models_` (property)            | Gets or sets the system models.                                                             |
| `get_similarity_measures()`           | Calculates similarity measures between the prototype and all combinations of system models.  |
| `__str__()`                           | Returns a string representation of the `MoMoModel` object, including the prototype and system models. |

---

##### Example Usage

```python
from momo.model import MoMoModel
from momo.system_models.system_models import MultiSystemModel, SystemModel


# Create individual system models
dbms = SystemModel(
    name="DBMS",
    data=[
        [1, 0, 1],  # Security
        [1, 1, 0],  # Performance
        [0, 1, 1],  # Speed
    ],
    features=["Security", "Performance", "Speed"],
    alternatives=["MySQL", "PostgreSQL", "MongoDB"]
)

connector = SystemModel(
    name="Connector",
    data=[
        [1, 0],  # Flexibility
        [1, 1],  # Cost
    ],
    features=["Flexibility", "Cost"],
    alternatives=["Copper", "Aluminum"]
)

# Initialize a MultiSystemModel
multi_system = MultiSystemModel([dbms, connector])

# Initialize a MoMoModel
momo_model = MoMoModel(system_models=multi_system)

# Access the prototype
print("Prototype:")
print(momo_model.prototype)

# Calculate similarity measures
similarity_measures = momo_model.get_similarity_measures()
print("\nSimilarity Measures:")
for combination, measure in similarity_measures.items():
    print(f"{combination}: {measure}")

# String representation
print("\nMoMoModel:")
print(momo_model)
```

**Output:**
```
Prototype:
DBMS       Security       0
           Performance    0
           Speed          0
Connector  Flexibility    0
           Cost           0
dtype: int64

Similarity Measures:
('MySQL', 'Copper'): 0.5
('MySQL', 'Aluminum'): 1.3333333333333333
('PostgreSQL', 'Copper'): 0.5
('PostgreSQL', 'Aluminum'): 1.3333333333333333
('MongoDB', 'Copper'): 0.5
('MongoDB', 'Aluminum'): 1.3333333333333333

MoMoModel:
Prototype:
DBMS       Security       0
           Performance    0
           Speed          0
Connector  Flexibility    0
           Cost           0
dtype: int64

System Models:
                       (MySQL, Copper)  (MySQL, Aluminum)  (PostgreSQL, Copper)  (PostgreSQL, Aluminum)  (MongoDB, Copper)  (MongoDB, Aluminum)
DBMS      Security                   1                  1                     0                       0                  1                    1
          Performance                1                  1                     1                       1                  0                    0
          Speed                      0                  0                     1                       1                  1                    1
Connector Flexibility                1                  0                     1                       0                  1                    0
          Cost                       1                  1                     1                       1                  1                    1
```







---

### prototype

The `prototype` module contains the `Prototype` class, which is a subclass of `pandas.Series`. It is designed to store and manipulate hierarchical data using features and alternatives.

### Prototype

The `Prototype` class extends the functionality of `pandas.Series` by allowing hierarchical data representation with support for setting values via dictionaries or lists. **And its represnt the prototype of the morphological model.**

##### Key Features
- Directly inherits all functionality from `pandas.Series`.
- Supports setting values using hierarchical dictionaries or lists.
- Maintains compatibility with standard pandas operations.

---

##### Initialization Parameters

| Parameter      | Type                       | Description                                                                 |
|----------------|----------------------------|-----------------------------------------------------------------------------|
| `data`         | `array-like`, `Iterable`, `dict`, `scalar` | The data to be stored in the `Prototype`.                                  |
| `index`        | `array-like` or `Index`    | The index labels for the data.                                             |

---

##### Methods Overview

| Method                            | Description                                                                                  |
|-----------------------------------|----------------------------------------------------------------------------------------------|
| `set_marks(marks_list)`           | Sets values in the `Prototype` using a dictionary or list.                                   |
| `_set_marks_dict(marks_dict)`     | Sets values in the `Prototype` from a dictionary of hierarchical data.                       |
| `_set_marks_list(marks_list)`     | Sets values in the `Prototype` from a list.                                                  |

---

##### Example Usage

```python
from momo.prototype import Prototype


# Initialize a prototype with hierarchical data
data = [0, 0, 0, 1]
index = [("System1", "Feature1"), ("System1", "Feature2"), ("System2", "Feature3"), ("System2", "Feature4")]

prototype = Prototype(data=data, index=index)

print("Initial Prototype:")
print(prototype)

# Set marks using a dictionary
prototype.set_marks({
    "System1": {"Feature1": 1, "Feature2": 2},
    "System2": {"Feature3": 3, "Feature4": 4}
})

print("\nPrototype after setting marks (dict):")
print(prototype)

# Set marks using a list
prototype.set_marks([10, 20, 30, 40])

print("\nPrototype after setting marks (list):")
print(prototype)
```

**Output:**
```
Initial Prototype:
(System1, Feature1)    0
(System1, Feature2)    0
(System2, Feature3)    0
(System2, Feature4)    1
dtype: int64

Prototype after setting marks (dict):
(System1, Feature1)    1
(System1, Feature2)    2
(System2, Feature3)    3
(System2, Feature4)    4
dtype: int64

Prototype after setting marks (list):
(System1, Feature1)    10
(System1, Feature2)    20
(System2, Feature3)    30
(System2, Feature4)    40
dtype: int64
```


---

### system_models

The `system_models` module contains the classes for the system models. The main classes are `SystemModel` and `MultySystemModel` which are used to create the system models.

#### `SystemModel`

The `SystemModel` class is a core component designed to represent and manipulate system models. It allows you to manage a structured representation of features and alternatives, supporting data storage, validation, and various manipulations.

##### Key Features
- Manage relationships between features and alternatives.
- Add, remove, and retrieve features and alternatives.
- Validate the consistency of data, features, and alternatives.
- Built-in support for `pandas.DataFrame` for structured data handling.

---

##### Initialization Parameters

| Parameter      | Type         | Description                                                                                       |
|----------------|--------------|---------------------------------------------------------------------------------------------------|
| `name`         | `str`        | The name of the system model.       |
| `data`         | `list`, `None` | The data matrix (rows: features, columns: alternatives) to initialize the system model. |
| `features`     | `list`, `None` | The list of feature names.  |
| `alternatives` | `list`, `None` | The list of alternative names.|

---

##### Methods Overview

| Method                     | Description                                                                                  |
|----------------------------|----------------------------------------------------------------------------------------------|
| `add_feature(feature_name, alternatives)` | Adds a new feature to the system model with its alternatives.          |
| `add_alternative(alternative_name, features)` | Adds a new alternative to the system model with its features. |
| `remove_feature(feature_name)` | Removes a feature from the system model.                                     |
| `remove_alternative(alternative_name)` | Removes an alternative from the system model.                        |
| `get_features()`           | Returns a tuple of all features in the system model.                                           |
| `get_alternatives()`       | Returns a tuple of all alternatives in the system model.                                       |
| `features` (property)      | Returns the list of feature names as a pandas DataFrame index.                                 |
| `alternatives` (property)  | Returns the list of alternative names as a pandas DataFrame column index.                      |
| `loc` (property)           | Provides access to pandas DataFrame `.loc` for advanced slicing and indexing.                 |
| `__getitem__(key)`         | Retrieves a value from the underlying data using a key (row/column-based indexing).            |
| `__setitem__(key, value)`  | Sets a value in the underlying data using a key.                                               |
| `__str__()`                | Returns a string representation of the system model, including its name and the data matrix.   |

---

##### Example Usage

```python
from momo.system_models.system_models import SystemModel

# Initialize a system model
model = SystemModel(
    name="DBMS",
    data=[
        [1, 0, 1],  # Security
        [1, 1, 0],  # Performance
        [0, 1, 1],  # Speed
    ],
    features=["Security", "Performance", "Speed"],
    alternatives=["MySQL", "PostgreSQL", "MongoDB"]
)

# Add a new feature
model.add_feature("Reliability", [1, 1, 1])

# Add a new alternative
model.add_alternative("SQLite", {"Security": 1, "Performance": 0, "Speed": 1, "Reliability": 1})

# Access features and alternatives
print("Features:", model.get_features())
print("Alternatives:", model.get_alternatives())
print()

# Remove a feature
model.remove_feature("Speed")

# String representation of the model
print(model)
```

**Output:**
```
Features: ('Security', 'Performance', 'Speed', 'Reliability')
Alternatives: ('MySQL', 'PostgreSQL', 'MongoDB', 'SQLite')

"DBMS"
             MySQL  PostgreSQL  MongoDB  SQLite
Security         1           0        1       1
Performance      1           1        0       0
Reliability      1           1        1       1
```

---

#### `MultiSystemModel`

The `MultiSystemModel` class is designed to represent and manipulate multiple system models. It supports operations like adding, removing, and combining data from multiple `SystemModel` instances into a unified structure.

##### Key Features
- Combine multiple system models into a unified structure.
- Add, remove, and retrieve system models by name.
- Generate combinations of alternatives across all systems.
- Retrieve features and alternatives for all systems collectively.
- Built-in support for `pandas.DataFrame` for data representation.

---

##### Initialization Parameters

| Parameter          | Type                   | Description                                                                 |
|--------------------|------------------------|-----------------------------------------------------------------------------|
| `system_models`    | `list`, `tuple`, `set`, `None` | The list, tuple, or set of `SystemModel` instances to initialize the multi-system model. |

---

##### Methods Overview

| Method                               | Description                                                                                  |
|--------------------------------------|----------------------------------------------------------------------------------------------|
| `add_system(system_model)`           | Adds a new system model to the multi-system model.                                           |
| `add_systems(system_models)`         | Adds multiple system models to the multi-system model.                                       |
| `remove_system(system_name)`         | Removes a system model by name.                                                             |
| `get_system_names()`                 | Returns a tuple of all system model names in the multi-system model.                        |
| `get_all_combinations()`             | Generates all combinations of alternatives across all system models and returns a DataFrame. |
| `get_features_related_to_system()`   | Returns a tuple of features associated with each system in the multi-system model.           |
| `get_all_features()`                 | Returns a tuple of all features across all systems in the multi-system model.                |
| `get_prototype()`                    | Creates and returns a `Prototype` instance based on the features of all system models.       |
| `__str__()`                          | Returns a string representation of the multi-system model.                                   |

---

##### Example Usage

```python
from momo.system_models.system_models import SystemModel, MultiSystemModel

# Create individual system models
dbms = SystemModel(
    name="DBMS",
    data=[
        [1, 0, 1],  # Security
        [1, 1, 0],  # Performance
        [0, 1, 1],  # Speed
    ],
    features=["Security", "Performance", "Speed"],
    alternatives=["MySQL", "PostgreSQL", "MongoDB"]
)

connector = SystemModel(
    name="Connector",
    data=[
        [1, 0],  # Flexibility
        [1, 1],  # Cost
    ],
    features=["Flexibility", "Cost"],
    alternatives=["Copper", "Aluminum"]
)

# Initialize a multi-system model
multi_system = MultiSystemModel([dbms, connector])

# Add a new system model
multi_system.add_system(
    SystemModel(
        name="Cache",
        data=[
            [1, 1],  # Caching Speed
            [0, 1],  # Cost Efficiency
        ],
        features=["Caching Speed", "Cost Efficiency"],
        alternatives=["Redis", "Memcached"]
    )
)

# Retrieve system names
print("System Names:", multi_system.get_system_names())

# Retrieve all combinations of alternatives across all systems
combinations = multi_system.get_all_combinations()
print("\nAll Combinations of Alternatives:")
print(combinations)

# Retrieve features related to each system
related_features = multi_system.get_features_related_to_system()
print("\nRelated Features:")
print(related_features)

# Get the prototype based on the multi-system model
prototype = multi_system.get_prototype()
print("\nPrototype:")
print(prototype)
```


**Output:**
```
System Names: ('DBMS', 'Connector', 'Cache')

All Combinations of Alternatives:
                           (MySQL, Copper, Redis)  (MySQL, Copper, Memcached)  (MySQL, Aluminum, Redis)  ...  (MongoDB, Copper, Memcached)  (MongoDB, Aluminum, Redis)  (MongoDB, Aluminum, Memcached)
DBMS      Security                              1                           1                         1  ...                             1                           1                               1
          Performance                           1                           1                         1  ...                             0                           0                               0
          Speed                                 0                           0                         0  ...                             1                           1                               1
Connector Flexibility                           1                           1                         0  ...                             1                           0                               0
          Cost                                  1                           1                         1  ...                             1                           1                               1
Cache     Caching Speed                         1                           1                         1  ...                             1                           1                               1
          Cost Efficiency                       0                           1                         0  ...                             1                           0                               1

[7 rows x 12 columns]

Related Features:
(('DBMS', 'Security'), ('DBMS', 'Performance'), ('DBMS', 'Speed'), ('Connector', 'Flexibility'), ('Connector', 'Cost'), ('Cache', 'Caching Speed'), ('Cache', 'Cost Efficiency'))

Prototype:
DBMS       Security           0
           Performance        0
           Speed              0
Connector  Flexibility        0
           Cost               0
Cache      Caching Speed      0
           Cost Efficiency    0
dtype: int64
```


---
