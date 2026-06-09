import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
import csv

# --- Initial Population Setup ---
nd = 3222   # Number of doves
nh = 6781   # Number of hawks

# Payoff trackers
hawks_points = 10000
doves_points = 10000

# Population history lists (recorded after warmup)
istd = []  # Dove counts over time
isth = []  # Hawk counts over time

# --- Simulation Loop ---
for i in range(90000):
    total = nd + nh

    # Randomly select two individuals from the population
    x = random.randint(1, total)
    y = random.randint(1, total)

    # Determine encounter type based on population threshold
    x_is_hawk = x > nd
    y_is_hawk = y > nd

    if x_is_hawk and y_is_hawk:
        # Hawk vs Hawk: one hawk loses and becomes a dove
        nh -= 1
        nd += 1
        hawks_points -= 50

    elif not x_is_hawk and not y_is_hawk:
        # Dove vs Dove: both share resource peacefully
        doves_points += 15

    else:
        # Hawk vs Dove: hawk wins, dove converts to hawk
        nh += 1
        nd -= 1
        hawks_points += 50

    # Record population after warmup period
    if i > 100:
        istd.append(nd)
        isth.append(nh)

# --- Results ---
total = nd + nh
print(
    f"Total population: {total}\n"
    f"Doves  — count: {nd}, points: {doves_points}, "
    f"mean %: {statistics.mean(istd) * 100 / total:.2f}%\n"
    f"Hawks  — count: {nh}, points: {hawks_points}, "
    f"mean %: {statistics.mean(isth) * 100 / total:.2f}%"
)

# --- Log Final State to CSV ---
csv_path = r"D:\hawk_dove_final.csv"
with open(csv_path, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([nd, nh, nd * 100 / total, nh * 100 / total])

# --- Smoothed Population Plot ---
window = 10  # Moving average window size (higher = smoother)
istd_smooth = np.convolve(istd, np.ones(window) / window, mode='valid')
isth_smooth = np.convolve(isth, np.ones(window) / window, mode='valid')

plt.plot(istd_smooth, label='Doves', color='blue')
plt.plot(isth_smooth, label='Hawks', color='red')
plt.axhline(y=np.mean(istd_smooth), color='blue', linestyle='--', alpha=0.5, label='Dove mean')
plt.axhline(y=np.mean(isth_smooth), color='red',  linestyle='--', alpha=0.5, label='Hawk mean')

plt.xlabel('Iterations')
plt.ylabel('Population')
plt.title('Hawk-Dove ESS Simulation')
plt.legend()
plt.show()
