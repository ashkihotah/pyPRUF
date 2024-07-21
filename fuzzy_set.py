import time

from pandas import DataFrame
from fuzzy_logic import FuzzyAnd, FuzzyNot, FuzzyOr

class DiscreteFuzzySet:
    def __init__(self, name: str, schema: tuple = None, dict_relation: dict = None, dataframe: DataFrame = None):
        if dataframe is not None:
            dict_relation = {}
            for key, value in dataframe.to_dict().items():
                dict_relation[key] = tuple(value.values())
            # print(dict_relation)
            keys = list(dict_relation.keys())
            # assert 'mu' in keys, "The membership degree column is missing!"
            # assert isinstance(dict_relation, dict), "'dict_relation' must be a dictionary in the numpy.DataFrame format!"
            assert len(keys) > 0, "There must be at least one column!"
            assert isinstance(keys[0], str), "All keys in 'dict_relation' must be strings representing the variables name!"
            assert isinstance(dict_relation[keys[0]], list) or isinstance(dict_relation[keys[0]], tuple), "All the values in 'dict_relation' must be lists or tuples with the same length!"
            length = len(dict_relation[keys[0]])
            assert length > 0, "The fuzzy set must contain at least a tuple!"
            for key, value in dict_relation.items():
                assert isinstance(key, str), "All keys in 'dict_relation' must be strings representing the variables name!"
                assert (isinstance(value, list) or isinstance(value, tuple)) and len(value) == length, "All the values in the dictionary must be lists or tuples with the same length!"
            
            self.__fuzzy_set = {}
            for i in range(0, length):
                variables = []
                mu = 1.0
                for key in keys:
                    if key != 'mu':
                        variables.append(dict_relation[key][i])
                    else:
                        mu = dict_relation[key][i]
                        assert isinstance(mu, float) and 0.0 <= mu and mu <= 1.0, "All values in 'mu' must be floats between [0, 1]!"
                self.__fuzzy_set[tuple(variables)] = mu

            if 'mu' in keys:
                keys.remove('mu')
            self.__schema = tuple(keys)
        else:
            assert (isinstance(schema, list) or isinstance(schema, tuple)) and len(schema) > 0, "'schema' must be a non-empty list or tuple of strings representing the variables names!"
            assert isinstance(dict_relation, dict), "'dict_relation' must be a dictionary!"
            length = len(schema)
            sorted_schema = list(schema)
            sorted_schema.sort()
            for i in range(1, len(sorted_schema)):
                assert schema[i] != schema[i - 1], "'schema' must not contains duplicates!"

            
            self.__fuzzy_set = {}
            for element, mu in dict_relation.items():
                assert (isinstance(element, list) or isinstance(element, tuple)) and len(element) == length, "All keys in 'dict_relation' must be lists or tuples with the same length as the schema!"
                assert isinstance(mu, float) and 0.0 <= mu and mu <= 1.0, "All memberships values must be floats between [0, 1]!"
                self.__fuzzy_set[tuple(element)] = mu

            self.__schema = list(schema)
        self.name = name
        

    def __getitem__(self, element) -> float:
        if element in self.__fuzzy_set.keys():
            return self.__fuzzy_set[element]
        return 0.0
    
    def __setitem__(self, element, membership: float) -> None:
        assert isinstance(membership, float), "'membership' must be a float!"
        assert 0 <= membership and membership <= 1, "'membership' must be between 0 and 1 inclusive!"
        assert isinstance(element, tuple), "'element' must be a tuple! "
        assert len(self.__schema) == len(element), "'element' must be a tuple of the same length of the schema!"

        self.__fuzzy_set[element] = membership

    def get_cardinality(self) -> float:
        memberships_sum = 0.0
        for value in self.__fuzzy_set.values():
            memberships_sum += value
        return memberships_sum
    
    def get_relative_cardinality(self) -> float:
        memberships_sum = 0.0
        n = 0
        for value in self.__fuzzy_set.values():
            memberships_sum += value
            n += 1
        return memberships_sum / n

    def to_dictionary(self) -> dict:
        return self.__fuzzy_set.copy()
    
    def get_tabular_str(self) -> str:
        # print("{:<25}{:<25}{:<25}{:<25}".format("Metric", "Score Mean", "Score Variance", "Score Std"))
        s = self.name + ' = \n'
        for key in self.__schema:
            s += "{:<15}".format(key)
        s += 'mu\n\n'
        for key, value in self.__fuzzy_set.items():
            for var in key:
                s += "{:<15}".format(var)
            s += "{:<15}\n".format(value)
        return s

    def get_string_repr(self) -> str:
        s = self.name + ' ='
        for value, membership in self.__fuzzy_set.items():
            s += ' ' + str(membership) + '/' + str(value) + ' +'
        if len(self.__fuzzy_set.items()) > 0:
            return s[:-2]
        return self.name + ' = ∅'
        # return self.name + f" = {self.__fuzzy_set}"

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def get_schema(self) -> tuple:
        return tuple(self.__schema)

    def rename_schema(self, ren_dict: dict) -> None:
        assert isinstance(ren_dict, dict), "'dict_relation' must be a dictionary!"
        for key, value in ren_dict.items():
            assert isinstance(key, str) and isinstance(key, str), "All keys and values in 'ren_dict' must be strings!"
            assert key in self.__schema, key + " not in " + self.name + " schema!"
            assert value not in self.__schema, value + " already in " + self.name + " schema!"
            self.__schema[self.__schema.index(key)] = value

