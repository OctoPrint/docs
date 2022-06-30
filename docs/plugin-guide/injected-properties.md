---
title: Injected properties
---

# Injected Properties {: #plugin_guide.injected-properties }

OctoPrint's plugin subsystem will inject a bunch of properties into each [mixin implementation][plugin-guide.mixins].
An overview of these properties follows.

## `self._identifier` {: #plugin_guide.injected-properties.identifier }

The plugin's identifier.

## `self._plugin_name` {: #plugin_guide.injected-properties.plugin-name }

The plugin's name, as taken from either the `__plugin_name__` control property or the package info.

## `self._plugin_version` {: #plugin_guide.injected-properties.plugin-version }

The plugin's version, as taken from either the `__plugin_version__` control property or the package info.

## `self._plugin_info` {: #plugin_guide.injected-properties.plugin-info }

The [`octoprint.plugin.core.PluginInfo`][octoprint.plugin.core.PluginInfo] object associated with the plugin.

## `self._basefolder` {: #plugin_guide.injected-properties.basefolder }

The plugin's base folder where it's installed. Can be used to refer to files relative to the plugin's installation
location, e.g. included scripts, templates or assets.

## `self._datafolder` {: #plugin_guide.injected-properties.datafolder }

The plugin's additional data folder path. Can be used to store additional files needed for the plugin's operation (cache,
data files etc). Plugins should not access this property directly but instead utilize [`self.get_plugin_data_folder`][octoprint.plugin.types.OctoPrintPlugin.get_plugin_data_folder]
which will make sure the path actually does exist and if not create it before returning it.

## `self._logger` {: #plugin_guide.injected-properties.logger }

A [`logging.Logger`][logging.Logger] instance logging to the log target
`octoprint.plugin.<plugin identifier>`.

## `self._settings` {: #plugin_guide.injected-properties.settings }

The plugin's personalized settings manager, injected only into plugins that include the [`octoprint.plugin.types.SettingsPlugin`][octoprint.plugin.SettingsPlugin] mixin.
An instance of [`octoprint.plugin.PluginSettings`][octoprint.plugin.PluginSettings].

## `self._plugin_manager` {: #plugin_guide.injected-properties.plugin-manager }

OctoPrint's plugin manager object, an instance of [`octoprint.plugin.core.PluginManager`][octoprint.plugin.core.PluginManager].

## `self._printer_profile_manager` {: #plugin_guide.injected-properties.printer-profile-manager }

OctoPrint's printer profile manager, an instance of [`octoprint.printer.profile.PrinterProfileManager`][octoprint.printer.profile.PrinterProfileManager].

## `self._event_bus` {: #plugin_guide.injected-properties.event-bus }

OctoPrint's event bus, an instance of [`octoprint.events.EventManager`][octoprint.events.EventManager].

## `self._analysis_queue` {: #plugin_guide.injected-properties.analysis-queue }

OctoPrint's analysis queue for analyzing GCODEs or other files, an instance of [`octoprint.filemanager.analysis.AnalysisQueue`][octoprint.filemanager.analysis.AnalysisQueue].

## `self._slicing_manager` {: #plugin_guide.injected-properties.slicing-manager }

OctoPrint's slicing manager, an instance of [`octoprint.slicing.SlicingManager`][octoprint.slicing.SlicingManager].

## `self._file_manager` {: #plugin_guide.injected-properties.file-manager }

OctoPrint's file manager, an instance of [`octoprint.filemanager.FileManager`][octoprint.filemanager.FileManager].

## `self._printer` {: #plugin_guide.injected-properties.printer }

OctoPrint's printer management object, an instance of [`octoprint.printer.PrinterInterface`][octoprint.printer.PrinterInterface].

## `self._user_manager` {: #plugin_guide.injected-properties.user-manager }

OctoPrint's user manager, an instance of [`octoprint.access.users.UserManager`][octoprint.access.users.UserManager].

## `self._connectivity_checker` {: #plugin_guide.injected-properties.connectivity-checker }

OctoPrint's connectivity checker, an instance of [`octoprint.util.ConnectivityChecker`][octoprint.util.ConnectivityChecker].

!!! see-also "See also"

    [`octoprint.plugin.core.Plugin`][octoprint.plugin.core.Plugin] and [`octoprint.plugin.types.OctoPrintPlugin`][octoprint.plugin.types.OctoPrintPlugin]
    :   Class documentation also containing the properties shared among all mixin implementations.

    [Available Mixins][plugin-guide.mixins]
    :   Some mixin types trigger the injection of additional properties.
