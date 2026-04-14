import subprocess

class ShellAdapter:
    def run(self, intent):
        cmd = intent.get("command")

        if not cmd:
            return {"status": "error", "reason": "no command"}

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        return {
            "status": "executed",
            "output": result.stdout,
            "error": result.stderr
        }
