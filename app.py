#!/usr/bin/python3
import sys

def main():
    if (len(sys.argv) != 2):
        print('Usage: python3 app.py input.txt')
        exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        text = file.read()
        print(text)

# Guard preventing this script to be run more
# than once when being imported from other scripts
if __name__ == "__main__":
    main()