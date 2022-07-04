from functools import cmp_to_key   

# Eine Beschreibung des Initialzustands
start_state =[2,8,3,1,6,4,7,0,5]

# Eine Zielbeschreibung
goal_state = [1,2,3,8,0,4,7,6,5]

# Eine Menge von Operatoren (0 nach oben, unten, links oder rechts schieben)
def move_up( state ):
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [0, 1, 2]:
		temp = new_state[index - 3]
		new_state[index - 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def move_down( state ):
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [6, 7, 8]:
		temp = new_state[index + 3]
		new_state[index + 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def move_left( state ):
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [0, 3, 6]:
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def move_right( state ):
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [2, 5, 8]:
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None


# Node Klasse erstellen
class Node:
	def __init__( self, state, parent, operator, depth, cost ):

		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth
		self.cost = cost
		self.f_cost = 0
       
	def getState(self):
		return self.state

	def getDepth(self):
		return self.depth
		
	def getParent(self):
		return self.parent
		
	def getMoves(self):
		return self.operator
		
	def getCost(self):
		return self.cost

	#Lösungsweg von Würzel (bzw. Root)
	def pathFromStart(self):
		stateList = []
		movesList = []
		currNode = self
		while currNode.getMoves() is not None:
			stateList.append(currNode.getState())
			movesList.append(currNode.getMoves())
			currNode = currNode.parent
		movesList.reverse()
		stateList.reverse()
		for state in stateList:
			display_board(state)
		return movesList

# Node erstellen
def create_node( state, parent, operator, depth, cost ):
	return Node( state, parent, operator, depth, cost )

def expand_node( node ):
	expanded_nodes = []
	expanded_nodes.append( create_node( move_up( node.state ), node, "oben", node.depth + 1, 0 ) )
	expanded_nodes.append( create_node( move_down( node.state ), node, "unten", node.depth + 1, 0 ) )
	expanded_nodes.append( create_node( move_left( node.state ), node, "links", node.depth + 1, 0 ) )
	expanded_nodes.append( create_node( move_right( node.state), node, "rechts", node.depth + 1, 0 ) )
	expanded_nodes = [node for node in expanded_nodes if node.state != None]
	return expanded_nodes

 
# Such-Algorithmus mit Breitensuche( bfs ), Tiefensuche( dfs ), A* ( a_star )
def search( start, goal, strategy ):
	if strategy =="bfs" or strategy =="dfs" or strategy =="a_star":
		nodes = []
		nodes.append( create_node( start, None, None, 0, 0 ) )
		count=0
		explored = []
		while nodes:
			if strategy =="a_star":
				nodes.sort(key=cmp_to_key(cmp))
			node = nodes.pop(0)
			count+=1
			print ("Zustand prüfen", node.state, " mit folgnden Verschiebung: ", node.operator)
			explored.append(node.getState())
			if node.state==goal:
				print ("Fertig !!!")
				print ("Anzahl der besuchten Nodes",count)
				print ("Lösungsweg wird grafisch wie folgt gezeigt =>")
				return node.pathFromStart()
			else:
				expanded_nodes = expand_node( node )
				for item in expanded_nodes:
					state = item.getState()
					if state not in explored and (strategy =="bfs" or strategy =="a_star"):
						nodes.append(item)
					elif state not in explored and strategy =="dfs":
						nodes.insert(0, item)
	else:
		print("Suchstrategie ist nicht enthalten bzw. nicht implementiert")

#Sortierverfahren
def cmp( x, y ):
	# Für 1. Heuristik (h1): Anzahl Kacheln falsch
	#return f1(x) - f1(y)
	
	# Für 2. Heuristik (h2): Entfernung Kacheln von Zielposition
	return f2(x) - f2(y)

def f2(node):
	#f2(s) = g(s) + h(s)
	return node.depth + h2(node.state)

def f1(node):
	#f1(s) = g(s) + h(s)
	return node.depth + h1( node.state, goal_state )

# 1. Heuristik (h1): Anzahl Kacheln falsch
def h1( state, goal ):
	cost = 0
	for i in range( len( state ) ):
		if state[i] != goal[i]:
			cost += 1
	return cost 


def getFinalPosition(state):
	temp=[([0] * 2) for j in range(len(state))]
	i=0
	for i in range(len(state)):
		index = state.index(i)
		if(index==0):
			temp[i]=(0,0)
		elif(index==1):
			temp[i]=(1,0)
		elif(index==2):
			temp[i]=(2,0)
		elif(index==3):
			temp[i]=(0,1)
		elif(index==4):
			temp[i]=(1,1)
		elif(index==5):
			temp[i]=(2,1)
		elif(index==6):
			temp[i]=(0,2)
		elif(index==7):
			temp[i]=(1,2)
		elif(index==8):
			temp[i]=(2,2)
	
	return temp
	
# 2. Heuristik (h2): Entfernung Kacheln von Zielposition
finalposition =  getFinalPosition(goal_state)
def h2(state):	
	cost = 0
	temp= board_state(state)
	for y in range(3):
		for x in range(3):
			t = temp[y][x]
			xf, yf = finalposition[t]
			cost += abs(xf - x) + abs(yf - y)
	return cost


#Aktuelle Werte (Zahlen) in Temp speichern
def board_state(state):
	i=0
	temp=[([0] * 3) for j in range(3)]
	for row in range(3):
         for col in range(3):
            temp[row][col] = state[i]
            i+=1
	return temp

# Nur um zu verdeutlichen (Die Lösungswege grafisch zeigen) (Aber nicht zwingend wichtig)
def display_board( state ):
	print ("-------------")
	print ("| %i | %i | %i |" % (state[0], state[1], state[2]))
	print ("-------------")
	print ("| %i | %i | %i |" % (state[3], state[4], state[5]))
	print ("-------------")
	print ("| %i | %i | %i |" % (state[6], state[7], state[8]))
	print ("-------------")
	

# Main method
def main():
	# mögliche Optionen zur Auswahl => Breitensuche( bfs ), Tiefensuche( dfs ), A* ( a_star )
	result = search( start_state, goal_state, "a_star")
	if result == None:	
		print ("Es gibt keine Lösung")
	elif result == [None]: 
		print ("Startzustand ist gleich der Zielzustand")
	else:
	    print (result)
	    print (len(result), " Verschiebungen")

# um die main-Methode direkt auszuführen, wenn das Program startet
if __name__ == "__main__":
	main()