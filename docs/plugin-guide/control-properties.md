---
title: Control properties
---

# Control properties {: #plugin-guide.control-properties }

As already mentioned in the introduction, plugins are Python packages which provide certain pieces of metadata to tell OctoPrint's
plugin subsystem about themselves. These are simple package attributes defined in the top most package file, e.g.:

``` python
import octoprint.plugin

# ...

__plugin_name__ = "My Plugin"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
    # whatever you need to do to load your plugin, if anything at all
    pass
```

The following properties are recognized:

## `__plugin_name__` {: #plugin-guide.control-properties.plugin-name }

Name of your plugin, optional, overrides the name specified in `setup.py` if provided. If neither this property nor
a name from `setup.py` is available to the plugin subsystem, the plugin's identifier (= package name) will be
used instead.

## `__plugin_version__` {: #plugin-guide.control-properties.plugin-version }

Version of your plugin, optional, overrides the version specified in `setup.py` if provided.

## `__plugin_description__` {: #plugin-guide.control-properties.plugin-description }

Description of your plugin, optional, overrides the description specified in `setup.py` if provided.

## `__plugin_author__` {: #plugin-guide.control-properties.plugin-author }

Author of your plugin, optional, overrides the author specified in `setup.py` if provided.

## `__plugin_url__` {: #plugin-guide.control-properties.plugin-url }

URL of the webpage of your plugin, e.g. the Github repository, optional, overrides the URL specified in `setup.py` if
provided.

## `__plugin_license__` {: #plugin-guide.control-properties.plugin-license }

License of your plugin, optional, overrides the license specified in `setup.py` if provided.

## `__plugin_pythoncompat__` {: #plugin-guide.control-properties.plugin-pythoncompat }
Python compatibility string of your plugin, optional, defaults to `>=2.7,<3` if not set and thus Python 2 but no
Python 3 compatibility. This is used as a precaution against issues with some of the Python 2 only plugins
that are still out there, as OctoPrint will not even attempt to load plugins whose Python compatibility
information doesn't match its current environment.

If your plugin is compatible to Python 3 only, you should set this to `>=3.7,<4`.

If your plugin is compatible to Python 2 and Python 3, you should set this to `>=2.7,<4`.

``` python
    __plugin_pythoncompat__ = ">=3.7,<4"
```

## `__plugin_implementation__` {: #plugin-guide.control-properties.plugin-implementation }

Instance of an implementation of one or more :ref:`plugin mixins <sec-plugins-mixins>`. E.g.

``` python
    __plugin_implementation__ = MyPlugin()
```

## `__plugin_hooks__` {: #plugin-guide.control-properties.plugin-hooks }

Handlers for one or more of the various :ref:`plugin hooks <sec-plugins-hooks>`. E.g.

``` python
def handle_gcode_sent(comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    if gcode in ("M106", "M107"):
        import logging
        logging.getLogger(__name__).info("We just sent a fan command to the printer!")

__plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.sent": handle_gcode_sent
}
```

## `__plugin_check__` {: #plugin-guide.control-properties.plugin-check }

Method called upon discovery of the plugin by the plugin subsystem, should return `True` if the
plugin can be instantiated later on, `False` if there are reasons why not, e.g. if dependencies
are missing. An example:

``` python
def __plugin_check__():
    # Make sure we only run our plugin if some_dependency is available
    try:
        import some_dependency
    except ImportError:
        return False

    return True
```

## `__plugin_load__` {: #plugin-guide.control-properties.plugin-load }

Method called upon loading of the plugin by the plugin subsystem, can be used to instantiate
plugin implementations, connecting them to hooks etc. An example:

``` python
def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MyPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
```

## `__plugin_unload__` {: #plugin-guide.control-properties.plugin-unload }

Method called upon unloading of the plugin by the plugin subsystem, can be used to do any final clean ups.

## `__plugin_enable__` {: #plugin-guide.control-properties.plugin-enable }

Method called upon enabling of the plugin by the plugin subsystem. Also see [`octoprint.plugin.core.Plugin.on_plugin_enabled`][octoprint.plugin.core.Plugin.on_plugin_enabled].

## `__plugin_disable__` {: #plugin-guide.control-properties.plugin-disable }

Method called upon disabling of the plugin by the plugin subsystem. Also see [`octoprint.plugin.core.Plugin.on_plugin_disabled`][octoprint.plugin.core.Plugin.on_plugin_disabled].

## `__plugin_settings_overlay__` {: #plugin-guide.control-properties.plugin-settings-overlay }

An optional `dict` providing an overlay over the application's default settings. Plugins can use that to modify the
**default** settings of OctoPrint and its plugins that apply when there's no different configuration present in [`config.yaml`][user-guide.configuration.config-yaml]. Note that `config.yaml`
has the final say - it is not possible to override what is in there through an overlay. Plugin authors should use this
sparingly - it's supposed to be utilized when creating specific customization of the core application that necessitate
changes in things like e.g. standard naming, UI ordering or API endpoints. Example:

``` python
__plugin_settings_overlay__ = dict(
    api=dict(
        enabled=False
    ), 
    server=dict(
        host="127.0.0.1",
        port=5001
    )
)
```
