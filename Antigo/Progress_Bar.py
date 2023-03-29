from alive_progress import alive_bar
import time

for x in 300,400,200,0:
    with alive_bar(total=x) as bar:
        for i in range(300):
            time.sleep(0.001)
            bar()