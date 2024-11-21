"""
Auteurs : Nassim Lattab, Mohamed Azzaoui
M2 IAD

Ce fichier contient l'implémentation de notre algorithme MinMaxEnvy que nous comparons à l'algorithme MaxNe du papier que nous avons étudié, dans le cas d'allocation sans envie locale.
"""

import copy
import itertools
import random

class Agent:
    def __init__(self, name, preference):
        """
        Constructor for an agent.

        :param name: Agent's name.
        :param preference: List of the agent's preferences.
        """
        self.name = name
        self.preference = preference
        self.allocation = None

    def append(self, x):
        """
        Adds an element to the agent's data list.

        :param x: Element to add.
        """
        self.data.append(x)


Graph = []  # Define an empty graph


def get_allocation_rank(agent, allocation):
    """
    Get the rank of an allocated item for a given agent.

    :param agent: The agent whose rank is calculated.
    :param allocation: The item allocated to the agent.
    :return: The rank of the item in the agent's preferences.
    """
    for i in range(len(agent.preference)):
        if agent.preference[i] == allocation:
            return i
    return None


def calculate_envy(agent1, agent2, n):
    """
    Calculates the envy between two agents.

    :param agent1: The first agent.
    :param agent2: The second agent.
    :param n: The total number of agents.
    :return: The envy measure.
    """
    return 1 / (n - 1) * max(0, get_allocation_rank(agent1, agent1.allocation) - get_allocation_rank(agent1, agent2.allocation))


def calculate_total_envy_for_agent(agents, agent, graph):
    """
    Calculates the total envy of a given agent towards all other agents.

    :param agents: List of agents.
    :param agent: The agent for which the total envy is calculated.
    :param graph: The graph representing the relationships between the agents.
    :return: The total envy for this agent.
    """
    total_envy = 0
    for i in range(len(graph[0])):
        if graph[agent.name][i] == 1 and i < len(agents):
            total_envy += calculate_envy(agent, agents[i], len(graph))

    return total_envy * (1 / (2 * count_edges_in_graph(graph)))


def generate_permutations(num_objects):
    """
    Generates all possible permutations of objects.

    :param num_objects: The total number of objects.
    :return: A list of all possible permutations of the objects.
    """
    objects = list(range(1, num_objects + 1))
    permutations = list(itertools.permutations(objects))
    return permutations


def calculate_factorial(n):
    """
    Calculates the factorial of a given number.

    :param n: The number to calculate the factorial of.
    :return: The factorial of n.
    """
    if n == 0 or n == 1:
        return 1
    return n * calculate_factorial(n - 1)


def calculate_expected_envy_classical_method(agents, unallocated_items, graph):
    """
    Calculates the expected envy for the classical method.

    :param agents: List of agents.
    :param unallocated_items: List of unallocated items.
    :param graph: The graph representing the agent relationships.
    :return: The item allocated to the agent according to the expected envy method.
    """
    permutations = generate_permutations(len(unallocated_items))
    final_scores = []
    for permutation in permutations:
        s = 0
        scores = []
        for j in range(len(agents) - len(unallocated_items), len(agents)):
            agents[j].allocation = unallocated_items[permutation[s] - 1]
            s = s + 1
        for l in range(len(agents)):
            scores.append(calculate_total_envy_for_agent(agents, agents[l], graph))

        final_scores.append(max(scores))

    solution = permutations[final_scores.index(min(final_scores))]
    chosen_agent = len(agents) - len(unallocated_items)
    agents[chosen_agent].allocation = unallocated_items[solution[0] - 1]
    return unallocated_items[solution[0] - 1]


def minimize_envy_in_non_paper_setting(agents, graph):
    """
    Allocates items to minimize envy in a non-paper setting.

    :param agents: List of agents.
    :param graph: The graph of relationships between agents.
    :return: List of agents with their allocated items.
    """
    unallocated_items = [i for i in range(0, len(agents))]

    for _ in range(len(agents) - 1):
        unallocated_items.remove(calculate_expected_envy_classical_method(agents, unallocated_items, graph))

    agents[len(agents) - 1].allocation = unallocated_items[0]
    return agents


def minimize_envy_in_paper_setting(agents, graph):
    """
    Allocates items to minimize envy in a paper setting.

    :param agents: List of agents.
    :param graph: The graph of relationships between agents.
    :return: List of agents with their allocated items.
    """
    unallocated_items = [i for i in range(0, len(agents))]

    for _ in range(len(agents) - 1):
        unallocated_items.remove(calculate_expected_envy_paper_method(agents, unallocated_items, graph))

    agents[len(agents) - 1].allocation = unallocated_items[0]
    return agents


def calculate_expected_envy_improved_method(agents, unallocated_items, graph):
    """
    Calculates the expected envy for the improved method.

    :param agents: List of agents.
    :param unallocated_items: List of unallocated items.
    :param graph: The graph of relationships between agents.
    :return: The item allocated to the agent in the improved method.
    """
    final_scores = []
    nat = len(agents) - len(unallocated_items)
    for i in range(len(unallocated_items)):
        scores = []
        agents[nat].allocation = unallocated_items[i]

        for j in range(nat + 1, len(agents)):
            average = 0
            for l in range(len(unallocated_items)):
                if l != i:
                    agents[j].allocation = unallocated_items[l]
                    average += calculate_total_envy_for_agent(agents[0:nat + 1], agents[j], graph)
            scores.append(average)
        scores.append(calculate_total_envy_for_agent(agents[0:nat + 1], agents[nat], graph))
        final_scores.append(scores)

    minimum = max(final_scores[0])
    idx = 0
    for i, score in enumerate(final_scores):
        if max(score) < minimum:
            idx = i
            minimum = max(score)
    agents[nat].allocation = unallocated_items[idx]
    return unallocated_items[idx]


