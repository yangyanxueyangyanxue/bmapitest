import os
import sys


def projectInit():
    projectPath = os.path.dirname(os.path.abspath(__file__))
    print(projectPath)
    for sysPath in sys.path:
        if "site-packages" in sysPath:
            with open(sysPath + "/bmapitest.pth", 'w', encoding="utf-8") as fp:
            # with open(sysPath + "/0603bbmmapi.pth", 'w', encoding="utf-8") as fp:

                fp.write(projectPath + '\n')
            break


if __name__ == "__main__":
    projectInit()
