def is_prime(num):
    if num / 2 == int(num / 2):
        return False

    for i in range(1, num, 2):
        result = num / i
        if i == 1 or i == num:
            continue
        if i > num / 2:
            break
        if result == int(result):
            return False
    return True

def is_trunc(num, mode = "right"):
    arr = []
    for i in range(0, len(str(num))):
        arr.append(str(num)[i])
        # Check to see if the number contains 0
        if arr[i] == "0":
            return False

    while len(arr) > 1:
        if is_prime(int("".join(arr))):
            if mode == "right":
                arr.pop() # For left truncatable primes
            else:
                arr.pop(0) # For right truncatable primes
        else:
            return False

    # Check to see if the last number in the array is prime
    if arr[0] == "2" or arr[0] == "3" or arr[0] == "5" or arr[0] == "7":
        return True
    else:
        return False

    print(arr)

options = [input("Truncatable type? 'left || right': \n"), input("Until? \n")]

# Simple code to write the number to a txt file
file = open(f"{options[0]}-trunc-primes.txt", "w")
n = 0
while n < int(options[1]):
    if is_trunc(n, options[0]):
        print(n)
        file.write(f"{n}, ")
    n += 1
file.close()

print(options)

# print(is_trunc(317))