def proportion(set1: DiscreteFuzzySet, set2: DiscreteFuzzySet, and_fun: FuzzyAnd) -> float:
    assert isinstance(set1, DiscreteFuzzySet) and isinstance(set2, DiscreteFuzzySet), "'set1' and 'set2' must be both of type 'DiscreteFuzzySet'!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
    new_set = intersection(set1, set2, and_fun)
    return new_set.get_cardinality() / set2.get_cardinality()

def cartesian_product(set1: DiscreteFuzzySet, set2: DiscreteFuzzySet, and_fun: FuzzyAnd) -> DiscreteFuzzySet:
    assert isinstance(set1, DiscreteFuzzySet) and isinstance(set2, DiscreteFuzzySet), "'set1' and 'set2' must be both of type 'DiscreteFuzzySet'!"
    set1_schema = set1.get_schema()
    for var in set2.get_schema():
        assert var not in set1_schema, "'" + var + "' is in " + set1.name + " schema: " + str(set1_schema) + "\n'set1' and 'set2' must have different schemas!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"

    new_set = {}
    for element1, membership1 in set1.to_dictionary().items():
        for element2, membership2 in set2.to_dictionary().items():
            new_set[element1 + element2] = and_fun(membership1, membership2)
    fs = DiscreteFuzzySet(set1.name + ' × ' + set2.name, set1.get_schema() + set2.get_schema(), new_set)
    return fs

def union(set1: DiscreteFuzzySet, set2: DiscreteFuzzySet, or_fun: FuzzyOr) -> DiscreteFuzzySet:
    assert isinstance(set1, DiscreteFuzzySet) and isinstance(set2, DiscreteFuzzySet), "'set1' and 'set2' must be both of type 'DiscreteFuzzySet'!"
    assert set1.get_schema() == set2.get_schema(), "'set1' and 'set2' must have the same schema!"
    assert isinstance(or_fun, FuzzyOr), "'or_fun' must be of type 'FuzzyOr'!"

    new_set = set1.to_dictionary()
    for element, membership2 in set2.to_dictionary().items():
        membership1 = set1[element]
        new_set[element] = or_fun(membership1, membership2)
    fs = DiscreteFuzzySet(set1.name + ' ∪ ' + set2.name, set1.get_schema(), new_set)
    return fs

