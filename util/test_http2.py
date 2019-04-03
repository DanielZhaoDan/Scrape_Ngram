def read_file():
    array = []
    with open("prime.txt", "r") as ins:
        for line in ins:
            if int(line) > 70000:
                array.append(int(line))

    for i in range(1, len(array)):
        for j in range(1, len(array)):
            if array[i] * array[j] // 1000 == 6541367:
                print(array[i], array[j])


read_file()
