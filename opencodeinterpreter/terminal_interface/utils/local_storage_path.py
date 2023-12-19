import os

import appdirs

# 使用appdirs确定用户特定的配置路径
config_dir = appdirs.user_config_dir("Open Code Interpreter")


def get_storage_path(subdirectory=None):
    if subdirectory is None:
        return config_dir
    else:
        return os.path.join(config_dir, subdirectory)
