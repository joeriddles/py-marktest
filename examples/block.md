```python
def hello():
    print("hello")
```

```python
def outer():
    def inner():
        raise Exception() # raises: Exception

outer()
```
