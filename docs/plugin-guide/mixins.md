# Mixins {: #plugin-guide.mixins }

## General Concepts  {: #plugin-guide.mixins.general-concepts }

Plugin mixins are the heart of OctoPrint's plugin system. They are :ref:`special base classes <sec-plugins-mixins>`
which are to be subclassed and extended to add functionality to OctoPrint. Plugins declare their instances that
implement one or multiple mixins using the `__plugin_implementation__` control property. OctoPrint's plugin core
collects those from the plugins and offers methods to access them based on the mixin type, which get used at multiple
locations within OctoPrint.

Using mixins always follows the pattern of retrieving the matching implementations from the plugin subsystem, then
calling the specific mixin's methods as defined and necessary.

The following snippet taken from OctoPrint's code for example shows how all [`AssetPlugin`][octoprint.plugin.AssetPlugin]
implementations are collected and then all assets they return via their [`get_assets`][octoprint.plugin.AssetPlugin.get_assets] methods are retrieved and
merged into one big asset map (differing between javascripts and stylesheets of various types) for use during
rendition of the UI.

``` python
asset_plugins = pluginManager.get_implementations(octoprint.plugin.AssetPlugin)
for name, implementation in asset_plugins.items():
    all_assets = implementation.get_assets()

    if "js" in all_assets:
        for asset in all_assets["js"]:
            assets["js"].append(url_for('plugin_assets', name=name, filename=asset))

    if preferred_stylesheet in all_assets:
        for asset in all_assets[preferred_stylesheet]:
            assets["stylesheets"].append((preferred_stylesheet, url_for('plugin_assets', name=name, filename=asset)))
    else:
        for stylesheet in supported_stylesheets:
            if not stylesheet in all_assets:
                continue

            for asset in all_assets[stylesheet]:
                assets["stylesheets"].append((stylesheet, url_for('plugin_assets', name=name, filename=asset)))
            break
```

!!! see-also

    [The Plugin Tutorial](tutorial)
    :  Tutorial on how to write a simple OctoPrint module utilizing mixins for various types of extension.

## Execution Order  {: #plugin-guide.mixins.execution-order }

Some mixin types, such as [StartupPlugin][octoprint.plugin.types.StartupPlugin], 
[ShutdownPlugin][octoprint.plugin.types.ShutdownPlugin] and [UiPlugin][octoprint.plugin.types.UiPlugin], 
support influencing the execution order for various execution contexts by also 
implementing the [SortablePlugin][octoprint.plugin.SortablePlugin] mixin.

If a method is to be called on a plugin implementation for which a sorting context is defined (see the mixin
documentation for information on this), OctoPrint's plugin subsystem will ensure that the order in which the implementation
calls are done is as follows:

  * Plugins with a return value that is not `None` for `get_sorting_key`
    for the provided sorting context will be ordered among each other first. If the returned order number is equal for
    two or more implementations, they will be sorted first by whether they come bundled with OctoPrint or not, then by
    their identifier.
  * After that follow plugins which returned `None` (the default). They are first sorted by whether they come bundled
    with OctoPrint or not, then by their identifier.

!!! example

    Consider four plugin implementations implementing the `StartupPlugin` mixin, called
    `plugin_a`, `plugin_b`, `plugin_c` and `plugin_d`, the latter coming bundled with OctoPrint. `plugin_a`
    and `plugin_d` don't override `get_sorting_key`. `plugin_b` and `plugin_c` both 
    return `1` for the sorting context `StartupPlugin.on_startup`, `None` otherwise:
    
    ``` python title="plugin_a.py"
    import octoprint.plugin
    
    class PluginA(octoprint.plugin.StartupPlugin):
    
        def on_startup(self, *args, **kwargs):
            self._logger.info("PluginA starting up")
    
        def on_after_startup(self, *args, **kwargs):
            self._logger.info("PluginA started up")
    
    __plugin_implementation__ = PluginA()
    ```
    
    ``` python title="plugin_b.py"
    import octoprint.plugin
    
    class PluginB(octoprint.plugin.StartupPlugin):
    
        def get_sorting_key(self, context):
            if context == "StartupPlugin.on_startup":
                return 1
            return None
    
        def on_startup(self, *args, **kwargs):
            self._logger.info("PluginB starting up")
    
        def on_after_startup(self, *args, **kwargs):
            self._logger.info("PluginB started up")
    
    __plugin_implementation__ = PluginB()
    ```
        
    ``` python title="plugin_c.py"
    import octoprint.plugin
    
    class PluginC(octoprint.plugin.StartupPlugin):
    
        def get_sorting_key(self, context):
            if context == "StartupPlugin.on_startup":
                return 1
            return None
    
        def on_startup(self, *args, **kwargs):
            self._logger.info("PluginC starting up")
    
        def on_after_startup(self, *args, **kwargs):
            self._logger.info("PluginC started up")
    
    
    __plugin_implementation__ = PluginC()
    ```
    
    ``` python title="plugin_d.py"
    # in this example this is bundled with OctoPrint
    import octoprint.plugin
    
    class PluginD(octoprint.plugin.StartupPlugin):
    
        def on_startup(self, *args, **kwargs):
            self._logger.info("PluginD starting up")
    
        def on_after_startup(self, *args, **kwargs):
            self._logger.info("PluginD started up")
    
    __plugin_implementation__ = PluginD()
    ```
    
    OctoPrint will detect that `plugin_b` and `plugin_c` define a order number, and since it's identical for both,
    namely `1`, will order both plugins based first on their bundling status and then on their plugin identifier.
    
    `plugin_a` and `plugin_d` don't define a sort key and hence will be
    put after the other two, with `plugin_d` coming *before* `plugin_a` since it comes bundled with OctoPrint.
    The execution order of the `on_startup` method will hence be `plugin_b`, `plugin_c`, `plugin_d`, `plugin_a`.
    
    Now, the execution order of the `on_after_startup` method will be determined based on another sorting context,
    `StartupPlugin.on_after_startup` for which all of the plugins return `None`. Hence, the execution order of the
    `on_after_startup` method will be ordered first by bundle status, then by plugin identifier: `plugin_d`, `plugin_a`, `plugin_b`, `plugin_c`.
    
    This will result in the following messages to be generated:
    
    ```
    Plugin B starting up
    Plugin C starting up
    Plugin D starting up
    Plugin A starting up
    Plugin D started up
    Plugin A started up
    Plugin B started up
    Plugin C started up
    ```

