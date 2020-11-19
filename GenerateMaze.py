import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt


"""
  0 for space,
  1 for wall,
  2 for treasure,
  3 for start
  4 for path, Waiting algo to add 
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = sys.maxsize


class GenerateMaze():
    def __init__(self, size=10,):
        self.size = size
        self.obstacle=pow(size, 2)//12
        self.array = np.zeros([self.size, self.size])

    def GenerateObstacle(self):

        self.array[self.size//2, self.size//2] = 1
        self.array[self.size//2, self.size//2-1] = 1

        # Generate an obstacle in the middle
        for i in range(self.size//4-1, self.size//4 + 1):
            self.array[i, self.size-i] =1
            self.array[i, self.size-i-1] = 1
            self.array[self.size-i, i] = 1
            self.array[self.size-i, i-1] = 1

        for i in range(self.obstacle-1):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.array[x, y] = 1

            if (np.random.rand() > 0.5): # Random boolean
                for l in range(self.size//10):
                    if y + l >= self.size:
                        self.array[x, self.size-1] = 1
                    else:
                        self.array[x, y + l] = 1

            else:
                for l in range(self.size//4):
                    if x+l >= self.size:
                        self.array[self.size-1, y] = 1
                    else:
                        self.array[x+l, y] = 1
        #Create Box
        self.array[:, 0] = 1
        self.array[0, :] = 1
        self.array[-1, :] = 1
        self.array[:, -1] = 1

        # Generate Treasure：
        x = np.random.randint(1, self.size-1)
        y = np.random.randint(1, self.size-1)
        self.array[x, y] = 2
        self.array[1, 1] = 3

    def IsObstacle(self, i, j):
        if self.array[i, j] == 1:
            return True
        return False

    def Show(self):
        color0 = 'b'
        color1 = (1, 1, 1)
        color2 = (247 / 255, 220 / 255, 111 / 255)
        color3 = 'r' #
        color4 = 'pink'
        # rec = Rectangle(self.array, 1, 1, color='c')
        # ax.add_patch(rec)
        my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('my_camp', [color1, color2, color3, color0, color4], 6)
        cs=plt.imshow(self.array, cmap=my_cmap)

    def create(self):
        self.GenerateObstacle()


if __name__ == '__main__':
    maze = GenerateMaze(12)
    maze.create()
    maze.Show()
    plt.show()

    goal = np.where(maze.array == 2)
    goal = np.dstack((goal[0], goal[1])).squeeze()
    print(goal)