def intersection(set1: DiscreteFuzzySet, set2: DiscreteFuzzySet, and_fun: FuzzyAnd) -> DiscreteFuzzySet:
    assert isinstance(set1, DiscreteFuzzySet) and isinstance(set2, DiscreteFuzzySet), "'set1' and 'set2' must be both of type 'DiscreteFuzzySet'!"
    assert set1.get_schema() == set2.get_schema(), "'set1' and 'set2' must have the same schema!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
    
    new_set = {}
    set1_keys = set1.to_dictionary().keys()
    set2_items = set2.to_dictionary().items()
    for value, membership2 in set2_items:
        if value in set1_keys:
            membership1 = set1[value]
            new_membership = and_fun(membership1, membership2)
            if new_membership > 0: # scelta progettuale: gli elementi con mu == 0 li mantieni oppure no? -> scelgo no
                new_set[value] = new_membership
    fs = DiscreteFuzzySet(set1.name + ' ∩ ' + set2.name, set1.get_schema(), new_set)
    return fs

def complement(fuzzy_set: DiscreteFuzzySet, not_fun: FuzzyNot) -> DiscreteFuzzySet:
    assert isinstance(fuzzy_set, DiscreteFuzzySet), "'fuzzy_set' must be of type 'DiscreteFuzzySet'!"
    assert isinstance(not_fun, FuzzyNot), "'not_fun' must be of type 'FuzzyNot'!"

    new_set = {}
    for value, membership in fuzzy_set.to_dictionary().items():
        new_membership = not_fun(membership)
        if new_membership > 0: # scelta progettuale: gli elementi con mu == 0 li mantieni oppure no? -> scelgo no
            new_set[value] = new_membership

    fs = DiscreteFuzzySet('~' + fuzzy_set.name, fuzzy_set.get_schema(), new_set)
    return fs

def or_projection(fuzzy_set: DiscreteFuzzySet, subvariable: tuple, or_fun: FuzzyOr) -> DiscreteFuzzySet:
    assert isinstance(fuzzy_set, DiscreteFuzzySet), "'fuzzy_set' must be of type 'DiscreteFuzzySet'!"
    assert isinstance(or_fun, FuzzyOr), "'or_fun' must be of type 'FuzzyOr'!"
    assert isinstance(subvariable, tuple), "'subvariable' must be a sub-tuple of variables from the schema of the fuzzy set!"

    schema = fuzzy_set.get_schema()
    indexes = []
    for var in subvariable:
        assert var in schema, "'" + str(var) + "' not in the schema of the fuzzy set!"
        indexes.append(schema.index(var))

    items = fuzzy_set.to_dictionary().items()
    new_set = {}
    for element, membership in items:
        new_tuple = []
        for index in indexes:
            new_tuple.append(element[index])

        new_tuple = tuple(new_tuple)
        if new_tuple in new_set.keys():
            new_set[new_tuple] = or_fun(new_set[new_tuple], membership)
        else:
            new_set[new_tuple] = membership

    fs = DiscreteFuzzySet('Proj(' + fuzzy_set.name + ', ' + str(subvariable) + ')', subvariable, new_set)
    return fs

def and_projection(fuzzy_set: DiscreteFuzzySet, subvariable: tuple, and_fun: FuzzyAnd) -> DiscreteFuzzySet:
    assert isinstance(fuzzy_set, DiscreteFuzzySet), "'fuzzy_set' must be a 'DiscreteFuzzySet'!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
    assert isinstance(subvariable, tuple), "'subvariable' must be a sub-tuple of variables from the schema of the fuzzy set!"

    schema = fuzzy_set.get_schema()
    indexes = []
    for var in subvariable:
        assert var in schema, "'" + str(var) + "' not in the schema of the fuzzy set!"
        indexes.append(schema.index(var))

    items = fuzzy_set.to_dictionary().items()
    new_set = {}
    for element, membership in items:
        new_tuple = []
        for index in indexes:
            new_tuple.append(element[index])

        new_tuple = tuple(new_tuple)
        if new_tuple in new_set.keys():
            new_set[new_tuple] = and_fun(new_set[new_tuple], membership)
        else:
            new_set[new_tuple] = membership

    fs = DiscreteFuzzySet('Proj(' + fuzzy_set.name + ', ' + str(subvariable) + ')', subvariable, new_set)
    return fs

