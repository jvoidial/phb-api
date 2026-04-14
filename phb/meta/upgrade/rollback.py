import shutil

class Rollback:
    def __init__(self, kernel_path):
        self.kernel_path = kernel_path

    def restore(self):
        backup = self.kernel_path + ".bak"
        shutil.copy(backup, self.kernel_path)
        print("↩ Kernel rolled back successfully")
