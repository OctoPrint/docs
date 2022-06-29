# Plugin Development Guide {: #plugin-guide }

OctoPrint's plugins are [Python Packages](https://docs.python.org/3/tutorial/modules.html#packages) which in their
top-level module define a bunch of [control properties][plugin-guide.control-properties] defining
metadata (like name, version etc of the plugin) as well as information on how to initialize the plugin and into what
parts of the system the plugin will actually plug in to perform its job.

There are three types of ways a plugin might attach itself to the system, through so called
[mixin][plugin-guide.mixins] implementations, by attaching itself to specified
[hooks][plugin-guide.hooks], by offering [helper][plugin-guide.helpers] functionality to be
used by other plugins or by providing [settings overlays][plugin-guide.control-properties.plugin_settings_overlay].

Plugin mixin implementations will get a bunch of [properties injected][plugin-guide.injected-properties]
by OctoPrint plugin system to help them work.
