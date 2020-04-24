if __name__ == "__main__":
    input_list = sys.argv
    print(sys.path)
    try:
        command_env = input_list[1]
        cfg.change_env(command_env)
    except IndexError:
        print("<><><><>launch Test Env<><><><>")
        print('You need uses the command line with Enter text online for switch Env')
    currentPath = __file__
    pathTuple = os.path.split(currentPath)
    startDir = pathTuple[0]
    allSuite = unittest.defaultTestLoader.discover(startDir, "test_*.py", top_level_dir=None)
    runner = xmlrunner.XMLTestRunner(output='target/test-report')
    runner.run(allSuite)
