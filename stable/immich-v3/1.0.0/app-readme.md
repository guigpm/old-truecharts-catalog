# Immich 3

Install as a separate app with its own PostgreSQL 16 database, Redis and media
storage. The default web port is 10324. Install the catalog's Prometheus Operator
and CloudNativePG operator first. Keep PostgreSQL 16 and standalone mode, set
a strong database password, and select the CPU image unless CUDA is configured.

Use new PVCs or dedicated host paths. Existing Immich 2 databases and media
volumes require a separately planned migration before import. The
[upstream migration guide](https://immich.app/blog/v3-migration) explains the
database changes. OpenVINO is unavailable in this chart because the v3.4.2
OpenVINO image was not published.
