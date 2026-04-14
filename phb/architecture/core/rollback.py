import shutil

class RollbackEngine:
    def backup(self, file):
        shutil.copy(file, file + ".bak")

    def restore(self, file):
        shutil.copy(file + ".bak", file)
