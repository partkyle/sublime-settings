import sublime_plugin


class UpdateExecutableCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        print view.file_name()
