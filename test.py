import copy
import itertools
import pandas as pd
import numpy as np
import random

class Agent:
    def __init__(self,name,preference):
        self.name = name
        self.preference=preference
        self.allocation = None
    def append(self, x):
        self.data.append(x)


Graph = []
def rank(agent,allocation) :

    for i in range(len(agent.preference)) :

        if(agent.preference[i]==allocation) :

            return i
        
    return None

def envie(agent1,agent2,n):

    return 1/(n-1) * max(0,rank(agent1,agent1.allocation)-rank(agent1,agent2.allocation))

def envieOneAgent(agents,agent,graph):
     envieTotal = 0
     for i in range(len(graph[0])) :
          if graph[agent.name][i] == 1 and i<len(agents)  :
               envieTotal += envie(agent,agents[i],len(graph))
    
     

     return envieTotal*(1/(2*count_edges(graph)))
    
def generate_combinations(num_objects):
    # Créer une liste avec les indices des objets, 1, 2, ..., num_objects
    objects = list(range(1, num_objects + 1))
    
    # Générer toutes les permutations possibles des objets
    combinations = list(itertools.permutations(objects))
    
    return combinations

    
def factor(n):
     if n==0 or n==1 :
          return 1
     return n*factor(n-1)

def esperanceEnvie(agents,itemNotAlloued,graph):
    combinations = generate_combinations(len(itemNotAlloued))
    print(combinations)
    scoreFinal = []
    for i in combinations : 
        s=0
        score=[]
        print(i)
        for j in range(len(agents)-len(itemNotAlloued),len(agents)):
            agents[j].allocation=itemNotAlloued[i[s]-1]
            s=s+1
        for l in range(len(agents)) :
            score.append(envieOneAgent(agents,agents[l],graph))
        
        scoreFinal.append(max(score))

    solution=combinations[scoreFinal.index(min(scoreFinal))]
    agentChoisi = len(agents)-len(itemNotAlloued)
    print(agentChoisi)
    print(solution)
    print(solution[0])
    agents[agentChoisi].allocation = itemNotAlloued[solution[0]-1]
    print(f"il va etre suprimmé{itemNotAlloued[solution[0]-1]}")
    return itemNotAlloued[solution[0]-1]

def AllocationEnvieFreeMinimize(agents,graph):
    itemNotAlloued = [i for i in range(0,len(agents))]
    

    for i in range(len(agents)-1):
        itemNotAlloued.remove(esperanceEnvie2(agents,itemNotAlloued,graph))
       

    agents[len(agents)-1].allocation = itemNotAlloued[0]
    return agents

def AllocationEnvieFreeMinimizeProf(agents,graph):
    itemNotAlloued = [i for i in range(0,len(agents))]
    

    for i in range(len(agents)-1):
        itemNotAlloued.remove(esperanceEnvieProf(agents,itemNotAlloued,graph))
        

    agents[len(agents)-1].allocation = itemNotAlloued[0]
    return agents
def esperanceEnvie2(agents,itemNotAlloued,graph):
    scoreFinal = []
    nat = len(agents)-len(itemNotAlloued)
    for i in range(len(itemNotAlloued)):
        score = []
        agents[nat].allocation = itemNotAlloued[i]
        
        for j in range(nat+1,len(agents)):
            moyenne = 0
            for l in range(len(itemNotAlloued)):
                if l != i :
                   
                    agents[j].allocation = itemNotAlloued[l]
                    moyenne =moyenne + envieOneAgent(agents[0:nat+1],agents[j],graph)
            score.append(moyenne)
        score.append(envieOneAgent(agents[0:nat+1],agents[nat],graph))
        scoreFinal.append(score)
    minimum = max(scoreFinal[0])
    l = 0
    indice=0
    for i in scoreFinal :
        if max(i)<minimum :
                indice = l
                minimum=max(i)
        l = l+1
    agents[nat].allocation = itemNotAlloued[indice]
    return itemNotAlloued[indice]

def count_edges(graph):
    """
    Calcule le nombre d'arêtes dans le graphe.
    :param graph: Matrice d'adjacence représentant le graphe.
    :return: Nombre d'arêtes.
    """
    num_edges = 0
    for row in graph:
        num_edges += sum(row)  # Ajouter tous les "1" de la ligne.
    return num_edges

