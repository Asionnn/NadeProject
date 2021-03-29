import cx_Freeze

executables = [cx_Freeze.Executable("Main2.py")]

cx_Freeze.setup(
    name="SuRT Clone",
    options={"build_exe":{"packages":["pygame"], "include_files":[]}},
    description="SuRT Clone - Gray BG with Black Circles",
    executables=executables
)