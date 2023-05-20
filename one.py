#one.py

def func():
    print("FUN() IN ONE.PY")

print("TOP LEVEL IN ONE.PY")

if __name__ == '__main__':
    # RUN THE SCRIPT!
    print('ONE.PY is being run directly!')
else:
    print('ONE.PY has been imported!')