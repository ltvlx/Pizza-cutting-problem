import json
import codecs
import matplotlib.pyplot as plt


with codecs.open("convergence.json", 'r') as fin:
    data = json.load(fin)

x = data["iterations"]
y = data["efficiency"]


plt.figure(figsize=(6, 6))
plt.grid(alpha = 0.5, linestyle = '--', linewidth = 0.2, color = 'black')
plt.xlabel("Iterations")
plt.ylabel("Efficiency")

plt.plot(x, y, 'o-', markersize=2.0, markeredgewidth=1.0)

plt.savefig("convergence.png", dpi=600, bbox_inches='tight')
plt.show()