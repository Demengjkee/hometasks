#!/usr/bin/python 

if __name__ == "__main__":

    kf = open("../resources/keys", "r")
    vf = open("../resources/values", "r")
    for line in kf:
        keys = line.strip().split(" ")
    for line in vf:
        values = line.strip().split(" ")
    kf.close()
    vf.close()
    
    if len(values) > len(keys):
        print("More values than keys, some values will be omitted")

    dictionary = {}
    for i in range(0, len(keys)):
        try:
            dictionary[keys[i]] = values[i]
        except Exception:
            dictionary[keys[i]] = "None"

    with open ("../target/result", "w") as f:
        f.write(str(dictionary) + "\n") 
         
    
