from __future__ import with_statement
import shutil
import os
import logging
import sys
import optparse

logging.basicConfig(level=logging.DEBUG)

#user = "rick"
user = "richardharris"
git_uri = "git://github.com/rconradharris/dotconfigs.git"

class GitRepo(object):
    def __init__(self, uri):
        self.uri = uri
        self.basename = os.path.basename(self.uri)
        self.path = os.path.join(os.path.abspath(os.getcwd()), self.basename)
    
    def clone_repo(self):
        logging.debug("cloning git repo '%s'" % self.uri)
        os.system("git clone %s %s" % (self.uri, self.basename))

    def make_path(self, path):
        return os.path.join(self.path, path)

    def __enter__(self):
        """ Activated when used in the with statement. 
            Should automatically acquire a lock to be used in the with block.
        """
        self.clone_repo()
        return self
 
    def __exit__(self, type, value, traceback):
        """ Activated at the end of the with statement.
            It automatically releases the lock if it isn't locked.
        """
        pass

def parse_args():
    parser = optparse.OptionParser("setup.py [options] <personal|work>")
    parser.add_option("-u", "--user",
                      action="store_true", dest="add_user", default=False,
                      help="add user to system")
    parser.add_option("-g", "--gitconfig",
                      action="store_true", dest="add_git_config", default=False,
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
    if len(args) < 1:
        parser.print_usage()
        sys.exit(1)
    return options, args

def make_user_path(path):
    return os.path.join(os.path.expanduser("~%s" % user), path)

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

def add_vimrc(git_repo, undo=False):
    dest = make_user_path('.vimrc')
    bak = make_user_path('.vimrc.bak')
    if undo:
        restore(bak, dest)
    else:
        backup(dest, bak, move=True)
        src = git_repo.make_path('.vimrc')
        symlink(src, dest)

options, args = None, None
if __name__ == "__main__":
    options, args = parse_args()
    with GitRepo(git_uri) as git_repo:
        if options.add_vimrc:
            add_vimrc(git_repo, undo=options.undo)
