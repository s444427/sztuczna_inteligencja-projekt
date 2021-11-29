import heapq

from src.dimensions import *


def getTotalCost(x):
    return x.totalCost


def showPath(node, goal):
    path = node.findPath(goal)
    for x in path:
        print(x.position, end=" ")
        print(x.rotation, end=" ")
        print(x.action)
    print("***")


def succesor(node):
    succesors = []
    if node.position[0] + node.rotation[0] in range(0, GSIZE) and node.position[1] + node.rotation[1] in range(0,
                                                                                                               GSIZE):
        child = Node(node.field, [node.position[0] + node.rotation[0], node.position[1] + node.rotation[1]],
                     node.rotation)
        child.action = "move"
        succesors.append(child)
    if node.rotation == [1, 0]:
        child = Node(node.field, node.position, [0, -1])
        child.action = "left"
        succesors.append(child)
        child = Node(node.field, node.position, [0, 1])
        child.action = "right"
        succesors.append(child)
    if node.rotation == [0, 1]:
        child = Node(node.field, node.position, [-1, 0])
        succesors.append(child)
        child.action = "right"
        child = Node(node.field, node.position, [1, 0])
        child.action = "left"
        succesors.append(child)
    if node.rotation == [-1, 0]:
        child = Node(node.field, node.position, [0, -1])
        succesors.append(child)
        child.action = "right"
        child = Node(node.field, node.position, [0, 1])
        child.action = "left"
        succesors.append(child)
    if node.rotation == [0, -1]:
        child = Node(node.field, node.position, [-1, 0])
        child.action = "left"
        succesors.append(child)
        child = Node(node.field, node.position, [1, 0])
        child.action = "right"
        succesors.append(child)
    return succesors


class Node:
    def __init__(self, field, position, rotation):
        self.parent = 0
        self.startCost = 0
        self.heuristic = 0
        self.totalCost = 0
        self.position = position
        self.rotation = rotation
        self.action = 0
        self.field = field

    def __lt__(self, other):
        return self.totalCost < other.totalCost

    def findPath(self, goal):
        startNode = Node(self.field, self.position, self.rotation)
        goalNode = goal

        openList = []
        closedList = []

        startNode.parent = None

        openList.append(startNode)

        while len(openList) > 0:
            openList.sort(key=getTotalCost)

            currentNode = openList.pop(0)
            closedList.append(currentNode)

            if currentNode.position == goalNode:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current)
                    current = current.parent
                return path[::-1]

            children = succesor(currentNode)

            perm = 0
            for child in children:
                for closedChild in closedList:
                    if child.position == closedChild.position and child.rotation == closedChild.rotation and child.action == closedChild.action:
                        perm = 1
                        break
                if perm == 1:
                    perm = 0
                    continue
                child.parent = currentNode
                child.startCost = currentNode.startCost + child.field[child.position[0]][child.position[1]].moveCost
                child.heuristic = abs(goal[0] - child.position[0]) + abs(goal[1] - child.position[1])
                child.totalCost = child.startCost + child.heuristic

                for openNode in openList:
                    if child.position == openNode.position and child.rotation == openNode.rotation and child.action == openNode.action and child.startCost > openNode.startCost:
                        perm = 1
                        break

                if perm == 1:
                    perm = 0
                    continue

                openList.append(child)

    def findPathToPlant(self):
        startNode = Node(self.field, self.position, self.rotation)

        openList = []
        closedList = []

        startNode.parent = None

        heapq.heappush(openList, startNode)

        while len(openList) > 0:
            currentNode = heapq.heappop(openList)

            closedList.append(currentNode)

            if currentNode.field[currentNode.position[0]][currentNode.position[1]].planted and \
                currentNode.field[currentNode.position[0]][currentNode.position[1]].field_type == "soil" and \
                    currentNode.field[currentNode.position[0]][currentNode.position[1]].hydration < 2:
                path = []
                for _ in range(currentNode.field[currentNode.position[0]][currentNode.position[1]].hydration, 4):
                    path.append("hydrate")
                path.append("fertilize")
                current = currentNode
                while current is not None:
                    path.append(current.action)
                    current = current.parent
                return path[::-1]

            children = succesor(currentNode)

            perm = 0
            for child in children:
                for closedChild in closedList:
                    if child.position == closedChild.position and child.rotation == closedChild.rotation and child.action == closedChild.action:
                        perm = 1
                        break
                if perm == 1:
                    perm = 0
                    continue
                child.parent = currentNode
                child.startCost = currentNode.startCost + child.field[child.position[0]][child.position[1]].moveCost
                child.heuristic = abs(startNode.position[0] - child.position[0]) + abs(
                    startNode.position[1] - child.position[1])
                child.totalCost = child.startCost + child.heuristic

                for openNode in openList:
                    if child.position == openNode.position and child.rotation == openNode.rotation and child.action == openNode.action and child.startCost >= openNode.startCost:
                        perm = 1
                        break

                if perm == 1:
                    perm = 0
                    continue

                heapq.heappush(openList, child)

    def findPathToPlantSpot(self, goals):
        startNode = Node(self.field, self.position, self.rotation)

        openList = []
        closedList = []

        startNode.parent = None

        heapq.heappush(openList, startNode)

        while len(openList) > 0:
            currentNode = heapq.heappop(openList)

            closedList.append(currentNode)

            if not currentNode.field[currentNode.position[0]][currentNode.position[1]].planted and \
                    goals[currentNode.position[0]][currentNode.position[1]] != "":
                path = []
                path.append("plant")
                current = currentNode
                while current is not None:
                    path.append(current.action)
                    current = current.parent
                return path[::-1]

            children = succesor(currentNode)

            perm = 0
            for child in children:
                for closedChild in closedList:
                    if child.position == closedChild.position and child.rotation == closedChild.rotation and child.action == closedChild.action:
                        perm = 1
                        break
                if perm == 1:
                    perm = 0
                    continue
                child.parent = currentNode
                child.startCost = currentNode.startCost + child.field[child.position[0]][child.position[1]].moveCost
                child.heuristic = abs(startNode.position[0] - child.position[0]) + abs(
                    startNode.position[1] - child.position[1])
                child.totalCost = child.startCost + child.heuristic

                for openNode in openList:
                    if child.position == openNode.position and child.rotation == openNode.rotation and child.action == openNode.action and child.startCost >= openNode.startCost:
                        perm = 1
                        break

                if perm == 1:
                    perm = 0
                    continue

                heapq.heappush(openList, child)
        
