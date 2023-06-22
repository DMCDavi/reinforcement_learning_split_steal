import random


police = open("police_1.txt","w")

for his_karma in range(11):
    for your_karma in range(11):
        for his_lastaction in ["None","split","steal"]:
            for rounds_left in range (10):
                r = random.choice([0,1])
                police.write(str(his_karma-5) + " " + str(your_karma-5) + " " + his_lastaction + 
                            " " + str(rounds_left) + " " + str(r) + "\n")
police.write("0")
police.close()