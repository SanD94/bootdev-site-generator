import shutil, os, sys

from convert import generate_blog

def copy_files(src: str = "static", dst: str = "docs"):
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




def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    copy_files()
    generate_blog(basepath = basepath)

if __name__ == "__main__":
    main()
