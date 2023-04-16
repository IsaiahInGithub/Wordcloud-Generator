from cx_Freeze import setup, Executable

executables = [Executable("main.py", base=None)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Wordcloud",
    options = options,
    version = 1,
    description = 'My cool wordcloud!',
    executables = executables
)