## Injected Properties  {: #plugin-guide.mixins.injected-properties }

OctoPrint's plugin subsystem will inject a bunch of properties into each mixin implementation.
An overview of these properties can be found in the section [Injected Properties][plugin_guide.injected-properties].

!!! see-also

    [`Plugin`][octoprint.plugin.core.Plugin] and [`OctoPrintPlugin`][octoprint.plugin.types.OctoPrintPlugin]
    :   Class documentation also containing the properties shared among all mixin implementations.

## Available plugin mixins {: #plugin-guide.mixins.available-plugin-mixins }

Please note that all plugin mixins inherit from 
[`Plugin`][octoprint.plugin.core.Plugin] and 
[`OctoPrintPlugin`][octoprint.plugin.types.OctoPrintPlugin], 
which also provide attributes of interest to plugin developers.

[`AssetPlugin`][octoprint.plugin.types.AssetPlugin]
:   The AssetPlugin mixin allows plugins to define additional static assets such as 
    JavaScript or CSS files to be automatically embedded into the pages delivered by the 
    server to be used within the client sided part of the plugin.
[`BlueprintPlugin`][octoprint.plugin.types.BlueprintPlugin]
:   The `BlueprintPlugin` mixin allows plugins to define their own full fledged endpoints 
    for whatever purpose, be it a more sophisticated API than what is possible via the 
    [`SimpleApiPlugin`][octoprint.plugin.SimpleApiPlugin] or a custom web frontend.
[`EnvironmentDetectionPlugin`][octoprint.plugin.types.EnvironmentDetectionPlugin]
:   The `EnvironmentDetectionPlugin` mixin allows enrichting OctoPrint's environmental
    information collections with additional data, and to react to successfully collected
    environmental information.
[`EventHandlerPlugin`][octoprint.plugin.types.EventHandlerPlugin]
:   The `EventHandlerPlugin` mixin allows OctoPrint plugins to react to any of [OctoPrint's events][dev-guide.events].
    OctoPrint will call the `on_event` method for any event fired on its internal event bus, supplying the
    event type and the associated payload.
[`ProgressPlugin`][octoprint.plugin.types.ProgressPlugin]
:   Via the `ProgressPlugin` mixin plugins can let themselves be called upon progress in
    print jobs or slicing jobs, limited to minimally 1% steps.
[`SettingsPlugin`][octoprint.plugin.types.SettingsPlugin]
:   Including the `SettingsPlugin` mixin allows plugins to store and retrieve their own
    settings within OctoPrint's configuration.
[`ShutdownPlugin`][octoprint.plugin.types.ShutdownPlugin]
:   The `ShutdownPlugin` allows hooking into the shutdown of OctoPrint. It's usually
    used in conjunction with the [`StartupPlugin`][octoprint.plugin.types.StartupPlugin]
    mixin, to cleanly shut down additional services again that where started by the
    [`StartupPlugin`][octoprint.plugin.types.StartupPlugin] part of the plugin.
[`SimpleApiPlugin`][octoprint.plugin.types.SimpleApiPlugin]
:   Utilizing the `SimpleApiPlugin` mixin plugins may implement a simple API based around 
    one GET resource and one resource accepting JSON commands POSTed to it.
[`SlicerPlugin`][octoprint.plugin.types.SlicerPlugin]
:   Via the `SlicerPlugin` mixin plugins can add support for slicing engines to be used by 
    OctoPrint.
[`StartupPlugin`][octoprint.plugin.types.StartupPlugin]
:   The `StartupPlugin` allows hooking into the startup of OctoPrint. It can be used to 
    start up additional services on or just after the startup of the server.
[`TemplatePlugin`][octoprint.plugin.types.TemplatePlugin]
:   Using the `TemplatePlugin` mixin plugins may inject their own components into the
    OctoPrint web interface.
[`UiPlugin`][octoprint.plugin.types.UiPlugin]
:   The `UiPlugin` mixin allows plugins to completely replace the UI served by OctoPrint.
[`WizardPlugin`][octoprint.plugin.types.WizardPlugin]
:   The `WizardPlugin` mixin allows plugins to report to OctoPrint whether
    the `wizard` templates they define via the 
    [`TemplatePlugin`][octoprint.plugin.types.TemplatePlugin] should be displayed to the 
    user, what details to provide to their respective wizard frontend components and 
    what to do when the wizard is finished by the user.

For more detailed information on each of the available plugin mixins, please click on
their respective links.
