import os
import os.path
import shutil
from TextNodeUtil import markdown_to_html_node, extract_title


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

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")  # notify user

    with open(from_path, "r") as src_file:      # source file containing the markdown
        src = src_file.read()

    with open(template_path, "r") as tpl_file:  # template file containing the template
        tpl = tpl_file.read()

    html_node = markdown_to_html_node(src)
    html_str = html_node.to_html()

    page_title = extract_title(src)

    html_str_with_title = tpl.replace("{{ Title }}", page_title)

    html_page = html_str_with_title.replace("{{ Content }}", html_str)

    with open(dest_path, "w") as dst_file:    # "w" erases everything in file if it exists, creates if doesn't exist
        dst_file.write(html_page)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    if not os.path.exists(dir_path_content):              # path to content not found;
        raise Exception(f'Error: directory path to content: "{dir_path_content}" does not exist')
     
    fd_list = os.listdir(dir_path_content)            # get list of files/dirs in the content directory

    for fd in fd_list:                                # process each fd entry;
        fd_path = os.path.join(dir_path_content, fd)  # pre-pend the current directory to fd name
        if os.path.isfile(fd_path):
            if fd == "index.md":

                with open(fd_path, "r") as src_file:       # source file containing the markdown
                    src = src_file.read()

                with open(template_path, "r") as tpl_file: # template file containing the template
                    tpl = tpl_file.read()

                html_node = markdown_to_html_node(src)
                html_str = html_node.to_html()

                page_title = extract_title(src)

                html_str_with_title = tpl.replace("{{ Title }}", page_title)

                html_page = html_str_with_title.replace("{{ Content }}", html_str)

                dest_path = os.path.join(dest_dir_path, "index.html")
                with open(dest_path, "w") as dst_file:    # "w" erases everything in file if it exists, creates if doesn't exist
#                    print(f"writing to {dest_path}")
                    dst_file.write(html_page)

        elif os.path.isdir(fd_path):
#           print(f"{fd_path} is a directory")
            dest_fd_path = os.path.join(dest_dir_path, fd)
#            print(f"write path: {dest_fd_path}")
##### NEED TO CREATE THE DEST DIR IF IT DOES NOT EXIST
            generate_pages_recursive(fd_path, template_path, dest_fd_path)

        else:
            raise Exception(f"Error: {fd_path} is neither file nor directory")  # should never happen

        


def main():

    source = "static"               # source dir;
    dest   = "public"               # destination dir; 
    recursive_copy(source, dest)

    from_path = "content"            
    templ_path = "template.html"
    dest_path = "public"
#    generate_page(from_path, templ_path, dest_path)

    generate_pages_recursive(from_path, templ_path, dest_path)

main()