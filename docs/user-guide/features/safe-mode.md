# Safe mode {: #user-guide.features.safe-mode }

[[ version_added 1.3.0 ]]

[[ version_changed 1.3.13 ]]

With the advent of support for plugins in OctoPrint, it quickly became apparent that some of the bugs
reported on OctoPrint's bug tracker were actually bugs with installed third party plugins or language
packs instead of OctoPrint itself.

To allow an easier identification of these cases, OctoPrint 1.3.0 introduced safe mode. Starting
OctoPrint in safe mode disables all plugins (and starting with 1.3.13 also all language packs) that are
not bundled with OctoPrint, allowing to easier identify most cases where a third party plugin or language
pack is the culprit of an observed issue.

Additionally, OctoPrint allows uninstalling plugins and language packs in this mode, allowing recovery
from cases where a third party addition causes the server to not start up or the web interface to not
render or function correctly anymore.

Whenever reporting an issue with OctoPrint, please always attempt to reproduce it in safe mode as well to
ensure it really is an issue in OctoPrint itself and now caused by one of your installed third party additions.

## How to start OctoPrint in safe mode {: #user-guide.features.safe-mode.start }

There exist three ways to start OctoPrint in safe mode.

### Via the "Restart OctoPrint in safe mode" system menu entry

[[ version_added 1.3.2 ]]

You can select "Restart OctoPrint in safe mode" from the "System" menu, if the "Restart 
OctoPrint" server command has been correctly configured.

<figure markdown>
  !["Restart OctoPrint in safe mode" in the "System" menu](site:images/user-guide/features/safe_mode/systemmenu.png)
  <figcaption>"Restart OctoPrint in safe mode" in the "System" menu</figcaption>
</figure>

### Via the `server.startOnceInSafeMode` config flag

You can set the flag `server.startOnceInSafeMode` in [`config.yaml`][user-guide.configuration.config-yaml]
to `true` and restart. This will make OctoPrint start up in safe mode. The flag will clear
automatically.

To set this flag you have the following options:

  * from command line run `octoprint safemode`[^octopi] (since OctoPrint 1.3.6)

  * from command line run `octoprint config set --bool server.startOnceInSafeMode true`[^octopi]

  * edit `config.yaml` manually with a text editor, locate the `server` block if it already exists or create it
    if it doesn't and add `startOnceInSafeMode: true` to it:

    ``` yaml
    server:
      startOnceInSafeMode: true
    ```

    Please also refer to the [YAML primer][user-guide.configuration.yaml-primer].

### Via the `--safe` command line flag

You can start OctoPrint in safe mode with the command line parameter `--safe`, e.g. `octoprint serve --safe`[^octopi]. 
Don't forget to shutdown OctoPrint first before doing this.

## Differences of safe mode vs normal operation mode {: #user-guide.features.safe-mode.differences }

When OctoPrint is running in safe mode the following changes to its normal operation mode apply:

  * OctoPrint will not enable any of the installed third party plugins. OctoPrint considers all plugins third
    party plugins that do not ship with OctoPrint's sources, so any plugins installed either via `pip` or
    into OctoPrint's plugin folder[^plugins].
  * OctoPrint will not enable any of the installed third party language packs. OctoPrint considers all language packs
    third party language packs that do not ship with OctoPrint's sources, so any language plugins installed
    through the language pack manager within settings and/or stored in the language pack folder[^lpack].
  * OctoPrint will still allow to uninstall third party plugins through the built-in Plugin Manager.
  * OctoPrint will still allow to disable (bundled) plugins that are still enabled.
  * OctoPrint will not allow to enable third party plugins.
  * OctoPrint will still allow to manage language packs.
  * OctoPrint's web interface will display a notification to remind you that it is running in
    safe mode.

    <figure markdown>
      ![Safe mode notification](site:images/user-guide/features/safe_mode/notification.png)
      <figcaption>Safe mode notification</figcaption>
    </figure>

[^octopi]: **OctoPi users**: For you that's `~/oprint/bin/octoprint` wherever it says just `octoprint`.
[^plugins]: `~/.octoprint/plugins` (Linux), `%APPDATA%/OctoPrint/plugins` (Windows) or
    `~/Library/Application Support/OctoPrint/plugins` (macOS)
[^lpack]: `~/.octoprint/translations` (Linux), `%APPDATA%/OctoPrint/translations` (Windows) or
    `~/Library/Application Support/OctoPrint/translations` (macOS)