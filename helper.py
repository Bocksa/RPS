import matplotlib.pyplot as plt
from IPython import display
import os
import math

def plot(scores, mean_scores, test_time):
    plt.clf()
    plt.title(f"Training Data")
    plt.xlabel('Number of Matches')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    #plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.savefig(f"./graphs/scores.png")

def bar(data, test_time):
    plt.clf()
    plt.title("Choice Spread")
    plt.xlabel("Choices")
    plt.ylabel("Number of Occurences")
    courses = list(data.keys())
    values = list(data.values())
    plt.bar(courses, values, color ='blue', width = 0.4)
    plt.savefig(f"./graphs/moves.png")
