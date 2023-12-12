```python
import operator
from retry_pytest.retry import Retry

with Retry() as r:
    r.check(operator.sub, 4, 2).equal(2)
```

```python
import operator
from retry_pytest.retry import Retry

with Retry(ZeroDivisionError, title='custom allure step title for skip ZeroDivisionError', timeout=10, poll_frequency=2) as r:
    r.check(operator.truediv, 4, 0).equal(2)
```

```python
import operator
from retry_pytest.retry import Retry

with Retry() as r:
    r.check(operator.sub, 4, 2).equal(1)
    r.on_timeout(print, 'wtf')
```

```python
import operator
from retry_pytest.retry import Retry

with Retry() as r:
    r.check(operator.sub, 4, 2).equal(2)
    r.check(operator.add, 2, 2).equal(4)
```

```python
from retry_pytest.retry import Retry

def get_result_as_list_of_dicts():
    return [{'key1': 'data1', 'key2': 'data2'}]
 
with Retry() as r:
    r.check(get_result_as_list_of_dicts).get(0).get('key1').equal('data1')
```

```python
from retry_pytest.retry import Retry

def get_result_as_list():
    return [1,2,3]
 
with Retry() as r:
    r.check(get_result_as_list).get(0).equal(1)
```

```python
from retry_pytest.retry import Retry

def get_result_as_dict():
    return {'key1': 'data1', 'key2': 'data2'}
 
with Retry() as r:
    r.check(get_result_as_dict).get('key1').equal('data1')
```

```python
from retry_pytest.retry import Retry

def get_result_as_list_of_dicts():
    return [{'key1': 'data1', 'key2': 'data2'}]
 
with Retry() as r:
    r.check(get_result_as_list_of_dicts).get(0).get('key1').equal('data1')
    r.check(get_result_as_list_of_dicts).get(0).get('key2').equal('data2')
 
print(r.commands[-2].result)
print(r.last_command.result)
```