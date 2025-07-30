# This script will cause a ZeroDivisionError

def cause_error():
    return 1 / 0  # Division by zero

if __name__ == "__main__":
    cause_error()