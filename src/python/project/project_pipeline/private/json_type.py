from typing import Any, List, Mapping, Union

# Values for JSON that aren't nested
_JSON = Union[str, int, float, bool, None]

# Multi-layered stops at JSON_4, so the maximum depth is 5 dicts/lists, like: {'a': {'b': {'c': {'d': {'e': 'f'}}}}}
# Add more nest layers if needed.
JSON_5 = _JSON
JSON_4 = Union[_JSON, List[JSON_5], Mapping[str, JSON_5]]
JSON_3 = Union[_JSON, List[JSON_4], Mapping[str, JSON_4]]
JSON_2 = Union[_JSON, List[JSON_3], Mapping[str, JSON_3]]
JSON_1 = Union[_JSON, List[JSON_2], Mapping[str, JSON_2]]
JSONType = Union[_JSON, List[JSON_1], Mapping[str, JSON_1]]

# skip type checking for layers
UnsafeJSON_5 = Union[_JSON, List[Any], Mapping[str, Any]]
UnsafeJSON_4 = Union[_JSON, List[UnsafeJSON_5], Mapping[str, UnsafeJSON_5]]
UnsafeJSON_3 = Union[_JSON, List[UnsafeJSON_4], Mapping[str, UnsafeJSON_4]]
UnsafeJSON_2 = Union[_JSON, List[UnsafeJSON_3], Mapping[str, UnsafeJSON_3]]
UnsafeJSON_1 = Union[_JSON, List[UnsafeJSON_2], Mapping[str, UnsafeJSON_2]]
UnsafeJSONType = Union[_JSON, List[UnsafeJSON_1], Mapping[str, UnsafeJSON_1]]