def count_edges_in_graph(graph):
    """
    Counts the number of edges in the graph.

    :param graph: Adjacency matrix representing the graph.
    :return: The number of edges.
    """
    num_edges = 0
    for row in graph:
        num_edges += sum(row)  # Add all the "1"s in the row.
    return num_edges


def calculate_expected_envy_paper_method(agents, unallocated_items, graph):
    """
    Calculates the expected envy for the paper method.

    :param agents: List of agents.
    :param unallocated_items: List of unallocated items.
    :param graph: The graph of relationships between agents.
    :return: The item allocated to the agent in the paper method.
    """
    nat = len(agents) - len(unallocated_items)
    scores = []
    for i in range(len(unallocated_items)):
        agents[nat].allocation = unallocated_items[i]

        average = 0
        for j in range(nat + 1, len(agents)):
            for l in range(len(unallocated_items)):
                if l != i:
                    agents[j].allocation = unallocated_items[l]
                    average += calculate_total_envy_for_agent(agents[0:nat + 1], agents[j], graph)
        scores.append(average + calculate_total_envy_for_agent(agents[0:nat + 1], agents[nat], graph))

    idx = 0
    minimum = scores[0]
    for i, score in enumerate(scores):
        if score < minimum:
            idx = i
            minimum = score
    agents[nat].allocation = unallocated_items[idx]
    return unallocated_items[idx]


def calculate_final_envy_for_agent(agents, agent, graph):
    """
    Calculates the final total envy of an agent towards all other agents.

    :param agents: List of agents.
    :param agent: The agent for which the final total envy is calculated.
    :param graph: The graph of relationships between agents.
    :return: The total envy for the agent.
    """
    total_envy = 0
    for i in range(len(graph[0])):
        if graph[agent.name][i] == 1:
            total_envy += calculate_envy(agent, agents[i], len(graph))

    return total_envy


def evaluate_graph_allocation(agents, graph):
    """
    Evaluates the allocation of items in a given graph.

    :param agents: List of agents.
    :param graph: The graph of relationships between agents.
    :return: Evaluation of the item allocation.
    """
    total_envy = 0
    for i in agents:
        total_envy += calculate_final_envy_for_agent(agents, i, graph)

    return total_envy * (1 / (2 * count_edges_in_graph(graph)))


def evaluate_graph_allocation_max_envy(agents, graph):
    """
    Evaluates the allocation based on the maximum envy for an agent.

    :param agents: List of agents.
    :param graph: The graph of relationships between agents.
    :return: The maximum envy of an agent.
    """
    max_envy = 0
    for i in agents:
        max_envy = max(max_envy, calculate_final_envy_for_agent(agents, i, graph))

    return max_envy / len(graph)


def evaluate_graph_allocation_satisfaction(agents, graph):
    """
    Evaluates the number of agents who are satisfied (envy equals zero).

    :param agents: List of agents.
    :param graph: The graph of relationships between agents.
    :return: The number of satisfied agents (envy = 0).
    """
    satisfied_agents = 0
    for i in agents:
        if calculate_final_envy_for_agent(agents, i, graph) == 0:
            satisfied_agents += 1

    return satisfied_agents


def generate_graph_and_agents(num_agents, num_objects):
    """
    Generates a graph and agents with random preferences.

    :param num_agents: Number of agents.
    :param num_objects: Number of objects.
    :return: The generated graph and agents.
    """
    graph = [[random.randint(0, 1) for _ in range(num_agents)] for _ in range(num_agents)]
    for i in range(num_agents):
        graph[i][i] = 0  # An agent cannot be connected to itself.

    agents = []
    for i in range(num_agents):
        preferences = random.sample(range(num_objects), num_objects)  # Unique random list
        agents.append(Agent(i, preferences))

    return graph, agents


# Initialisation des variables pour les moyennes
mme_mean = 0
mme_max_mean = 0 
mne_mean = 0
mne_max_mean = 0
egac = 0
egac2 = 0

print("Calcul en cours ...")
for i in range(100):
    test1 = generate_graph_and_agents(4, 4) # MinMaxEnvyY Meilleur sur des petits graphs
    test2 = copy.deepcopy(test1)
    minimize_envy_in_non_paper_setting(test2[1], test2[0])
    minimize_envy_in_paper_setting(test1[1], test1[0])
    
    mme_mean += evaluate_graph_allocation(test2[1], test2[0])
    mme_max_mean += evaluate_graph_allocation_max_envy(test2[1], test2[0])
    mne_mean += evaluate_graph_allocation(test1[1], test1[0])
    mne_max_mean += evaluate_graph_allocation_max_envy(test1[1], test1[0])
    egac += evaluate_graph_allocation_satisfaction(test2[1], test2[0])
    egac2 += evaluate_graph_allocation_satisfaction(test2[1], test2[0])

print("Résultats des deux méthodes :")
print("-" * 50)
print(f"Méthode MinMaxEnvy :")
print(f"  - Moyenne : {mme_mean / 100:.4f}")
print(f"  - Max en envie : {mme_max_mean / 1000:.4f}")
print("-" * 50)
print(f"Méthode MaxNE :")
print(f"  - Moyenne : {mne_mean / 100:.4f}")
print(f"  - Max en envie : {mne_max_mean / 1000:.4f}")
