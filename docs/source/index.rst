dsf-python
==========

``dsf-python`` is a Python client for the `Duet Software Framework <https://github.com/Duet3D/DuetSoftwareFramework>`_
(DSF) control server. It talks to DSF over its UNIX socket and provides:

- ``dsf.connections``: connections for sending commands, subscribing to the object model and intercepting codes
- ``dsf.object_model``: the DSF object model as typed Python classes
- ``dsf.http``: custom HTTP and WebSocket endpoints served through DSF
- ``dsf.commands``: low-level builders for every DSF command

It follows the C# ``DuetAPIClient`` closely, but uses Python naming. See :ref:`differences` before porting
C# code or reading the DSF docs.

.. contents::
   :local:
   :depth: 2

Installation
------------

.. code-block:: bash

   python3 -m pip install dsf-python

Python 3.11 or newer is required. Your script must run on the machine that runs DSF, as a user that can
access the DSF socket (usually the ``dsf`` user). The socket path is read from ``/opt/dsf/conf/config.json``
and falls back to ``/run/dsf/dcs.sock``.

Quick Start
-----------

.. code-block:: python

   from dsf.connections import CommandConnection

   connection = CommandConnection()
   connection.connect()
   try:
       print(connection.perform_simple_code("M115"))

       object_model = connection.get_object_model()
       print(object_model.state.status.value)
       print(object_model.state.up_time)       # "upTime" in DSF
   finally:
       connection.close()

Connections
-----------

========================== =============================================================================================
Connection                 Use it to
========================== =============================================================================================
``CommandConnection``      Run codes, evaluate expressions, read the object model, manage plugins, files and HTTP endpoints
``SubscribeConnection``    Keep a local copy of the object model up to date and react to changes
``InterceptConnection``    Handle custom M-codes, or inspect codes before or after DSF processes them
========================== =============================================================================================

Every connection is configured in its constructor, opened with ``connect()`` and closed with ``close()``.
Errors reported by DSF are raised as ``InternalServerException`` (with ``error_type`` and ``error_message``),
or as ``TaskCanceledException`` if DSF cancelled the request.

SubscribeConnection
^^^^^^^^^^^^^^^^^^^

- In ``SubscriptionMode.PATCH``, the first ``get_object_model()`` call blocks until the full model arrives.
  Later calls do not block: they apply every queued patch to the cached model and return it.
- In ``SubscriptionMode.FULL``, every call blocks until the next full object model arrives.
- ``subscribe_to_keys()`` callbacks run synchronously inside ``get_object_model()``, only in patch mode, and
  receive the keyword arguments ``key``, ``data`` (the raw JSON value from the patch) and ``indices`` (the list
  indexes matched by ``^``, or ``None``). Register them after the first ``get_object_model()`` call.
  The return value removes the callback again.
- DSF sends each message only once, so in patch mode ``object_model.messages`` collects the messages of every
  applied patch. By default ``get_object_model()`` clears it first, so it holds only the messages received since
  the previous call. With ``SubscribeConnection(..., clear_messages=False)`` messages are kept until you clear the
  list.

See :ref:`example-subscribe`.

InterceptConnection
^^^^^^^^^^^^^^^^^^^

Every intercepted code must be answered with ``resolve_code()``, ``ignore_code()`` or ``cancel_code()``.
``InterceptConnection`` also has all ``CommandConnection`` methods, so it can run other codes while a code
is intercepted, e.g. ``perform_simple_code("M117 hi", code.channel)``.

See :ref:`example-m-codes`.

Custom HTTP Endpoints
^^^^^^^^^^^^^^^^^^^^^

``CommandConnection.add_http_endpoint()`` registers ``/machine/{namespace}/{path}`` with DSF and returns an
``HttpEndpointUnixSocket``. Pass an ``async`` handler to ``set_endpoint_handler()``. It receives an
``HttpEndpointConnection`` for each request. Call ``remove_http_endpoint()`` and then ``close()`` the socket
when finished.

See :ref:`example-http`.

.. _differences:

Differences From The DSF API
----------------------------

Naming
^^^^^^

Python attributes and methods are ``snake_case``. **Anything passed to DSF as a string stays in DSF's**
**camelCase format**, because DSF interprets it and not this library.

