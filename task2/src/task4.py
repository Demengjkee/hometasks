#!/usr/bin/python

import operator
import re


if __name__ == "__main__":
    f = open("../resources/access.log", "r")
    count = {}
    matcher = re.compile("(\d{1,3}\.){3}\d{1,3}")
    for line in f:
        ip = line.strip().split(" ")[0]
        result = matcher.match(ip)
        if result is None:
            continue

        if ip in count.keys():
            count[ip] += 1
        else:
            count[ip] = 1
    f.close()

    sorted_count = sorted(
        count.items(),
        key=operator.itemgetter(1), reverse=True
    )

    top = [tup[0] for tup in sorted_count[:10]]
    with open("../target/top_ip", "w") as f:
        f.write(str(top) + "\n")
    print(top)
#   print(sorted_count[:10])
