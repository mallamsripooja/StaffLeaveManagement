import matplotlib.pyplot as plt
import cgi
try:
    print("Content-Type:html/text")
    plt.plot([1,2,3,4])
    #plt.savefig("../../testcasefig.png")
    plt.draw()
    print(1)
except Exception as e:
    print(e)
