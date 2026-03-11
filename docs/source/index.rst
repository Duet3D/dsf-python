.. dsf documentation master file, created by
   sphinx-quickstart on Sun Mar 28 21:52:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dsf's documentation!
====================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

Overview
========

`dsf-python` is the Python client library for the Duet Software Framework control
server. It provides:

- connection classes for DSF sockets
- typed object model classes
- command builders for low-level DSF operations
- helpers for custom HTTP and WebSocket endpoints

The main public modules are:

- ``dsf``: package entry point, protocol constants, and default socket discovery
- ``dsf.connections``: command, subscription, and interception connections
- ``dsf.commands``: low-level DSF command payload builders
- ``dsf.object_model``: typed object model classes and enums
- ``dsf.http``: HTTP endpoint helpers for DSF plugins

Getting Started
===============

Run A Simple Command
--------------------

.. code-block:: python

   from dsf.connections import CommandConnection

   connection = CommandConnection()
   connection.connect()

   response = connection.perform_simple_code("M115")
   print(response.result)

   connection.close()

Read The Object Model Once
--------------------------

.. code-block:: python

   from dsf.connections import CommandConnection

   connection = CommandConnection()
   connection.connect()

   object_model = connection.get_object_model()
   print(object_model.state.status)
   print(object_model.move.axes[0].letter)

   connection.close()

Connection Types
================

CommandConnection
-----------------

Use ``CommandConnection`` for request-response workflows such as:

- sending G-code
- requesting the full object model
- interacting with files, plugins, packages, and user sessions

SubscribeConnection
-------------------

Use ``SubscribeConnection`` to receive streamed object model updates.

- ``SubscriptionMode.FULL`` sends a full object model for every update
- ``SubscriptionMode.PATCH`` sends partial JSON fragments for each update

In patch mode, the first ``get_object_model()`` call reads the full model. Later
calls reuse an internal cached model and apply one queued patch if available.


Callbacks For Specific Keys
===========================

``SubscribeConnection.subscribe_to_keys()`` registers a callback for one or more
dot-delimited object model key paths. Call ``get_object_model()`` once first, then
register the callback to receive matching values synchronously from later patch
updates processed by ``get_object_model()``.

Callbacks always receive these keyword arguments:

- ``key``: the subscribed key path that matched
- ``data``: the changed value found at that key path
- ``indices``: a tuple of matched wildcard indexes or ``None``

Use ``^`` in list positions to match any changed list item.

.. code-block:: python

   from dsf.connections import SubscribeConnection, SubscriptionMode

   def handle_changes(*, key, data, indices):
      print(key, data, indices)

   subscription = SubscribeConnection(SubscriptionMode.PATCH)
   subscription.connect()
   subscription.get_object_model()
   subscription.subscribe_to_keys(
      ["heat.heaters.0.current", "state.upTime"],
      handle_changes,
   )

   while True:
      object_model = subscription.get_object_model()

.. code-block:: python

   def handle_any_heater(*, key, data, indices):
      print(key, indices, data)

   subscription.subscribe_to_keys(
      ["heat.heaters.^.current"],
      handle_any_heater,
   )

InterceptConnection
-------------------

Use ``InterceptConnection`` when a Python component needs to intercept or handle
G/M/T-code traffic. This is the connection type used by custom M-code handlers and
other DSF plugin workflows.

Object Model
============

The ``dsf.object_model`` package mirrors the DSF object model in typed Python classes.
It lets applications work with structured attributes instead of raw JSON dictionaries.

.. code-block:: python

   print(object_model.boards[0].name)
   print(object_model.state.up_time)
   print(object_model.move.axes[0].letter)

Object model instances can also be updated from JSON fragments:

.. code-block:: python

   object_model.update_from_json({"state": {"upTime": 1234}})

Commands
========

The ``dsf.commands`` package contains the low-level request builders used by the
connection classes. Most applications will call higher-level connection methods,
but the command modules are available when direct control over a DSF request is needed.

Custom HTTP Endpoints
=====================

The ``dsf.http`` module provides helpers for custom HTTP and WebSocket endpoints
implemented in Python.

Important types include:

- ``HttpEndpointUnixSocket``
- ``HttpEndpointConnection``
- ``ReceivedHttpRequest``
- ``HttpResponseType``

Examples
========

The project includes examples for the major workflows:

- ``examples/send_simple_code.py``
- ``examples/subscribe_object_model.py``
- ``examples/custom_m_codes.py``
- ``examples/custom_http_endpoint.py``

API Reference
=============

.. automodule:: dsf
   :members:
.. automodule:: dsf.connections
   :members:
.. automodule:: dsf.commands
   :members:
.. automodule:: dsf.object_model
   :members:
.. automodule:: dsf.http
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
