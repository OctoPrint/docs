---
title: Plugin concepts
---

# Plugin concepts {: #plugin-guide.concepts }

OctoPrint's plugins are [Python Packages](https://docs.python.org/3/tutorial/modules.html#packages) which in their
top-level module define a bunch of [control properties][plugin-guide.concepts.control-properties] defining
metadata (like name, version etc of the plugin) as well as information on how to initialize the plugin and into what
parts of the system the plugin will actually plug in to perform its job.

There are three types of ways a plugin might attach itself to the system, through so called
[mixin][plugin-guide.concepts.mixins] implementations, by attaching itself to specified
[hooks][plugin-guide.concepts.hooks], by offering [helper][plugin-guide.concepts.helpers] functionality to be
used by other plugins or by providing [settings overlays][plugin-guide.concepts.control-properties.plugin-settings-overlay].

Plugin mixin implementations will get a bunch of [properties injected][plugin-guide.concepts.mixins.injected-properties]
by OctoPrint's plugin subsystem to help them work.

The plugin subsystem will also manage plugin's general [lifecycle][plugin-guide.concepts.lifecycle] and
register declared [hook handlers][plugin-guide.concepts.hooks] and [helpers][plugin-guide.concepts.helpers].
