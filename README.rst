pyzanata
========

Alternative `Zanata <http://zanata.org/>`_ restapi client.

Usage
-----

In order to get started two imports are needed::

    from pyzanata import ZanataCredentials
    from pyzanata import ZanataClient

First credentials needs to be set::

    credentials = ZanataCredentials('http://zanata.exampl.com', 'johndoe', 'secret')

Then the client can be initialized::

    client = ZanataClient(credentials)

Now Zanata infos can be fetched::

    client.ProjectsResource.projects.GET()

Consult the `Zanata REST API Documentation <https://zanata.ci.cloudbees.com/job/zanata-api-site/site/zanata-common-api/rest-api-docs/index.html#resources>`_ for details.

Deprecated APIs are not implemented.

For further details see also the `YAML Definition File (GitHub) <https://github.com/collective/pyzanata/blob/master/src/pyzanata/restapi.yaml>`_. This file is read by the generic API runtime code and declares the API.


Contribute
----------

- Issue Tracker: https://github.com/bluedynamics/pyanata/issues
- Source Code: https://github.com/bluedynamics/pyanata


Support
-------

If you are having issues, please let me know: jens@bluedynamics.com


License
-------

The project is licensed under the GPLv2.
