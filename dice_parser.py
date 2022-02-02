import re
import random


def get_dice_roll():
    user_input = input("Let's roll those dice!: ")
    user_input = user_input.lower()
    user_input = user_input.replace(" ", "")
    roll_list = user_input.split("+")
    return roll_list


def total_roll(roll_list):
    total = 0
    for roll in roll_list:
        total += general_roll(roll)
    return total


def explode(num, arg):
    explode_arg = re.findall(r"!.+", arg)
    roll_arg = re.findall(r"\w+!", arg)[0][:-1]
    current_roll_count = 0
    explosion_total = 0
    if not explode_arg:
        while current_roll_count < num:
            current_roll_count += 1
            explosion_total += explosion_roll(int(roll_arg), int(roll_arg)-1)
        return explosion_total
    explode_condition = explode_arg[0][1:]
    if explode_condition[0] == ">":
        while current_roll_count < num:
            current_roll_count += 1
            explosion_total += explosion_roll(int(roll_arg),
                                              int(explode_condition[1:]))
        return explosion_total


def general_roll(roll):
    split_input = roll.split("d")
    quantity = int(split_input[0])
    roll_arg = split_input[1]
    current_roll_count = 0
    roll_total = 0
    if roll_arg.isnumeric():
        while current_roll_count < quantity:
            current_roll_count += 1
            roll_total += random.randint(1, int(roll_arg))
        return roll_total
    if "!" in roll_arg:
        roll_total += explode(quantity, roll_arg)
        return roll_total
    if "r" in roll_arg:
        roll_total += reroll(quantity, roll_arg)
        return roll_total


def reroll(num, arg):
    reroll_arg = re.findall(r"r.+", arg)[0][1:]
    roll_arg = re.findall(r"\w+r", arg)[0][:-1]
    current_roll_count = 0
    reroll_total = 0
    if reroll_arg[0] == "o":
        reroll_arg = reroll_arg[2:]
        while current_roll_count < num:
            current_roll_count += 1
            reroll_total += reroll_roll(int(roll_arg), int(reroll_arg),
                                        roll_once=True)
        return reroll_total
    reroll_arg = reroll_arg[1:]
    while current_roll_count < num:
        current_roll_count += 1
        reroll_total += reroll_roll(int(roll_arg), int(reroll_arg))
    return reroll_total


def reroll_roll(sides, limit, roll_once=False):
    roll = random.randint(1, sides)
    while roll < limit:
        roll = random.randint(1, sides)
        if roll_once:
            return roll
    return roll


def explosion_roll(sides, limit):
    roll_total = random.randint(1, sides)
    if roll_total > limit:
        roll = random.randint(1, sides)
        roll_total += roll
        while roll > limit:
            roll = random.randint(1, sides)
            roll_total += roll
    return roll_total


if __name__ == "__main__":
    user_roll_list = get_dice_roll()
    print(total_roll(user_roll_list))
