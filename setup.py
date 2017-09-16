import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="The Cave Crawler",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["lib.py","constants.py","sprites","audio","font.ttf"]}},
    executables = executables

    )