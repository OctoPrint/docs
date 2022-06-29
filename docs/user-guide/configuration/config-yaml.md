# Main configuration: config.yaml {: #user-guide.configuration.config-yaml }

If not specified via the command line, the main configuration file `config.yaml` for 
OctoPrint is expected in its settings folder, which unless defined differently via the 
command line is located at `~/.octoprint` on Linux, at `%APPDATA%/OctoPrint` on Windows 
and at `~/Library/Application Support/OctoPrint` on macOS. If the file is not there, you 
can just create it - it will only get created by OctoPrint once you save settings that 
deviate from the default settings.

Note that many of these settings are available from the Settings in OctoPrint 
itself. They can also be configured via config command line interface.

The configuration is a YAML file with a top-level dictionary. The keys of this dictionary
are as follows:

{{ pydantic_example("octoprint.schema.config.Config", recursive=False) }}

Their content is described in the following sections.

## accessControl {: #user-guide.configuration.config-yaml.accessControl }

{{ pydantic("octoprint.schema.config.AccessControlConfig", key="accessControl") }}

## api {: #user-guide.configuration.config-yaml.api }

{{ pydantic("octoprint.schema.config.ApiConfig", key="api") }}

## appearance {: #user-guide.configuration.config-yaml.appearance }

Using the `appearance` settings you can tweak OctoPrint's appearance a bit to better 
distinguish multiple instances/printers appearance or to modify the order and presence 
of the various UI components

{{ pydantic("octoprint.schema.config.AppearanceConfig", key="appearance") }}

!!! hint

    By modifying the `components.order` lists you may reorder OctoPrint's UI components 
    as you like.  You can also inject Plugins at another than their default location in 
    their respective container by adding the entry `plugin_<plugin identifier>` where 
    you want them to appear.

    When you override this setting, the resulting order for display will be calculated as
    follows:

      - first all components as defined by the `components.order` list
      - then all enabled core components as defined in the default order
    
    Components not contained within the default order (e.g. from third party plugins) will
    be either prepended or appended to that result, depending on the component type.
 
    Example: If you want the tab of the [Hello World Plugin]() to appear as the first tab
    in OctoPrint, you'd need to redefine `components.order.tab` by including something 
    like this in your `config.yaml`:
 
    ```yaml
    appearance:
      components:
        order:
          tab:
            - plugin_helloworld
    ```
 
    OctoPrint will then display the Hello World tab first, followed by the default tabs
    and then any other not explicitely ordered tabs.

## controls {: #user-guide.configuration.config-yaml.controls }

Use the `controls` section to add [custom controls]() to the "Controls" tab within 
OctoPrint.

### Defaults

``` yaml
controls: []
```

### Data model

`controls` is a list, with each entry in the list being a dictionary describing either a 
control or a container.

#### Control model

{{ pydantic_table("octoprint.schema.config.ControlConfig") }}

#### Container model

{{ pydantic_table("octoprint.schema.config.ContainerConfig") }}

### Example

```yaml
controls:
    - name: Fan
    layout: horizontal
    children:
        - name: Enable Fan
        command: M106 S%(speed)s
        input:
            - name: Speed (0-255)
            parameter: speed
            default: 255
            slider:
                min: 0
                max: 255
        - name: Disable Fan
        command: M107
    - name: Example for multiple commands
    children:
        - name: Move X (static)
        confirm: You are about to move the X axis right by 10mm with 3000mm/min.
        commands:
            - G91
            - G1 X10 F3000
            - G90
        - name: Move X (parametric)
        commands:
            - G91
            - G1 X%(distance)s F%(speed)s
            - G90
        input:
            - default: 10
            name: Distance
            parameter: distance
            - default: 3000
            name: Speed
            parameter: speed
    - name: Reporting
    children:
        - name: Get Position
        command: M114
        regex: "X:([-+]?[0-9.]+) Y:([-+]?[0-9.]+) Z:([-+]?[0-9.]+) E:([-+]?[0-9.]+)"
        template: "Position: X={0}, Y={1}, Z={2}, E={3}"
    - name: Fun stuff
    children:
        - name: Dance
        script: custom/dance.gco
        input:
            - name: Go arounds
            parameter: repetitions
            slider:
                max: 10
                min: 1
                step: 1
```

## devel {: #user-guide.configuration.config-yaml.devel }

The following settings are only relevant to you if you want to do OctoPrint development.

{{ pydantic("octoprint.schema.config.DevelConfig", key="devel") }}

## estimation {: #user-guide.configuration.config-yaml.estimation }

