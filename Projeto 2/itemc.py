import random

# I'm defining 1 as BAR, 2 as  BELL, 3 as LEMON and 4 as CHERRY

numberOfRounds = []     # Stores the number of rounds it took to go broke, for each iteration
partialMean = 0         # Accumulates the number of rounds it took to go broke, for each iteration
                        # It helps calculating the mean

for i in range(10001):

    coins = 8           # Initial coin amount
    count = 0           # Counts how many rounds it took to go broke

    while 1:
        count += 1
        coins -= 1

        firstSlot = random.randint(1, 4)
        secondSlot = random.randint(1, 4)
        thirdSlot = random.randint(1, 4)

        if (firstSlot == 1 and secondSlot == 1 and thirdSlot == 1):
            coins += 21
        elif (firstSlot == 2 and secondSlot == 2 and thirdSlot == 2):
            coins += 16
        elif (firstSlot == 3 and secondSlot == 3 and thirdSlot == 3):
            coins += 5
        elif (firstSlot == 4 and secondSlot == 4 and thirdSlot == 4):
            coins += 3
        elif (firstSlot == 4 and secondSlot == 4 and thirdSlot != 4):
            coins += 2
        elif (firstSlot == 4 and secondSlot != 4):
            coins += 1

        if(coins == 0):
            numberOfRounds.append(count)
            partialMean += count
            break

mean = partialMean / 10001
numberOfRounds.sort()
median = numberOfRounds[5000]

print("The estimated mean is " + str(mean) + " and the estimated median is " + str(median))