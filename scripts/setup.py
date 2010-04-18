from __future__ import with_statement
import shutil
import os
import logging
import sys
import optparse

logging.basicConfig(level=logging.DEBUG)

GIT_URI = "git://github.com/rconradharris/dotconfigs.git"
class GitRepo(object):
    def __init__(self, uri):
        self.uri = uri
        self.basename = os.path.basename(self.uri)
        self.path = os.path.join(os.path.abspath(os.getcwd()), self.basename)
    
    def clone(self):
        logging.debug("cloning git repo '%s'" % self.uri)
        os.system("git clone %s %s" % (self.uri, self.basename))

    def pull(self, remote='origin', branch='master'):
        logging.debug("pulling branch '%s' from '%s'" % (branch, remote))
        cwd = os.getcwd()
        try:
            os.chdir(self.path)
            os.system("git pull %s %s" % (remote, branch))
        finally:
            os.chdir(cwd)

    def make_path(self, *path):
        return os.path.join(self.path, *path)

    def __enter__(self):
        """ Activated when used in the with statement. 
            Should automatically acquire a lock to be used in the with block.
        """
        self.clone()
        self.pull()
        return self
 
    def __exit__(self, type, value, traceback):
        """ Activated at the end of the with statement.
            It automatically releases the lock if it isn't locked.
        """
        pass

def parse_args():
    parser = optparse.OptionParser("setup.py [options] <personal|work> " 
                                   "<user>")
    parser.add_option("-u", "--user",
                      action="store_true", dest="add_user", default=False,
                      help="add user to system")
    parser.add_option("-g", "--gitconfig",
                      action="store_true", dest="add_gitconfig", default=False,
                      help="add git config for user")
    parser.add_option("-v", "--vimrc",
                      action="store_true", dest="add_vimrc", default=False,
                      help="add vimrc for user")
    parser.add_option("-s", "--sudo-user",
                      action="store_true", dest="sudo_user", default=False,
                      help="add sudo for user")
    parser.add_option("-d", "--dry-run",
                      action="store_true", dest="dry_run", default=False,
                      help="run in dry-run mode")
    parser.add_option("-n", "--undo",
                      action="store_true", dest="undo", default=False,
                      help="reverse specified operaions")

    options, args = parser.parse_args()
    if len(args) < 2:
        parser.print_usage()
        sys.exit(1)
    return options, args

def make_user_path(path):
    return os.path.join(os.path.expanduser("~%s" % the_user), path)

def backup(path, backup_path, move=False):
    _backup_restore(path, backup_path, 'backing up', move=move)

def restore(backup_path, path, move=False):
    _backup_restore(backup_path, path, 'restoring', move=move)

def _backup_restore(src, dest, msg, move=False):
    if os.path.exists(src):
        if move:
            logging.debug("%s with move from '%s' to '%s'" %
                          (msg, src, dest))
            if not options.dry_run:
                os.rename(src, dest)
        else:
            logging.debug("%s with copy from '%s' to '%s'" %
                          (msg, src, dest))
            if not options.dry_run:
                shutil.copy(src, dest)
    else:
        logging.debug("path '%s' doesnt exist, not %s" % (src, msg))

def is_symlink_broken(path):
    return os.path.lexists(path) and not os.path.exists(path)

def symlink(src, dest):
    if is_symlink_broken(dest):
        logging.debug("symlink '%s' broken, deleting" % dest)
        if not options.dry_run:
            os.unlink(dest)

    logging.debug("symlinking '%s' to '%s'" % (src, dest))
    if not options.dry_run:
        cwd = os.getcwd()
        try:
            os.chdir(os.path.dirname(dest))
            os.symlink(src, os.path.basename(dest))
        finally:
            os.chdir(cwd)

def add_dotfile(git_repo, src_name, dest_name, undo=False):
    dest = make_user_path(dest_name)
    bak = make_user_path("%s.bak" % dest_name)
    if undo:
        restore(bak, dest)
    else:
        backup(dest, bak, move=True)
        src = git_repo.make_path('dotfiles', src_name) 
        symlink(src, dest)

def add_vimrc(git_repo, undo=False):
    return add_dotfile(git_repo, '.vimrc', '.vimrc', undo=options.undo)

def add_gitconfig(git_repo, undo=False):
    dst_name = '.gitconfig'
    src_name = '%s-%s' % (dst_name, mode)
    return add_dotfile(git_repo, src_name, dst_name, undo=options.undo)

options, args = None, None
the_user = mode = None
if __name__ == "__main__":
    options, args = parse_args()
    mode, the_user = args
    with GitRepo(GIT_URI) as git_repo:
        if options.add_vimrc:
            add_vimrc(git_repo, undo=options.undo)
        if options.add_gitconfig:
            add_gitconfig(git_repo, undo=options.undo)

