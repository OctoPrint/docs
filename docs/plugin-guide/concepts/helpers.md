---
title: Helpers
---

# Helpers {: #plugin-guide.concepts.helpers }

Helpers are methods that plugins can expose to other plugins in order to make common functionality available on the
system. They are registered with the OctoPrint plugin system through the use of the control property [`__plugin_helpers__`][plugin-guide.concepts.control-properties.plugin-helpers].

An example for providing some helper functions to the system can be found in the
bundled [Discovery Plugin][user-guide.bundled-plugins.discovery] which provides its SSDP browsing 
and Zeroconf browsing and publishing functions as helper methods.

``` python hl_lines="7 8 9 10 11 12 13" title="src/octoprint/plugins/discovery/__init__.py"
def __plugin_load__():
    plugin = DiscoveryPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_helpers__
    __plugin_helpers__ = {
        "ssdp_browse": plugin.ssdp_browse,
        "zeroconf_browse": plugin.zeroconf_browse,
        "zeroconf_register": plugin.zeroconf_register,
        "zeroconf_unregister": plugin.zeroconf_unregister,
    }
```

An example of how to use helpers can be found in the (unmaintained) [Growl Plugin](https://github.com/OctoPrint/OctoPrint-Growl).
Using [`octoprint.plugin.core.PluginManager.get_helpers`][octoprint.plugin.core.PluginManager.get_helpers] plugins can retrieve exported helper methods and call
them as (hopefully) documented.

``` python hl_lines="6 7 8 20"
def on_after_startup(self):
    host = self._settings.get(["hostname"])
    port = self._settings.getInt(["port"])
    password = self._settings.get(["password"])

    helpers = self._plugin_manager.get_helpers("discovery", "zeroconf_browse")
    if helpers and "zeroconf_browse" in helpers:
        self.zeroconf_browse = helpers["zeroconf_browse"]

    self.growl, _ = self._register_growl(host, port, password=password)

# [...]

def on_api_get(self, request):
    if not self.zeroconf_browse:
        return flask.jsonify(dict(
            browsing_enabled=False
        ))

    browse_results = self.zeroconf_browse("_gntp._tcp", block=True)
    growl_instances = [dict(name=v["name"], host=v["host"], port=v["port"]) for v in browse_results]

    return flask.jsonify(dict(
        browsing_enabled=True,
        growl_instances=growl_instances
    ))
```
