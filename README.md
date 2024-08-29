<p align="center">
  <a href="" rel="noopener">
 <img width=400px src="assets/img/title.png" alt="Project logo"></a>
</p>

<h1 align="center">AnaHiePro</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/danylevych/AnaHiePro/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/danylevych/AnaHiePro/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p>
<b>AnaHiePro</b> is a module that allows solving various tasks of systems analysis using the Analytic Hierarchy Process (AHP).
    <br>
</p>

## 📝 Content

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Authors](#authors)


## 🧐 About <a name = "about"></a>

<b>AnaHiePro</b>  is a Python module designed to simplify the decision-making process by using the Analytic Hierarchy Process (AHP) method. This method allows you to structure complex problems in the form of a hierarchical model consisting of goals, criteria, and alternatives. AnaHiePro automatically calculates global priorities for the entire hierarchy.

The module provides a recursive traversal of the hierarchical tree, starting from the leaf nodes and moving up to the root. Each level of the hierarchy is processed by multiplying the matrix of local child vectors by the global parent vector, which allows you to determine the weight of each element at all levels. This makes AnaHiePro an ideal tool for analyzing complex systems and making informed decisions in a variety of fields, including business, project management, scientific research, and more.

## 🏁 Getting Started <a name="getting_started"></a>

<h4>These are simple instructions on how to install <b>AnaHiePro</b> on your PC and start using it.</h4>

### Installing

Open the terminal window (Linux and macOS) or command line (Windows). Then use the `pip` command to install the module:

```sh
pip install anahiepro
```

### Prerequisites

Before installing AnaHiePro, ensure you have Python 3.x and `pip` installed on your system. You can download the latest version of Python from [python.org](https://www.python.org/).

After loading you can use all AnaHiePro's functionality, down below you can see the simplest way of using AnaHiePro.

```py
from anahiepro.nodes import Problem, Criteria, Alternative
from anahiepro.models.model import Model

problem = Problem("Example Problem")

list_of_criterias = [
    Criteria("Citeria_1"),
    Criteria("Citeria_2"),
    Criteria("Citeria_3")
]

alternatives = [
    Alternative("Alternative_1"),
    Alternative("Alternative_2")
]

model = Model(problem, list_of_criterias, alternatives)

print(model.show())
```


## 🎈 Usage <a name="usage"></a>

- [Pairwise comparison matrix](#pairwise_matrix)
- [Nodes](#nodes)
- [Models](#models)
- [Tools](#tools)


### Pairwise matrix <a name="pairwise_matrix"></a>

`PairwiseComparisonMatrix` represents the pairwise comparison matrix. A pairwise comparison matrix is a tool used in decision-making processes. It helps compare different options or criteria by evaluating them in pairs. Each element of the matrix represents the comparison result between two options or criteria.

#### Methods


| Method Name       | Description                                       |
|-------------------|---------------------------------------------------|
| `__init__(self, size, matrix)` | Initialize a pairwise comparison matrix with the given size or given matrix. |
| `set_comparison(self, i, j, value)` | Set the comparison value for the given indices. Might raise the `ValueError` exception when you try to set diagonal values to value, that not equal `1`. |
| `set_matrix(self, matrix)` | Set the entire matrix, ensuring it is a valid pairwise comparison matrix. Might raise the `ValueError` if the matrix is not consistent or not valid.|
| `get_matrix(self)` | Returns the current pairwise comparison matrix. |
| `calculate_priority_vector(self)` | Calculate the priority vector from the pairwise comparison matrix. |
| `calculate_consistency_ratio(self)` | Calculate the consistency ratio of the pairwise comparison matrix. |
| `__getitem__(self, key)` | Returns the value at the specified index in the matrix. |
| `__setitem__(self, key, value)` | Set the value at the specified index in the matrix. |

#### Example

```py
from anahiepro.pairwise import PairwiseComparisonMatrix


matrix = [
    [1,   2,   3],
    [1/2, 1,   2],
    [1/3, 1/2, 1]
]

pairwise_matrix = PairwiseComparisonMatrix(matrix=matrix)

print(pairwise_matrix.get_matrix())
print("Consistency ratio:", pairwise_matrix.calculate_consistency_ratio())
print("Priority vector:", pairwise_matrix.calculate_priority_vector())
```

Output:
```
[[1.         2.         3.        ]
 [0.5        1.         2.        ]
 [0.33333333 0.5        1.        ]]
Consistency ratio: 0.007933373029552656
Priority vector: [0.84679693 0.46601031 0.25645536]
```

### Nodes

AnaHiePro has three types of nodes: Problem, Criteria (also DummyCriteria, which use for normalizing the model) and Alternative. All of them is inherited from abstract class `Node`.

> **_NOTE:_** And we want to mentione that each class which is inhereted from `Node` has an id field.

#### Node class

As we mentioned before, `Node` is a basic class for `Problem`, `Criteria` and `Alternative`. Down below you can see all `Node`'s methods:
<br>

| Method Name       | Description                                       |
|-------------------|---------------------------------------------------|
| `__init__(self, name, parents, children, id, pcm)` | Initialize the `Node` object with given `name`, list of its `parents`, list of `children`, identifier (`id`) and pcm. |
| `get_name(self)`                    | Returns the name of the node. |
| `get_parents(self)`                 | Returns list of parents for the node. |
| `get_children(self)`                | Returns list of children for the node. |
| `get_key(self)`                     | Returns the tuple object, which consists of name of a node and its id. |
| `add_child(self, child)`            | Add `child` to the list of children. |
| `show(self)`                        | Returns str object, which represent all relations between nodes. |
| `compare(self, key: tuple)`         |  Compare the node with a given key, where `key` is a tuple object which has size that equal 2. `key[0]` is a name of node and `key[1]` is an identifier of the node. |
| `create_pcm(self)`                  | Create a pairwise comparison matrix (PCM) object for the node which shape is equal number of node's childrens. |
| `set_matrix(self, matrix)`          | Attach given PCM to the node. If the `self.pcm` does not exist call the `create_pcm` method than checks if the shape of given matrix matchs, raise `VlalueError` if does not otherwise attach it. |
| `set_comparison(self, i, j, value)` |  Set given `value` to the right place. Other words it is a wrapper above the `PairwiseComparisonMatrix`'s `set_comparison` method. |
| `get_priority_vector(self)`         | Wrapper above PairwiseComparisonMatrix`'s `get_priority_vector` method. |
| `get_consistency_ratio(self)`       | Wrapper above PairwiseComparisonMatrix`'s `get_consistency_ratio` method. |
| `get_pcm(self)`                     | Returns the pairwise comparison matrix of the node. |
| `__eq__(self, value)` | Compare two `Node`'s instance. |
| `def show(self)` | Show the node and its children in a hierarchical structure. |
| `__copy__(self)` | Copy the node. |


#### Problem class

`Problem` is a class that represents the problem that the user wants to solve. This class inherits from Node and has the same methods as its parent. However, it overrides some methods.

| Method Name       | Description                                       |
|-------------------|---------------------------------------------------|
| `__init__(self, name, children, pcm)` | Initialize the `Problem` object with given `name`, list of its childern and pairwise comparison matrix. |

The remaining methods are the same as in the `Node` class.

#### Criteria class

`Criteria` represents the criteria which will be used for selection. This class inherits form `Node` and has the same methods as his parrent, except of this it overrides some methods.

| Method Name       | Description                                       |
|-------------------|---------------------------------------------------|
| `__init__(self, name, children, pcm)` | Initialize the `Criteria` object with given `name`, list of its childern and pairwise comparison matrix. |

The remaining methods are the same as in the `Node` class.

#### DummyCriteria class

`DummyCriteria` class that inherited from `Criteria` it is used for normalizing problem in `VaryDepthModel`.

#### Alternative class

`Alternative` represents alternatives between which the selection occurs. Since `Alternative` is the final node in the hierarchy, it has no children, so the self.pcm field for it is deleted.

| Method Name       | Description                                       |
|-------------------|---------------------------------------------------|
| `__init__(self, name)` | Initialize the `Alternative` object with given `name`. |
| `create_pcm(self)` | Not implemented for reasons which were mentioned. |
| `set_matrix(self, matrix)` | Not implemented and raise `NotImplementedError` exception. |
| `set_comparison(self, i, j, value) | Not implemented and raise `NotImplementedError` exception. |

The remaining methods are the same as in the `Node` class.

#### Example

```py
from anahiepro.nodes import Problem, Criteria, Alternative


# Create instance of each classes.
problem = Problem("Example Problem")

criteria1 = Criteria("Criteria_1")
criteria2 = Criteria("Criteria_2")

alternative1 = Alternative("Alternative_1")
alternative2 = Alternative("Alternative_2")

# Linking each instances.
problem.add_child(criteria1)
problem.add_child(criteria2)

criteria1.add_child(alternative1)
criteria1.add_child(alternative2)

criteria2.add_child(alternative1)
criteria2.add_child(alternative2)

# Print the problem hierarchy.
print(problem.show())
```

Output:

```
+Example Problem
+--Criteria_1
+----Alternative_1
+----Alternative_2
+--Criteria_2
+----Alternative_1
+----Alternative_2
```

### Models

AnaHiePro has two types of models that you can use to automatically solve the set problems: `Model` and `VaryDepthModel`.

#### Differences between `Model` and `VaryDepthModel`

These two classes are designed to solve different types of problems. Specifically, `VaryDepthModel` is used for problems with varying depths, as shown in the image below.

![example](assets/img/varydepthmodel.png)

On the other hand, `Model` can solve problems that have a hierarchy with the same depth for each child, as illustrated in the next picture.

![example](assets/img/normalmodel.png)

#### About Models

Each model class in AnaHiePro has methods that are described below.

| Method Name       | Description                                       |
|-------------------|---------------------------------------------------|
| `__init__(self, problem: Problem, criterias, alternatives: list)` | Initialize the model with a problem, criteria, and alternatives. Also checks if the criterias has correct format, type and for `Model` - if the depth of the criterias hierarchy is the same depth. |
| `get_problem(self)` | Return the problem instance. |
| `get_alternatives(self)` | Return the list of alternatives. |
| `get_criterias_name_ids(self)` | Get the names and IDs of the criteria. |
| `find_criteria(self, key: tuple)` | Find criteria by (name, id) tuple. |
| `attach_criteria_pcm(self, key: tuple, pcm)`| Attach a pairwise comparison matrix to the criteria identified by the key. |
| `__getitem__(self, key: tuple)` | Get the criteria identified by the key. |
| `solve(self, showAlternatives=False)` | Solve the model to calculate the global priority vector. |
| `show(self)` | Display the problem. |

#### Examples

`Model` and `VaryDepthModel` can take the next format of the criterias in their `__init__` method:

```py
criterias = [Criteria(children=[Criteria()]),
             Criteria(children=[Criteria()]),
             Criteria(children=[Criteria()])]
```

or

```py
criterias = [
    {Criteria(): [
        {Criteria(): None}
    ]},
    {Criteria(): [
        {Criteria(): None}
    ]},
    {Criteria(): [
        {Criteria(): None}
    ]}
]
```


Another formats of the `criterias` param is not added (except of empty list).

Here you can see the simplest way how to create `Model` instance:

```py
from anahiepro.nodes import Problem, Criteria, Alternative
from anahiepro.models.model import Model

problem = Problem("Example Problem")

list_of_criterias = [
    Criteria("Citeria_1", children=[
        Criteria("Criteria_4")
    ]),
    Criteria("Citeria_2", children=[
        Criteria("Criteria_5")
    ]),
    Criteria("Citeria_3", children=[
        Criteria("Criteria_5")
    ]),
]

alternatives = [
    Alternative("Alternative_1"),
    Alternative("Alternative_2")
]

model = Model(problem, list_of_criterias, alternatives)

print(model.show())
```

Output:

```
+Example Problem
+--Citeria_1
+----Criteria_4
+------Alternative_1
+------Alternative_2
+--Citeria_2
+----Criteria_5
+------Alternative_1
+------Alternative_2
+--Citeria_3
+----Criteria_5
+------Alternative_1
+------Alternative_2
```

Now let's see how it works for `VaryDepthModel`:

```py
from anahiepro.nodes import Problem, Criteria, Alternative
from anahiepro.models.vary_depth_model import VaryDepthModel

problem = Problem("Example Problem")

list_of_criterias = [
    Criteria("Citeria_1", children=[
        Criteria("Criteria_4")
    ]),
    Criteria("Citeria_2", children=[
        Criteria("Criteria_5")
    ]),
    Criteria("Citeria_3"),  # <- Here Criteria_3 does not have children.
]

alternatives = [
    Alternative("Alternative_1"),
    Alternative("Alternative_2")
]

model = VaryDepthModel(problem, list_of_criterias, alternatives)

print(model.show())
```

Output:

```
+Example Problem
+--Citeria_1
+----Criteria_4
+------Alternative_1
+------Alternative_2
+--Citeria_2
+----Criteria_5
+------Alternative_1
+------Alternative_2
+--DummyCriteria0
+----Citeria_3
+------Alternative_1
+------Alternative_2
```

So, as you can see from the output, `VaryDepthModel` normalized the hierarchy. And, yes, you can use `VaryDepthModel` with the example for `Model` class.

#### Example with the solving of the hierarchy

```py
from anahiepro.nodes import Problem, Criteria, Alternative
from anahiepro.models.model import Model

problem = Problem("Example Problem", pcm=[[1,   2,   1/2],
                                          [1/2, 1,   1/7],
                                          [2,   7,   1]])

list_of_criterias = [
    Criteria("Citeria_1", pcm=[[1,   2,   4],
                               [1/2, 1,   3],
                               [1/4, 1/3, 1]]),

    Criteria("Citeria_2", pcm=[[1,   2,   1/5],
                               [1/2, 1,   3],
                               [5,   1/3, 1]]),

    Criteria("Citeria_3", pcm=[[1,   1/3,   3],
                               [3,   1,   3],
                               [1/3, 1/3, 1]]),
]

alternatives = [
    Alternative("Alternative_1"),
    Alternative("Alternative_2"),
    Alternative("Alternative_3")
]

model = Model(problem, list_of_criterias, alternatives)

print("Global vector without alternatives:")
print(model.solve())

print("Global vector with alternatives:")
print(model.solve(showAlternatives=True))
```

Output:
```
Global vector without alternatives:
[0.64557092 0.88998852 0.15336415]

Global vector with alternatives:
[(Alternative_1, np.float64(0.6455709201621959)), (Alternative_2, np.float64(0.8899885172373624)), (Alternative_3, np.float64(0.15336414859759606))]
```

## ✍️ Authors <a name = "authors"></a>

- [@danylevych](https://github.com/danylevych) - Idea & Initial work
