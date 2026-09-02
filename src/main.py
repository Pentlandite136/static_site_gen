import os
import os.path
import shutil


def recursive_copy(source: str, dest: str) -> None:

    src = source[1:] if source.startswith("/") else source # discard any leading "/"
    dst =   dest[1:] if   dest.startswith("/") else dest   # discard any leading "/"

    if not os.path.exists(src):       # nothing to copy,
        return                        # so just return;

    if os.path.exists(dst):           # old destination file tree exists,
        shutil.rmtree(dst)            # so remove it entirely;

    os.mkdir(dst)                     # always re-make dest path;
 
    fd_source_list = os.listdir(src)  # get list of file & dir names in source

    if len(fd_source_list) == 0:      # if source path is empty,
        return                        # we are done;

    for fd_source in fd_source_list:             # process a file/dir entry from the list;
        source_path = src + "/" + fd_source      # MUST build path; fd_source by itself will fail the if tests
        dest_path = dst + "/" + fd_source
        if os.path.isfile(source_path):          # a file?
            shutil.copy(source_path, dest_path)
        elif os.path.isdir(source_path):         # a dir?
            recursive_copy(source_path, dest_path)
        else:
            raise Exception("Error: {source_path} is neither file not directory")  # should never happen


def main():
    source = "static"              # my test source root dir;
    dest   = "public"              # my test destination root dir; 

    recursive_copy(source, dest)

main()