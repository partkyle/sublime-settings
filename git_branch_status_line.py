# import sublime
import sublime_plugin
import commands
import os


status_tag_name = '00_git_branch'

# finds the current branch name for the dir param
def git_branch_name(dir):
    command = 'cd "%s"; git symbolic-ref HEAD 2>/dev/null' % dir
    return commands.getoutput(command).replace('refs/heads/', '')


# formats a branch display
def format_git_branch(git_branch):
    return 'git: %s' % git_branch


# Sublime EventListener that add the git branch to the
class GitBranchStatusBarCommand(sublime_plugin.EventListener):
    # When a new buffer is created
    def on_new(self, view):
        self._update_status_line(view)

    # When the a file is loaded
    def on_load(self, view):
        self._update_status_line(view)

    # When a file is modified
    # def on_modified(self, view):
    #     self._update_status_line(view)

    # When sublime takes focus
    def on_activated(self, view):
        self._update_status_line(view)

    # updates the status to the current branch
    def _update_status_line(self, view):
        working_dir = self._get_working_dir(view)
        view.erase_status(status_tag_name)
        if working_dir != None and len(working_dir) > 0:
            git_branch = git_branch_name(working_dir)
            if len(git_branch) > 0:
                view.set_status(status_tag_name, format_git_branch(git_branch))

    # If there is a file in the active view use that file's directory to
    # search for the Git root.  Otherwise, use the only folder that is
    # open.
    def _get_working_dir(self, view):
        file_name = view.file_name()
        git_dir = None
        if file_name:
            git_dir = os.path.dirname(file_name)
        elif view.window() != None and len(view.window().folders()) > 0:
            git_dir = view.window().folders()[0]
        else:
            git_dir = None

        if git_dir == None:
            return None
        elif os.path.exists(git_dir):
            return git_dir
