import os
import os.path
import shutil
import stat

def build(source_path, build_path, install_path, targets):
    print source_path, build_path, install_path, targets

    if "install" in (targets or []):
        # rez-build create the folder by default. We'll replace it by a symlink for simplicity.
        if os.path.exists(install_path) and os.path.isdir(install_path):
            os.rmdir(install_path)  # Directory should be empty, let if crash if it fail.

        #os.symlink(source_path, install_path)
        shutil.copytree(source_path, install_path)

