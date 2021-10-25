class Node:
    def __init__(self, payload, neighbors={}):
        self.payload = payload
        self.neighbors = {"north": None, "east": None, "south": None, "west": None}

    @staticmethod
    def nope(thing):
        if thing is not None and thing is not "":
            return thing.payload
        else:
             return "None"

    def __repr__(self):
        return f"I am a node! My payload is {self.payload}, my Northern neighbor is {self.nope(self.neighbors['north'])}," \
               f"my Eastern neighbor is {self.nope(self.neighbors['east'])}, my Southern neighbor is {self.nope(self.neighbors['south'])}," \
               f"my Western neighbor is {self.nope(self.neighbors['west'])}."

class Maze:
    def __init__(self, nodes=[]):
        self.nodes = nodes

def mazemaker(mazetxt, mazeobj):
    mazerow = []
    counter = 0
    with open(mazetxt) as file:
        c = file.read(1)
        while c != '':
            if c.isalpha():
                newnode = Node(c)
                mazerow.append(newnode)
            elif c == '\n':
                wmazerow = mazerow
                for nodeid in range(len(mazerow)):
                    print(nodeid)
                    if nodeid != 0 and nodeid != (len(wmazerow) - 1):
                        print("VALID INDEX")
                        wmazerow[nodeid].neighbors["west"] = wmazerow[(nodeid - 1)]
                        wmazerow[nodeid].neighbors["east"] = wmazerow[(nodeid + 1)]
                    elif nodeid == 0:
                        wmazerow[nodeid].neighbors["west"] = None
                        wmazerow[nodeid].neighbors["east"] = mazerow[(nodeid + 1)]
                        print("We hit 0.")
                    elif nodeid == (len(wmazerow) - 1):
                        wmazerow[nodeid].neighbors["west"] = mazerow[(nodeid -1)]
                        wmazerow[nodeid].neighbors["east"] = None
                        print("We hit the end")
                    print("My western neighbor is " + Node.nope(wmazerow[nodeid].neighbors["west"]))
                    print("My eastern neighbor is " + Node.nope(wmazerow[nodeid].neighbors["east"]))
                temprow = wmazerow
                mazeobj.append(temprow)
                mazerow = []
            c = file.read(1)
        for nodeid in range(len(mazerow)):
            print(nodeid)
            if nodeid != 0 and nodeid != (len(mazerow) - 1):
                print("VALID INDEX")
                mazerow[nodeid].neighbors["west"] = mazerow[(nodeid - 1)]
                mazerow[nodeid].neighbors["east"] = mazerow[(nodeid + 1)]
            elif nodeid == 0:
                mazerow[nodeid].neighbors["west"] = None
                mazerow[nodeid].neighbors["east"] = mazerow[(nodeid + 1)]
                print("We hit 0.")
            elif nodeid == (len(wmazerow) - 1):
                mazerow[nodeid].neighbors["west"] = mazerow[(nodeid -1)]
                mazerow[nodeid].neighbors["east"] = None
                print("We hit the end")
            print("My western neighbor is " + Node.nope(mazerow[nodeid].neighbors["west"]))
            print("My eastern neighbor is " + Node.nope(mazerow[nodeid].neighbors["east"]))
        temprow = mazerow
        mazeobj.append(temprow)
    for row in range(len(mazeobj)):
        for node in range(len(mazeobj[row])):
            if row != 0 and row != len(mazeobj) - 1:
                mazeobj[row][node].neighbors["north"] = mazeobj[row-1][node]
                mazeobj[row][node].neighbors["south"] = mazeobj[row+1][node]
            elif row == 0:
                mazeobj[row][node].neighbors["north"] = None
                mazeobj[row][node].neighbors["south"] = mazeobj[row+1][node]
            elif row == len(mazeobj) - 1:
                mazeobj[row][node].neighbors["north"] = mazeobj[row-1][node] 
                mazeobj[row][node].neighbors["south"] = None
                
    return mazeobj

def pathfinder(maze):
    i = 0
    for row in maze:
        print(i)
        for node in row:
            print (f"I am number {i}" + node.__repr__())
            i+=1

if __name__ == "__main__":
    myMaze = []
    myMaze = mazemaker("XXOXX.txt", myMaze)
    pathfinder(myMaze)
    print("Done")
    print(None)