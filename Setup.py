import cx_Freeze

executables = [cx_Freeze.Executable("Main.py")]

cx_Freeze.setup(
    name="SuRT Clone",
    options={"build_exe":{"packages":["pygame", "csv"], "include_files":[]}},
    description="SuRT Clone",
    executables=executables
)