.. list-table::
   :header-rows: 1

   * -
     - DSF / C#
     - dsf-python
   * - Object model properties
     - ``state.upTime``, ``move.axes[0].userPosition``
     - ``state.up_time``, ``move.axes[0].user_position``
   * - Uppercase acronyms
     - ``move.skew.tanXY``
     - ``move.skew.tan_XY`` (acronyms stay uppercase)
   * - Global variables
     - ``global``
     - ``globals`` (``global`` is a Python keyword)
   * - Names shadowing builtins (``type``, ``id``, ``min``, ``max``, ``format``, ``license``)
     - ``axis.max``
     - ``axis.max`` (unchanged)
   * - Methods
     - ``PerformSimpleCodeAsync()``
     - ``perform_simple_code()``
   * - Intercepted ``Code`` attributes
     - ``MajorNumber``, ``KeywordArgument``
     - ``majorNumber``, ``keywordArgument`` (**camelCase, as in the JSON**)
   * - ``CodeParameter`` attributes
     - ``StringValue``, ``IsString``
     - ``string_value``, ``is_string``
   * - HTTP request fields
     - ``SessionId``, ``ContentType``
     - ``session_id``, ``content_type``
   * - Error responses
     - ``errorType``, ``errorMessage``
     - ``error_type``, ``error_message``
   * - Enum members
     - ``MessageType.Success``
     - Not normalised: ``MessageType.Success``, ``MachineStatus.idle``, ``SubscriptionMode.PATCH``,
       ``HttpEndpointType.GET``. Values match the DSF JSON.

These strings keep DSF naming:

.. list-table::
   :header-rows: 1

   * - Where
     - Format
     - Example
   * - ``SubscribeConnection(filter_list=...)``
     - ``/``-separated, ``[*]`` for any list item, ``**`` for everything below
     - ``"heat/heaters[*]/current"``, ``"move/**"``
   * - ``CommandConnection.get_object_model(filters)``
     - ``.``-separated key paths
     - ``["state", "move.axes"]``
   * - ``SubscribeConnection.subscribe_to_keys(keys)``
     - ``.``-separated, list indexes as numbers, ``^`` for any list item
     - ``"heat.heaters.^.current"``, ``"move.axes.2.userPosition"``
   * - ``evaluate_expression()``, ``query_object_model()``, G-code
     - RepRapFirmware expressions
     - ``"state.upTime"``, ``"move.axes[0].homed"``

``ObjectModel.update_from_json()`` and ``from_json()`` take DSF JSON (camelCase), and ``to_json()`` writes it back:

.. code-block:: python

   object_model.update_from_json({"state": {"upTime": 1234}})
   object_model.state.up_time    # 1234
   object_model.to_json()        # '{..."state": {..."upTime": 1234...}...}'

Behaviour
^^^^^^^^^

- **Synchronous.** Connection methods block and have no ``Async`` suffix or ``CancellationToken``.
  Only HTTP endpoint handlers are ``async`` coroutines.
- **Configuration in the constructor.** Options passed to C# ``ConnectAsync()`` (mode, filters, channels,
  ``verbose``, ...) are constructor arguments. ``connect()`` takes only an optional socket path.
- **Patches are applied for you.** ``SubscribeConnection.get_object_model()`` keeps an internal model up to
  date in patch mode. In C#, you apply patches from ``GetObjectModelPatchAsync()`` yourself.
  ``get_object_model_patch()`` and ``get_serialized_object_model()`` still return raw JSON if you need it.
- **Key callbacks** (``subscribe_to_keys()``) are specific to dsf-python.
- **Messages are cleared for you.** In C#, messages pile up in ``Model.Messages`` until you clear them.
  ``get_object_model()`` clears them at the start of each call unless ``clear_messages=False``.
- **Return values.** ``perform_simple_code()`` returns the reply as a string. ``evaluate_expression()`` and the
  lower-level methods return a ``Response`` whose value is in ``.result``.
- **Interception.** ``resolve_code()`` takes a ``MessageType`` and an optional string, not a ``Message``.
  There is no ``rewrite_code()``. ``flush()`` takes a channel instead of flushing the intercepted code's channel.
- **HTTP endpoints.** Handlers are registered with ``set_endpoint_handler()`` instead of an event.
  ``add_http_endpoint()`` returns an ``HttpEndpointUnixSocket``, which must be closed after
  ``remove_http_endpoint()``.

Examples
--------

The examples are also in the
`examples directory <https://github.com/Duet3D/dsf-python/tree/HEAD/examples>`_ on GitHub.

Send Commands
^^^^^^^^^^^^^

Run codes, evaluate expressions, read part of the object model, write messages and handle errors.

.. literalinclude:: ../../examples/send_commands.py
   :language: python

.. _example-subscribe:

Subscribe To The Object Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Filtered patch subscription and key callbacks with and without ``^``.

.. literalinclude:: ../../examples/subscribe_object_model.py
   :language: python

.. _example-m-codes:

Custom M-Codes
^^^^^^^^^^^^^^

Custom M-codes, reading parameters and running codes from an interceptor.

.. literalinclude:: ../../examples/custom_m_codes.py
   :language: python

.. _example-http:

Custom HTTP Endpoints
^^^^^^^^^^^^^^^^^^^^^

GET and POST endpoints with plain text and JSON responses.

.. literalinclude:: ../../examples/custom_http_endpoint.py
   :language: python

API Reference
-------------

.. automodule:: dsf.connections
   :imported-members:

.. automodule:: dsf.object_model
   :imported-members:

.. automodule:: dsf.http

.. automodule:: dsf.commands.code

.. automodule:: dsf.commands.code_parameter

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
