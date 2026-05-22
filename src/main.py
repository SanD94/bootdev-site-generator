import shutil, os

from convert import generate_page

def copy_files(src: str = "static", dst: str = "public"):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for dir in os.listdir(src):
        src_dir_path = os.path.join(src, dir)
        dst_dir_path = os.path.join(dst, dir)
        if os.path.isfile(src_dir_path):
            shutil.copy(src_dir_path, dst_dir_path)
        if os.path.isdir(src_dir_path):
            copy_files(src_dir_path, dst_dir_path)


def generate_index():
    generate_page("content/index.md", "template.html", "public/index.html")

def main():
    copy_files()
    generate_index()

if __name__ == "__main__":
    main()
