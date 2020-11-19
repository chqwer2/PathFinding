import numpy as np
from GenerateMaze import GenerateMaze
import matplotlib.pyplot as plt
import matplotlib

class A_star():
    def __init__(self, array):
        # point = [x, y] : value
        # start points = [1, 1]
        self.array = array
        self.open_set = np.array([[1, 1]])   #Waiting to traverse, 等待迭代
        self.close_set = np.array([] )  #Traversed
        self.g_score = np.ones(shape=np.shape(array))*999
        self.g_score[1, 1] = 0
        self.f_score = np.ones(shape=np.shape(array))*999
        goal = np.where(array == 2)
        self.goal = np.dstack((goal[0], goal[1])).squeeze()
        print("Goal is ", self.goal)

    def f_cost(self, node):
        # F function
        # F = G + H
        G = self.g_score[node[0], node[1]]
        H = self.heuristic(node)
        return G + H


    def heuristic(self, node, type=2):
        """
        heuristic function, 启发函数
        Input:
        node: list
            [x, y]
        type: int
            1. Manhattan distance 曼哈顿距离
            2. Euclidean distance 欧几里得距离
            3. Diagonal distance 对角距离
        
        """
        D = 1
        dx = abs(node[0] - self.goal[0])  # x distance to goal
        dy = abs(node[1] - self.goal[1])  # y distance to goal

        if type == 1:
            return D * (dx + dy)
        elif type == 2:
            return D * np.sqrt(dx * dx + dy * dy)
        elif type == 3:
            return D * (dx + dy) + (np.sqrt(2) - 2 * D) * min(dx, dy)


    def check_if_in_close(self, node, score):

        if node in self.close_set.tolist():   # If in close set, already walked
            # Update
            self.g_score[node[0], node[1]] = min(self.g_score[node[0], node[1]], score)
            self.f_score[node[0], node[1]] = min(self.f_score[node[0], node[1]], self.f_cost(node))

        else:  # add in open set
            self.g_score[node[0], node[1]] = score
            self.f_score[node[0], node[1]] = self.f_cost(node)
            if node not in self.open_set.tolist():
                self.open_set = np.append(self.open_set, node).reshape(-1, 2)




    def check_around_points(self, node):
        print("checking:", node)
        up = [node[0], node[1]-1]
        down = [node[0], node[1]+1]
        left = [node[0]-1, node[1]]
        right = [node[0]+1, node[1]]
        points_list = [up, down, left, right]

        for point in points_list:
            if point[0] > np.shape(self.array)[0] or point[1] > np.shape(self.array)[0]:  #outside the maze
                print(point, " outside")
                continue
            elif point[0] < 0 or point[1] < 0:
                print(point, "outside")
                continue
            elif self.array[point[0], point[1]] == 1:
                print(point, "A wall")
                continue
            self.check_if_in_close(point, self.g_score[node[0], node[1]] + 1)



    def FindPath(self):
        while 1 :
            for i, node in enumerate(self.open_set):   # Get nodes from open_set 拿出open中的点

                if self.goal.tolist() in self.close_set.tolist():
                    print("Target Found!")
                    return self.f_score
                g_score = self.g_score[node[0], node[1]]
                print("Points:",node," ,Score:", g_score)

                # add new points
                self.check_around_points(node)
                print("before deletion:", self.open_set, "wants to delete", node)
                self.open_set = np.delete(self.open_set, np.argmax(np.all(self.open_set==node, axis=1)), 0).reshape(-1, 2)
                print("after deletion:", self.open_set)
                self.close_set = np.append(self.close_set, node).reshape(-1, 2)

            if self.open_set.size == 0:
                print("End finding")
                break

    def ShowPath(self):
        print("Plot the path")
        points = self.goal.tolist()
        x = points[0]
        y = points[1]
        while x!=1 or y!=1:
            up = self.f_score[x, y-1]
            down = self.f_score[x, y+1]
            right = self.f_score[x+1, y]
            left = self.f_score[x-1, y]


            minus = np.argmin([up, down, right, left])
            if minus == 0:
                y -= 1
            elif minus == 1:
                y += 1
            elif minus == 2:
                x += 1
            elif minus == 3:
                x-=1
            self.array[x, y] = 4
        self.array[1, 1] = 3


    def drawplot(self):
        color0 = 'b'
        color1 = (1, 1, 1)
        color2 = (247 / 255, 220 / 255, 111 / 255)
        color3 = 'r'  #
        color4 = 'green'
        # rec = Rectangle(self.array, 1, 1, color='c')
        # ax.add_patch(rec)
        my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('my_camp',[color1, color3, color4, color0, color2], 6)
        cs = plt.imshow(self.array, cmap=my_cmap)




if __name__ == '__main__':
    maze = GenerateMaze(30)
    maze.create()
    array = maze.array
    maze.Show()

    print(array)
    Astar = A_star(array)
    score = Astar.FindPath()
    Astar.ShowPath()
    Astar.drawplot()
    plt.show()
