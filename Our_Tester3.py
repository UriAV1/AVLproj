import os

from AVLTree import AVLTree, AVLNode
import time
import random


def first_expiriment(i):
    lst = list(range(1, 300 * (2 ** i) + 1))
    random.shuffle(lst)
    tree = AVLTree(is_avl=False)
    n = 300 * (2 ** i)
    rotations = 0
    time_in_actions = 0
    time_in_miliseconds = 0
    height_changes = 0
    start = time.time()
    for j in lst:
        x, actions, rotated, high =  tree.insert(j, str(1))
        rotations += rotated
        time_in_actions += actions
        height_changes += high
        sum_of_actions = time_in_actions + height_changes + rotations
        height = tree.get_height()


    return rotations, sum_of_actions, height_changes,height, (time.time() - start) * 1000


def avg_exprinement(i):
    rotations = 0
    time_in_actions = 0
    time_in_miliseconds = 0
    height_changes = 0
    height = 0
    for j in range(20):
        r, t, h,g, m = first_expiriment(i)
        rotations += r
        time_in_actions += t
        height_changes += h
        time_in_miliseconds += m
        height += g



    return f"n = 300 * 2^{i} = {300 * (2 ** i)}, rotations = {rotations / 20}, time_in_actions = {time_in_actions / 20}, height_changes = {height_changes / 20}, height = {height / 20}, time_in_miliseconds = {time_in_miliseconds / 20}"

with open("third.txt", "a") as f:
    for i in range(1, 11):
        print(f"Running experiment for i={i}...")
        result = avg_exprinement(i)
        f.write(result + "\n")
        f.flush()  # This ensures the text is written to the file immediately
        print(f"Done i={i}")