def particularization(fuzzy_set: DiscreteFuzzySet, assignment: dict, and_fun: FuzzyAnd) -> DiscreteFuzzySet:
    assert isinstance(fuzzy_set, DiscreteFuzzySet), "'fuzzy_set' must be a 'DiscreteFuzzySet'!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"
    assert isinstance(assignment, dict), "'assignment' must be a dictionary!"

    schema = fuzzy_set.get_schema()
    indexes = []
    fs_indexes = []
    for var in assignment.keys():
        assert var in schema, "'" + str(var) + "' not in the schema of the fuzzy set!"
        index = schema.index(var)
        if isinstance(assignment[schema[index]], DiscreteFuzzySet):
            fs_indexes.append(index)
        else:
            indexes.append(index)
    
    new_set = {}
    for element, membership in fuzzy_set.to_dictionary().items():
        for index in indexes:
            if element[index] != assignment[schema[index]]:
                membership = 0
                break
        for index in fs_indexes:
            membership = and_fun(assignment[schema[index]][(element[index],)], membership)
        if membership > 0:
            new_set[element] = membership

    fs = DiscreteFuzzySet(fuzzy_set.name + str(assignment), schema, new_set)
    return fs

def natural_join(set1: DiscreteFuzzySet, set2: DiscreteFuzzySet, and_fun: FuzzyAnd) -> DiscreteFuzzySet:
    assert isinstance(set1, DiscreteFuzzySet) and isinstance(set2, DiscreteFuzzySet), "'set1' and 'set2' must be both of type 'DiscreteFuzzySet'!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"

    schema1 = set1.get_schema()
    schema2 = list(set2.get_schema())
    indexes1 = []
    indexes2 = []
    for index, var in enumerate(schema1):
        if var in schema2:
            indexes1.append(index)
            indexes2.append(schema2.index(var))
            schema2.remove(var)

    assert len(indexes1) > 0, "'set1' and 'set2' must have at least one variable in common int their schema!"
    new_set = {}
    for element1, membership1 in set1.to_dictionary().items():
        for element2, membership2 in set2.to_dictionary().items():
            to_insert = True
            for index in range(0, len(indexes1)):
                if element1[indexes1[index]] != element2[indexes2[index]]:
                    to_insert = False
                    break
            if to_insert:
                new_elem = list(element1)
                for index, var in enumerate(element2):
                    if index not in indexes2:
                        new_elem.append(var)
                new_set[tuple(new_elem)] = and_fun(membership1, membership2)
    return DiscreteFuzzySet(set1.name + ' ⋈ ' + set2.name, schema1 + tuple(schema2), new_set)


def compatibility(fuzzy_set: DiscreteFuzzySet, reference_set: DiscreteFuzzySet) -> DiscreteFuzzySet:
    assert isinstance(fuzzy_set, DiscreteFuzzySet) and isinstance(reference_set, DiscreteFuzzySet), "'fuzzy_set' and 'reference_set' must be both of type 'DiscreteFuzzySet'!"
    assert fuzzy_set.get_schema() == reference_set.get_schema(), "'fuzzy_set' and 'reference_set' must have the same schema!"

    new_set = {}
    for element, membership in reference_set.to_dictionary().items():
        key = (reference_set[element], )
        if key in new_set.keys():
            new_set[key] = max(fuzzy_set[element], new_set[key])
        else:
            new_set[key] = fuzzy_set[element]
        
    return DiscreteFuzzySet('Comp(' + str(fuzzy_set) + ', ' + str(reference_set) + ')', fuzzy_set.get_schema(), new_set)

def consistency(fuzzy_set: DiscreteFuzzySet, reference_set: DiscreteFuzzySet, and_fun: FuzzyAnd) -> float:
    assert isinstance(fuzzy_set, DiscreteFuzzySet) and isinstance(reference_set, DiscreteFuzzySet), "'fuzzy_set' and 'reference_set' must be both of type 'DiscreteFuzzySet'!"
    assert fuzzy_set.get_schema() == reference_set.get_schema(), "'fuzzy_set' and 'reference_set' must have the same schema!"
    assert isinstance(and_fun, FuzzyAnd), "'and_fun' must be of type 'FuzzyAnd'!"

    consistency = -1
    for element, mu1 in reference_set.to_dictionary().items():
        consistency = max(and_fun(mu1, fuzzy_set[element]), consistency)

    return consistency

