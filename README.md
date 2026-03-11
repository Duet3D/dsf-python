# Duet Software Framework Python Bindings

This is also availabe as a [pip package on pypi](https://pypi.org/project/dsf-python/)

Find out more about [Duet Software Framework](https://github.com/Duet3D/DuetSoftwareFramework).

Examples of the [Duet Software Framework Python Bindings](https://github.com/Duet3D/dsf-python/tree/main/examples).

Get in touch with the community at [Duet Software Framework Forum](https://forum.duet3d.com/category/31/dsf-development) for bug reports, discussion and any kind of exchange.

## Installation
This package contains a `setup.py` so it can be installed with `python3 setup.py install`.

## Usage
See included `examples/` folder for various use cases.

For patch subscriptions, `BaseConnection.has_data_available()` can be used to poll a
subscription socket without blocking on `receive_json()` or `get_object_model_patch()`.
This is useful when object model updates arrive less frequently than another data source.

```python
from dsf.connections import SubscribeConnection, SubscriptionMode

subscription = SubscribeConnection(SubscriptionMode.PATCH)
subscription.connect()
object_model = subscription.get_object_model()

while True:
	if subscription.has_data_available():
		object_model.update_from_json(subscription.get_object_model_patch())
```
