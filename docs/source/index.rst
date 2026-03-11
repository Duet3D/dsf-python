.. dsf documentation master file, created by
   sphinx-quickstart on Sun Mar 28 21:52:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dsf's documentation!
====================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

API
===

Subscription Polling
====================

Patch subscriptions can be polled without blocking by checking
``BaseConnection.has_data_available()`` before reading the next patch.

.. code-block:: python

   from dsf.connections import SubscribeConnection, SubscriptionMode

   subscription = SubscribeConnection(SubscriptionMode.PATCH)
   subscription.connect()
   object_model = subscription.get_object_model()

   while True:
      if subscription.has_data_available():
         object_model.update_from_json(subscription.get_object_model_patch())

.. automodule:: dsf
   :members:
.. automodule:: dsf.connections
   :members:
.. automodule:: dsf.http_endpoint
   :members:
.. automodule:: dsf.commands
   :members:
.. automodule:: dsf.initmessages
   :members:
.. automodule:: dsf.model
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