# Example usage:
if __name__ == "__main__":
    start_time = time.time()
    
    and_fun = FuzzyAnd.MIN
    or_fun = FuzzyOr.MAX
    not_fun = FuzzyNot.STANDARD

    # fs1 = DiscreteFuzzySet('A', {'V1': [1, 'val1', 2], 'V2': ['val2', 3.4, 'val2'], 'mu': [0.3, 0.6, 0.9]})
    # fs2 = DiscreteFuzzySet('B', {'V1': [2, 'val3', 'val1'], 'V2': ['val4', 4.4, 3.4], 'mu': [0.1, 0.5, 0.7]})
    # fs3 = DiscreteFuzzySet('C', {'X1': [2, 'val3'], 'mu': [0.1, 0.5]})

    fs1 = DiscreteFuzzySet('A', ('V1', 'V2'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
    fs2 = DiscreteFuzzySet('B', ('V1', 'V2'), {(2, 'val4'): 0.1, ('val3', 4.4): 0.5, ('val1', 3.4): 0.7})
    fs3 = DiscreteFuzzySet('C', ('V1', ), {(2,): 0.1, ('val3',): 0.5})
    fs4 = DiscreteFuzzySet('NOT(SMALL_INTEGER)', ('n', ), {(0, ): .0, (1, ): .0, (2, ): 0.2, (3, ): 0.4, (4, ): 0.6, (5, ): 0.8})
    not_fs4 = complement(fs4, not_fun)
    fs5 = DiscreteFuzzySet('D', ('V1', 'V3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})
    fs6 = DiscreteFuzzySet('D', ('V6', 'V3'), {(1, 'val2'): 0.3, ('val1', 3.4): 0.6, (2, 'val2'): 0.9})

    print(fs1[(1, 'val2')])
    fs1[(1, 'val2')] = 0.7
    print(fs1[(1, 'val2')])
    print(fs1.get_string_repr())
    print(fs2.get_string_repr())
    print(fs3.get_string_repr())
    print(fs4.get_string_repr())
    print(not_fs4.get_string_repr())
    print(fs5.get_string_repr())

    union_set = union(fs1, fs2, or_fun)
    intersection_set = intersection(fs1, fs2, and_fun)
    complement_set = complement(fs1, not_fun)
    cartesian_product_set = cartesian_product(fs1, fs6, and_fun)
    or_projection_set = or_projection(fs1, ('V2',), or_fun)
    and_projection_set = and_projection(fs1, ('V2',), and_fun)
    print(union_set.get_string_repr(), "\nschema:", union_set.get_schema(), end="")
    print("    cardinality:", union_set.get_cardinality())
    print(intersection_set.get_string_repr(), "\nschema:", intersection_set.get_schema(), end="")
    print("    cardinality:", intersection_set.get_cardinality())
    print(complement_set.get_string_repr(), "\nschema:", complement_set.get_schema(), end="")
    print("    cardinality:", complement_set.get_cardinality())
    print(cartesian_product_set.get_string_repr(), "\nschema:", cartesian_product_set.get_schema(), end="")
    print("    cardinality:", cartesian_product_set.get_cardinality())
    print(or_projection_set.get_string_repr(), "\nschema:", or_projection_set.get_schema(), end="")
    print("    cardinality:", or_projection_set.get_cardinality())
    print(and_projection_set.get_string_repr(), "\nschema:", and_projection_set.get_schema(), end="")
    print("    cardinality:", and_projection_set.get_cardinality())
    print(particularization(fs1, {'V1': fs3}, and_fun).get_string_repr())
    print("Prop{A/G} = ", proportion(fs1, fs2, and_fun))
    print(compatibility(not_fs4, fs4).get_string_repr())
    print("Cons{NOT(SMALL_INTEGER), SMALL_INTEGER} = ", consistency(not_fs4, fs4, and_fun))
    print(natural_join(fs1, fs5, and_fun).get_string_repr())

    fs1.rename_schema({'V1': 'X1', 'V2': 'X2'})
    print(fs1.get_schema())
    print(fs1.get_string_repr())

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nElapsed time: {elapsed_time} seconds")