{{ pydantic("octoprint.schema.config.EstimationConfig", key="estimation") }}

## events {: #user-guide.configuration.config-yaml.events }

Use the following settings to add shell/gcode commands to be executed on certain [events]():

{{ pydantic("octoprint.schema.config.EventsConfig", key="events") }}

### Example

```yaml
events:
    subscriptions:
    # example event consumer that prints a message to the system log if the printer is disconnected
    - event: Disconnected
        command: "logger 'Printer got disconnected'"
        type: system

    # example event consumer that queries printer information from the firmware, prints a "Connected"
    # message to the LCD and homes the print head upon established printer connection, disabled though
    - event: Connected
        command: M115,M117 printer connected!,G28
        type: gcode
        enabled: False
```

!!! hint

    For debugging purposes, you can set the `debug` property on your event subscription 
    definition to `true`. That will make the event handler print a log line with your 
    subscription's command after performing all placeholder replacements.
    
    Example:

    ```yaml
    events:
      subscriptions:
        - event: Startup
          command: "logger 'OctoPrint started up'"
          type: system
          debug: true
    ```

    This will be logged in OctoPrint's logfile as

    ```
    Executing System Command: logger 'OctoPrint started up'
    ```

## feature {: #user-guide.configuration.config-yaml.feature }

{{ pydantic("octoprint.schema.config.FeatureConfig", key="feature") }}

## folder {: #user-guide.configuration.config-yaml.folder }

{{ pydantic("octoprint.schema.config.FolderConfig", key="folder") }}

## gcodeAnalysis {: #user-guide.configuration.config-yaml.gcodeAnalysis }

{{ pydantic("octoprint.schema.config.GcodeAnalysisConfig", key="gcodeAnalysis") }}

## plugins {: #user-guide.configuration.config-yaml.plugins }

The `plugins` section is where plugins can store their specific settings. It is also 
where the installed but disabled plugins are tracked.

{{ pydantic("octoprint.schema.config.PluginsConfig", key="plugins") }}

Additionally to the fields listed here, `plugins` will contain further keys for each
plugin that is storing settings itself. The keys will be the plugin's identifier.

## Example

```yaml
plugins:
  _disabled:
    - some_plugin
  _forcedCompatible:
    - some_other_plugin
  _sortingOrder:
    yet_another_plugin:
      octoprint.plugin.ordertest.callback: 1
      StartupPlugin.on_startup: 10
  virtual_printer:
    _config_version: 1
    enabled: true
```

## printerParameters {: #user-guide.configuration.config-yaml.printerParameters }

{{ pydantic("octoprint.schema.config.PrinterParametersConfig", key="printerParameters") }}

## printerProfiles {: #user-guide.configuration.config-yaml.printerProfiles }

{{ pydantic("octoprint.schema.config.PrinterProfilesConfig", key="printerProfiles") }}

## scripts {: #user-guide.configuration.config-yaml.scripts }

Default scripts and snippets. You'd usually not edit the `config.yaml` file to adjust 
those but instead create the corresponding files in `~/.octoprint/scripts/`. 
See [GCODE Scripts]().

{{ pydantic("octoprint.schema.config.ScriptsConfig", key="scripts") }}

## serial {: #user-guide.configuration.config-yaml.serial }

{{ pydantic("octoprint.schema.config.SerialConfig", key="serial") }}

## server {: #user-guide.configuration.config-yaml.server }

{{ pydantic("octoprint.schema.config.ServerConfig", key="server") }}

## slicing {: #user-guide.configuration.config-yaml.slicing }

{{ pydantic("octoprint.schema.config.SlicingConfig", key="slicing") }}

## system {: #user-guide.configuration.config-yaml.system }

{{ pydantic("octoprint.schema.config.SystemConfig", key="system") }}

## temperature {: #user-guide.configuration.config-yaml.temperature }

{{ pydantic("octoprint.schema.config.TemperatureConfig", key="temperature") }}

## terminalFilters {: #user-guide.configuration.config-yaml.terminalFilters }

Use the following settings to define a list of terminal filters to display in the terminal tab for filtering certain lines from the display terminal log.

### Defaults

{{ pydantic_example("octoprint.schema.config.DEFAULT_TERMINAL_FILTERS", key="terminal_filters") }}

### Data model

Each filter entry in the list is a dictionary with the following keys:

{{ pydantic_table("octoprint.schema.config.TerminalFilterEntry") }}

## webcam {: #user-guide.configuration.config-yaml.webcam }

{{ pydantic("octoprint.schema.config.WebcamConfig", key="webcam") }}
