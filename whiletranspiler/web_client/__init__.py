from .flask_app import app
from .socket import (
    sio,
    socket_action,
    triggers as socket_triggers,
)
import socketio
import os
import flask

app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

class PluginData:
    head_block = []
    windows = []

    @classmethod
    def load_static(cls, plugin, attribute, tag):
        settings = plugin.PLUGIN_SETTINGS.web_interface
        plugin_dir = os.path.dirname(os.path.abspath(plugin.__file__))
        if hasattr(settings, attribute):
            try:
                files = (x for x in getattr(settings, attribute))
            except TypeError:
                pass
            else:
                for static_file in files:
                    path = os.path.join(plugin_dir, static_file)
                    with open(path, "r") as fb:
                        PluginData.head_block.append(
                                f"<{tag}>{fb.read()}</{tag}>")

@app.context_processor
def inject_plugin():
    head_block = flask.Markup("".join(PluginData.head_block))
    windows = [(x, flask.Markup(y)) for x, y in PluginData.windows]
    return dict(plugin_head_block=head_block, plugin_windows=windows)

def run(plugins=[]):
    plugin_main_func_names = []
    for plugin in plugins:
        if not hasattr(plugin.PLUGIN_SETTINGS, "web_interface"):
            continue

        PluginData.load_static(plugin, "css", "style")
        PluginData.load_static(plugin, "js", "script")

        settings = plugin.PLUGIN_SETTINGS.web_interface
        plugin_dir = os.path.dirname(os.path.abspath(plugin.__file__))

        if hasattr(settings, "js_main") and settings.js_main is not None:
            plugin_main_func_names.append(str(settings.js_main))

        if hasattr(settings, "windows") and settings.windows is not None:
            try:
                windows = (x for x in settings.windows)
            except TypeError:
                pass
            else:
                for name, filename in windows:
                    path = os.path.join(plugin_dir, filename)
                    with open(path, "r") as fb:
                        PluginData.windows.append((name, fb.read()))

        if hasattr(settings, "main"):
            settings.main(app, socket_action, socket_triggers)

    if len(plugin_main_func_names) > 0:
        names = ",".join(plugin_main_func_names)
        PluginData.head_block.append(
            f"<script>var plugins = [{names}];</script>"
        )

    app.run()

