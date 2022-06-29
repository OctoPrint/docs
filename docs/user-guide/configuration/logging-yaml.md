# Logging configuration: logging.yaml {: #user-guide.configuration.logging-yaml }

The logging configuration file `logging.yaml` for OctoPrint is expected in its settings 
folder, which unless defined differently on the command line is located at `~/.octoprint` 
on Linux, at `%APPDATA%/OctoPrint` on Windows and at `~/Library/Application Support/OctoPrint` 
on macOS.

You can use it to change the log levels of the individual components within OctoPrint, 
which might be necessary to help in debugging issues you are experiencing, or to change 
the configuration of the logging handlers themselves, e.g. in order to change size after 
which to rollover the `serial.log`.

!!! hint

    You can also configure individual logging levels for all components via UI by using 
    the Logging options in the Settings.

## Changing log levels {: #user-guide.configuration.logging-yaml.levels }

If you need to change the default logging level within OctoPrint, create the file with a text editor of your choice (it's usually not there). The general format is this:

``` yaml
loggers:
  <component>:
    level: <loglevel>
```

with `<component>` being the internal OctoPrint component for which to change the 
loglevel, and `<loglevel>` being the new log level to set. An example for increasing the 
log level of the events and the file management components to `DEBUG` (the highest amount 
of logging) would be this `logging.yaml`:

``` yaml
loggers:
  octoprint.events:
    level: DEBUG
  octoprint.filemanager:
    level: DEBUG

```

A list of important components for which an increase in logging might be interesting follows:

  * `octoprint.events`: the event sub system
  * `octoprint.filemanager`: the file management layer
  * `octoprint.plugin`: the plugin sub system
  * `octoprint.plugins.<plugin>`: the plugin `<plugin>` to change the log level of, 
    e.g. `octoprint.plugins.discovery` to change the log level of the 
    [Discovery Plugin]() or `octoprint.plugins.backup` to change the log level of the 
    [Backup plugin]().
  * `octoprint.slicing`: the slicing sub system

This list will be expanded as deemed necessary.

## Changing logging handlers {: #user-guide.configuration.logging-yaml.handlers }

You can also change the configuration of the logging handlers themselves, e.g. in order 
to make the `serial.log` larger for debugging long running communications or to change 
the behaviour of the `octoprint.log`.

You can find the default configurations of the `file` handler used for the 
`octoprint.log`, the `serialFile` handler used for the `serial.log` and the `console` 
handler used for the output to stdout in YAML format below:

``` yaml
handlers:
  # stdout
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
  # octoprint.log
  file:
    class: logging.handlers.TimedRotatingFileHandler
    level: DEBUG
    formatter: simple
    when: D
    backupCount: 1
    filename: /path/to/octoprints/logs/octoprint.log
  # serial.log
  serialFile:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: simple
    maxBytes: 2097152 # 2 * 1024 * 1024 = 2 MB in bytes
    filename: /path/to/octoprints/logs/serial.log
```

!!! todo
    
    This is currently not being synced up with the code and needs rework.

You can find more information on the used logging handlers in the Python documentation on
[logging.handlers](https://docs.python.org/3/library/logging.handlers.html).

## Changing logging formatters {: #user-guide.configuration.logging-yaml.formatters }

The logging formatters can be defined via `logging.yaml` as well. The `simple` formatter 
as referenced above is expressed in YAML as follows:

``` yaml
formatters:
  simple:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

!!! todo
    
    This is currently not being synced up with the code and needs rework.

The possible keys for the logging format can be found in the 
[Python documentation on LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-objects).
