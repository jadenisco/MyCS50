
# lecture 2 Python

## f strings

``` python
    name = "John"
    print(f"Hello, {name}")
```

## tuple

- sequence of immutable values

## set

- Collection of unique values

## dict

- Collection of key-value pairs

## Decorators

```python
def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done running the function.")
    return wrapper


@announce
def hello():
    print("Hello, world!")

hello()
```

## Look at lambda.py


