# Duet Software Framework Python Bindings

`dsf-python` provides Python bindings for the Duet Software Framework control server.
It exposes the DSF socket protocol as Python connection classes, typed object model
classes, command builders, and helpers for custom HTTP endpoints.

This project is also published on [PyPI](https://pypi.org/project/dsf-python/).

Useful links:

- [Duet Software Framework](https://github.com/Duet3D/DuetSoftwareFramework)
- [dsf-python examples](https://github.com/Duet3D/dsf-python/tree/main/examples)
- [Duet Software Framework forum](https://forum.duet3d.com/category/31/dsf-development)

## What The Library Contains

The top-level package is organised around the main DSF workflows.

- `dsf.connections`: socket-based client connections for commands, subscriptions, and code interception
- `dsf.commands`: request payload builders for low-level DSF commands
- `dsf.object_model`: the typed DSF object model and related enums
- `dsf.http`: helpers for custom HTTP and WebSocket endpoints exposed through DSF
- `dsf.exceptions`: shared exception types raised by connection classes

## Installation

The package can be installed from source:

```bash
python3 setup.py install
```

Or with `pip`:

```bash
python3 -m pip install dsf-python
```

Most code using this library must run on a system with Duet Software Framework
installed and with permission to access the DSF UNIX socket.

## Quick Start

### Run A Simple Command

Use `CommandConnection` to send general-purpose commands such as G-code or to
request the full object model on demand.

```python
from dsf.connections import CommandConnection

connection = CommandConnection()
connection.connect()

response = connection.perform_simple_code("M115")
print(response.result)

connection.close()
```

### Read The Object Model Once

```python
from dsf.connections import CommandConnection

connection = CommandConnection()
connection.connect()

object_model = connection.get_object_model()
print(object_model.state.status)
print(object_model.move.axes[0].letter)

connection.close()
```

### Subscribe To Object Model Updates

Use `SubscribeConnection` when you want DSF to push object model updates over a
subscription socket.

```python
from dsf.connections import SubscribeConnection, SubscriptionMode

subscription = SubscribeConnection(SubscriptionMode.PATCH)
subscription.connect()

object_model = subscription.get_object_model()

while True:
	object_model = subscription.get_object_model()
```

In `SubscriptionMode.PATCH`, the first `get_object_model()` call reads the full
model. Later calls reuse an internal cached model and apply one queued patch if
available.

## Connections

### CommandConnection

`CommandConnection` is the general-purpose connection type. It is used for:

- sending simple G-code
- requesting the full object model
- working with files, packages, plugins, and user sessions through DSF commands
- issuing lower-level requests through the command helpers in `dsf.commands`

Choose this connection when you want request-response behaviour and do not need
streamed updates.

### SubscribeConnection

`SubscribeConnection` receives streamed object model updates from DSF. It supports:

- `SubscriptionMode.FULL`: every update is a full object model
- `SubscriptionMode.PATCH`: every update is a partial JSON fragment

#### Key-Based Callbacks

`SubscribeConnection.subscribe_to_keys()` can run callbacks synchronously when
selected object model paths appear in a patch update processed by `get_object_model()`.

Key paths use dot notation and can include list indexes:

- `state.upTime`
- `heat.heaters.0.current`
- `move.axes.2.userPosition`

Use `^` in a list position to match any changed index:

- `heat.heaters.^.current`
- `tools.^.state`

Callbacks always receive keyword arguments:

- `key`: the subscribed key path that matched
- `data`: the changed value found at that path
- `indices`: a tuple of matched wildcard indexes, or `None` when the key does not use `^`

```python
from dsf.connections import SubscribeConnection, SubscriptionMode


def handle_change(*, key, data, indices):
	print(key, data, indices)


subscription = SubscribeConnection(SubscriptionMode.PATCH)
subscription.connect()
subscription.get_object_model()

unsubscribe = subscription.subscribe_to_keys(
	["heat.heaters.0.current", "state.upTime"],
	handle_change,
)

while True:
	object_model = subscription.get_object_model()
```

Wildcard example:

```python
def handle_any_heater(*, key, data, indices):
	print(key, indices, data)


subscription.subscribe_to_keys(
	["heat.heaters.^.current"],
	handle_any_heater,
)
```

### InterceptConnection

`InterceptConnection` is used for custom code handling and code interception. Use it
when a plugin needs to receive G/M/T-code events before or after the firmware handles them.

Typical use cases include:

- implementing custom M-codes
- inspecting or rewriting commands
- reacting to executed code notifications

See `examples/custom_m_codes.py` for a complete example.

## Object Model

The `dsf.object_model` package mirrors the DSF object model in typed Python classes.
It lets you work with structured properties instead of manually traversing raw JSON.

Examples:

```python
print(object_model.boards[0].name)
print(object_model.state.up_time)
print(object_model.move.axes[0].letter)
print(object_model.tools[0].state)
```

Object model instances support JSON-driven updates:

```python
object_model.update_from_json({"state": {"upTime": 1234}})
print(object_model.state.up_time)
```

This is the mechanism used internally when patch subscriptions are applied.

## Commands

The `dsf.commands` package contains low-level command builders for code execution,
file access, plugins, packages, object model manipulation, and other DSF protocol
requests.

Most users should start with the higher-level methods on `CommandConnection` or
`BaseCommandConnection`. Reach for `dsf.commands` directly when you need explicit
control over the payload sent to DSF.

## Custom HTTP Endpoints

The `dsf.http` module contains helpers for custom HTTP and WebSocket endpoints.
This is useful when a DSF plugin needs to expose an HTTP route that is handled by
Python code.

Key types include:

- `HttpEndpointUnixSocket`
- `HttpEndpointConnection`
- `ReceivedHttpRequest`
- `HttpResponseType`

See `examples/custom_http_endpoint.py` for a practical example.

## Included Examples

The `examples/` directory demonstrates the main workflows supported by the library.

- `send_simple_code.py`: send G-code over a command connection
- `subscribe_object_model.py`: subscribe to object model updates
- `custom_m_codes.py`: intercept and implement custom M-codes
- `custom_http_endpoint.py`: serve a custom HTTP endpoint through DSF

## API Reference

The Sphinx docs expose the package API for the major public modules:

- `dsf`
- `dsf.connections`
- `dsf.commands`
- `dsf.object_model`
- `dsf.http`

## Development Notes

The library talks to DSF using the configured UNIX socket path. By default this is
resolved from the DSF config and falls back to `/run/dsf/dcs.sock`.

If you are extending the library itself, the test suite under `tests/` contains
mock socket servers and object model fixtures that are useful for validating new
connection behaviour.
