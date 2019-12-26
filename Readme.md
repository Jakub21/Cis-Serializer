# Cis-Protocol
Set of classes to encode python dictionaries in byte strings.

## Usage

### Installation
To install this package navigate to root directory of this repo and execute `sudo python3 setup.py install`. Package is not available on PIP.

### Encoder
This example shows how to encode a dictionary
```python
from Cis import Query

# method 1
data = {'Hello': 'World', 'int': 1024, 'flt': 3.14159}
query = Query('Demo', **data)

# method 2
query = Query('Demo', Hello='World', int=1024, flt=3.14159)

# method 3
query = Query('Demo')
query.addParam('Hello', 'World')
query.addParam('int', 1044)
query.addParam('flt', 3.14159)

encoded = query.build()
```

Query is a dictionary wrapper class with methods usede in encoding. `Query` objects can be created in three ways, all shown in the example. After object is created and has all entries it can be encoded with `build` method. This method returns `bytes` that can be easily transported.

### Decoder
This example shows how to decode Cis Query
```python
from Cis import Parser

# get contents of "encoded" variable from Encoder example
encoded = b''

# Create parser instance and add encoded data
parser = Parser()
parser.pushBytes(encoded)
# Convert data into Query objects and retrieve them
parser.parse()
decoded = parser.queries.pop()
data_2 = decoded.params
```
Parser stores all data it received with `pushBytes` method. This allows for non-complete or multiple queries to be added to parser. Method `parse` converts bytes into `Query` objects and stores them in FIFO queue (refered to as `parser.queries` in code).

### Limitations

Input data can only contain inteters, floats and strings of limited set of characters. Allowed characters include upper- and lower-case letters and those: `_ . , ! @ # $ % ^ & *`. Character limitations also apply to dictionary keys.

When adding parameters with method 2 `q=Query(key, k=v)` it is not possible to add dictionary entry with key `key` or `params`.