def esperanceEnvieProf(agents,itemNotAlloued,graph):
    scoreFinal = []
    nat = len(agents)-len(itemNotAlloued)
    score = []
    for i in range(len(itemNotAlloued)):
        
        agents[nat].allocation = itemNotAlloued[i]
    
        moyenne=0
        for j in range(nat+1,len(agents)):
            for l in range(len(itemNotAlloued)):
                if l != i :
                    
                    agents[j].allocation = itemNotAlloued[l]
                    moyenne = moyenne + envieOneAgent(agents[0:nat+1],agents[j],graph)
        score.append(moyenne+envieOneAgent(agents[0:nat+1],agents[nat],graph))

    print(score)   
    l = 0
    indice=0
    minimum=score[0]
    for i in score :
            if i<minimum :
                indice = l
                minimum=i
            l = l+1
    agents[nat].allocation = itemNotAlloued[indice]
    return itemNotAlloued[indice]
def envieOneAgentFinale(agents,agent,graph):
     envieTotal = 0
     for i in range(len(graph[0])) :
          if graph[agent.name][i] == 1 :
               envieTotal += envie(agent,agents[i],len(graph))


     return envieTotal

def evaluationGraphAllocation(agents,graph):
    envietotal=0
    for i in agents :
        envietotal=envietotal+envieOneAgentFinale(agents,i,graph)
    
    return envietotal*(1/(2*count_edges(graph)))

def evaluationGraphAllocationPireAgent(agents,graph):
    max=0
    for i in agents :
        if(max<envieOneAgentFinale(agents,i,graph)):
            max=envieOneAgentFinale(agents,i,graph)
    
    return max*(1/(2*count_edges(graph)))

def evaluationGraphAllocationContent(agents,graph):
    max=0
    for i in agents :
        if(envieOneAgentFinale(agents,i,graph)==0):
            max=max+1
    
    return max*(1/(2*count_edges(graph)))



graph=([0,1,1,1],[1,0,1,1],[1,1,0,1],[0,0,0,0])
test = [5,7,8,2]
del test[2]
print(test)
agents = []
agents.append(Agent(0,[0,1,2,3]))
agents.append(Agent(1,[2,1,3,0]))
agents.append(Agent(2,[1,3,2,0]))
agents.append(Agent(3,[1,2,0,3]))
print(agents[0])

AllocationEnvieFreeMinimizeProf(agents,graph)

def generate_graph_and_agents(num_agents, num_objects):
    """
    Génère un graphe aléatoire de liaisons entre agents et des préférences aléatoires pour chaque agent.
    :param num_agents: Nombre d'agents.
    :param num_objects: Nombre d'objets.
    :return: Une matrice de graphe et une liste d'agents.
    """
    # Générer le graphe d'attaque (matrice d'adjacence)
    graph = [[random.randint(0, 1) for _ in range(num_agents)] for _ in range(num_agents)]
    for i in range(num_agents):
        graph[i][i] = 0  # Un agent ne peut pas s'attaquer lui-même.

    # Générer des préférences aléatoires pour chaque agent
    agents = []
    for i in range(num_agents):
        preferences = random.sample(range(num_objects), num_objects)  # Liste aléatoire unique
        agents.append(Agent(i, preferences))

    return graph, agents
for i in agents :
    print(i.allocation)
    print(i.preference)
    print(" ------------------------ ")
print(f"la solution est {evaluationGraphAllocation(agents,graph)}")
Moyenne2=0
Moyenne1Max=0
Moyenne1=0
Moyenne2Max=0
ok2=0
ok=0
for i in range(1000):
    test1=generate_graph_and_agents(8,8)
    test2=copy.deepcopy(test1)
    AllocationEnvieFreeMinimize(test2[1],test2[0])
    AllocationEnvieFreeMinimizeProf(test1[1],test1[0])
   
    
    Moyenne1 =Moyenne1 + evaluationGraphAllocation(test2[1],test2[0])
    Moyenne1Max=Moyenne1Max+evaluationGraphAllocationPireAgent(test2[1],test2[0])
    Moyenne2 = Moyenne2 + evaluationGraphAllocation(test1[1],test1[0])
    Moyenne2Max= Moyenne2Max+evaluationGraphAllocationPireAgent(test1[1],test1[0])
    ok= ok+evaluationGraphAllocationContent(test2[1],test2[0])
    ok2= ok2+evaluationGraphAllocationContent(test2[1],test2[0])

print(f"En moyenne resultats methode crée fait {Moyenne1/1000}   comme moyenne et comme max en envie {Moyenne1Max/1000} et nombre agent heureux {ok/1000}")
print(f"En moyenne resultats methode prof fait {Moyenne2/1000}   comme moyenne et comme max en envie {Moyenne2Max/1000} et nombre agent heureux {ok2/1000}")
       
   
             
           
                       




