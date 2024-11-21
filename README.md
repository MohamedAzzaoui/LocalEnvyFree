# Local Envy-Free (LEF) Allocation Project

This project implements a Local Envy-Free (LEF) allocation algorithm and compares it with the MAXNE algorithm from the referenced paper. The goal of this project is to explore how to construct LEF allocations in environments where agents' preferences are affected by social networks, and to minimize the number of agents to be removed to achieve a LEF allocation.

## Overview

Envy-Free allocations are a fundamental concept in resource allocation problems where fairness is crucial. In particular, a Local Envy-Free (LEF) allocation ensures that no agent envies another agent's allocation when considering their local surroundings or social network.

This project provides an implementation of an algorithm for constructing LEF allocations, with a specific focus on minimizing the number of agents to be removed from the allocation graph to achieve LEF. The goal is to make the allocation process as fair as possible while maintaining as many agents in the allocation as possible.

The approach is compared with the MAXNE algorithm from the paper "Envy-free allocations respecting social networks" by Bredereck et al. (2021).

## Problem Description

The main challenge in this project is to construct an allocation that respects local envy-freeness, especially when the underlying graph of agents is not conducive to a straightforward LEF solution. In such cases, we attempt to remove a minimal number of agents (or nodes) from the graph, ensuring that the remaining agents can be allocated without envy.

## Algorithm

### LEF Algorithm
The LEF algorithm implements a method that aims to:
1. Identify agents whose presence in the allocation graph creates envy.
2. Remove these agents while maintaining the fairness of the allocation.
3. Ensure that the remaining allocation is LEF and respects the social network constraints.

### MAXNE Algorithm (Comparison)
The MAXNE algorithm is used as a benchmark for comparison. It is a known algorithm for maximizing the number of non-envious allocations in similar settings. We compare the results of the LEF algorithm with those obtained by MAXNE in terms of fairness and the number of agents removed.

## Key Features
- **Graph-based Allocation**: The allocation is modeled using a graph structure where nodes represent agents and edges represent social relationships or preferences.
- **Local Envy-Free**: The allocation ensures that agents do not envy others within their local social network.
- **Algorithm Comparison**: The LEF algorithm's performance is compared to the MAXNE algorithm in terms of fairness and efficiency.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lef-allocation.git
   cd lef-allocation
   
2. Install dependencies:
If you're using Python for the implementation, make sure to install the necessary dependencies. First, navigate to the project directory and then run:
   ```bash
   pip install -r requirements.txt
   
3. Run the LEF Algorithm:
The main algorithm is implemented in implementation.py. To run the LEF algorithm, use the following command:
   ```bash
   python implementation.py

4. View Results:
Once the algorithms have run, results will typically be printed to the console.

