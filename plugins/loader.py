import importlib, os

def load_plugins():
    plugins = []
    for f in os.listdir("plugins"):
        if f.endswith(".py") and f != "__init__.py":
            name = f[:-3]
            module = importlib.import_module("plugins."+name)
            plugins.append(module)
    return plugins
