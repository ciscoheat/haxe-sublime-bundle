import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_extract_var import *
    from .haxe_generate_prop import *
    from .haxe_implement_interface import *
    from .haxe_generate_field import *
    from .haxe_generate_code_helper import *
except (ValueError):  # Python 2
    from haxe_extract_var import *
    from haxe_generate_prop import *
    from haxe_implement_interface import *
    from haxe_generate_field import *
    from haxe_generate_code_helper import *


class HaxeGenerateCode(sublime_plugin.WindowCommand):

    gens = [
        HaxeExtractVar,
        HaxeGeneratePropVar,
        HaxeConvertToProp,
        HaxeGenerateGetSet,
        HaxeImplementInterface,
        HaxeGenerateField
    ]

    def complete(self):
        cmd_name = self.cmd[1]
        args = self.cmd[2]

        self.window.run_command(cmd_name, args)

    def on_select(self, index):
        if index == -1:
            return

        self.cmd = self.cmds[index]
        self.cmds = None

        sublime.set_timeout(lambda: self.complete(), 10)

    def run(self):
        win = self.window
        view = win.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)

        self.cmds = []
        for gen in HaxeGenerateCode.gens:
            self.cmds.extend(gen.poll(self.context))

        items = []
        for cmd in self.cmds:
            items.append(cmd[0])

        win.show_quick_panel(items, self.on_select)
