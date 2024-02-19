from tkinter import *
import random as rand
import json

root = Tk()
resX = 1000; resY = 500
canvas = Canvas(root, bg="black", height=resY, width=resX); canvas.pack()

# Définition des limites pour la génération des nœuds
x_lower_limit = 0
x_upper_limit = 200
y_lower_limit = 0
y_upper_limit = 100

map = {
    'resX': 200,
    'resY': 100,
    'cLevel': 0,
    'nodes': [],
    'seed': 35,
    'Choice': [-75, 100]
}

class node:
    def __init__(self, xy):
        self.xy = xy
        self.el = 0
        self.temp = 0         
        self.neighbors = []
        self.active = True
        
    def render(self):
        if self.el <= map['cLevel']:
            color = 'blue'
        elif self.el <= 25 and self.temp <=0:
            color = 'light grey'
        elif self.el <= 25 and self.temp <=5:
            color = 'green'
        elif self.el <= 25 and self.temp <=10:
            color = 'dark green'
        elif self.el <= 25 and self.temp <=100:
            color = 'yellow'
        else:
            color = 'white'
        a = self.xy[0]*5; b = self.xy[1]*5
        c = a + 5; d = b + 5
        canvas.create_rectangle(a,b,c,d, fill= color, outline= color)
        
    def to_dict(self):
        return {
            'xy': self.xy,
            'el': self.el,
            'temp': self.temp,
            'neighbors': [n.xy for n in self.neighbors],
            'active': self.active,
        }

def genNodes():
    for i in range(map['resX']):
        for j in range(map['resY']):
            if x_lower_limit <= i <= x_upper_limit and y_lower_limit <= j <= y_upper_limit:
                map['nodes'].append(node([i,j]))
            
print('Gen')
genNodes()

def getNeighbors():
    temp = []
    for n in map['nodes']:
        temp.append(n)
    for n1 in map['nodes']:
        temp.pop(0)
        for n2 in temp:
            if n1 != n2:
                if n1.xy[0] == n2.xy[0]:
                    if n2.xy[1] == n1.xy[1] + 1:
                        n1.neighbors.append(n2)
                elif n1.xy[1] == n2.xy[1]:
                    if n2.xy[0] == n1.xy[0] + 1:
                        n1.neighbors.append(n2)
                if len(n1.neighbors) >= 2:
                    break

print('Getting Neighbors')
getNeighbors()

def seed():
    start_node = rand.choice(map['nodes'])
    start_node.active = True

    for n in map['nodes']:
        if x_lower_limit <= n.xy[0] <= x_upper_limit and y_lower_limit <= n.xy[1] <= y_upper_limit:
            if n != start_node:
                # Ajuster la condition pour augmenter la probabilité au centre
                if rand.randint(0, 800) <= map['seed']:
                    n.el = rand.choice(map['Choice'])
                    n.temp = rand.choice(map['Choice'])

print('Seeding')
seed()

def setActive():
    for n in map['nodes']:
        n.active = True

def smoothMap():
    for n1 in map['nodes']:
        n1.active = False
        for n2 in n1.neighbors:
            if n2.active == True:
                if n1.el != n2.el:
                    if rand.randrange(0, 100) < 5:
                        a = (n1.el + n2.el)/2
                        n1.el = a
                        n2.el = a
                    elif rand.randrange(0, 100) < 5:
                        a = (n1.temp + n2.temp)/2
                        n1.temp = a
                        n2.temp = a

def raiseLand():
    for n in map['nodes']:
        if n.el > 0:
            if rand.randrange(0, 100) < 1:
                n.el += 100
def lowerSea():
    for n in map['nodes']:
        if n.el <= 0:
            if rand.randrange(0, 100) < 0:
                n.el -= 100
def raiseTemp():
    for n in map['nodes']:
        if n.el > 0:
            if rand.randrange(0, 100) < 1:
                n.temp += 10

def process1():
    setActive()
    smoothMap()
def process2():
    setActive()
    lowerSea()
    canvas.delete('all')
def process3():
    setActive()
    raiseLand()  
def process4():
    setActive()
    raiseTemp()

    
print('0')
for i in range(100):
    process1()
    process4()
print('1')
for i in range(15):
    process2()
    process3()
print('2')
for i in range(100):
    process1()

# canvas.delete('all')
# for n in map['nodes']:
#     n.render()
# canvas.update()

# mainloop()

# Convert nodes to a dictionary representation
nodes_dict = [node.to_dict() for node in map['nodes']]

# Create the final JSON structure
output_json = {
    'resX': map['resX'],
    'resY': map['resY'],
    'nodes': nodes_dict,
}

# Output to JSON file
json_stock = "./test_gen_map/test.json"
with open(json_stock, "w") as f:
    json.dump(output_json, f, indent=1)