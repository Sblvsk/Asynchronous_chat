import yaml
import codecs

data = {
    "list": ["foo", "bar", "baz"],
    "integer": 42,
    "nested_dict": {
        "key1": "value1€",
        "key2": "value2€",
        "key3": "value3€"
    }
}

with codecs.open('file.yaml', 'w', encoding='utf8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

with codecs.open('file.yaml', 'r', encoding='utf8') as f:
    loaded_data = yaml.load(f, Loader=yaml.FullLoader)

assert data == loaded_data
