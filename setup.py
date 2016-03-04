import cx_Freeze

executables = [cx_Freeze.Executable("starwarsV1.py")]
cx_Freeze.setup(
    name="Outreach Game",
    options={"build_exe":{"packages":["pygame"],"include_files":
                          ["pictures/","diehund.ttf","sounds/"
                           ,"wallpaper/","ezpztext.py","Hole.py","Movement.py",
                           "ParserThread.py","Timer.py","cour.ttf"]}},
    description = "Programming Game",
    executables = executables
    )
