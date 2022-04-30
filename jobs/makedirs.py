import os.path
import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid arguments', file = sys.stderr)
        exit(1)

    dir_name = os.path.expandvars(sys.argv[1])
    os.makedirs(dir_name, exist_ok = True)
    print(f'Created directory: {dir_name}')
