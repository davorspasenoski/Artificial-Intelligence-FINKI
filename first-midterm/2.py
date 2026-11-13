# Даден е лавиринт NxN во кој се движи човече. Во лавиринтот има ѕидови кои се поставени на случајни позиции и истите не може да се прескокнуваат. Потребно е човечето да стигне до куќичката без притоа да удри во некој ѕид или да излезе надвор од лавиринтот. Човечето во четири насоки: горе, долу, лево и десно.
# Со еден потег човечето во десно може да се помести за две или три позиции, а во сите останати насоки може да се помести само за една позиција.

# За сите тест примери големината на таблата n се чита од стандарден влез. Потоа се чита бројот на ѕидови и позициите на секој ѕид. На крај се читаат позициите на човечето и куќичката. 
# Ваша задача е да го имплементирате движењето на човечето во successor функцијата. Акциите се именуваат како „Right X/Up/Down/Left“. Потоа имплементирајте ја хевристичката функција h.
# Потребно е проблемот да се реши во најмал број на чекори со примена на информирано пребарување.

# Test:
# TC1
# 5
# 4
# 2,0
# 3,1
# 1,2
# 2,4
# 0,0
# 4,4
# ['Up', 'Right 2', 'Up', 'Right 2', 'Up', 'Up']


from searching_framework import Problem, astar_search, breadth_first_graph_search

class Game(Problem):
    def __init__(self, initial, n, walls, goal):
        super().__init__(initial, goal)
        self.n = n
        self.walls = walls
        self.goal = goal

    def h(self, node):
        """
        Manhattan distance divided by the max move size (3) 
        to maintain admissibility for A*.
        """
        man = node.state
        return (abs(man[0] - self.goal[0]) + abs(man[1] - self.goal[1])) / 3

    def goal_test(self, state):
        return state == self.goal

    def actions(self, state):
        # successor returns a dictionary; we want the keys (action names)
        return list(self.successor(state).keys())

    def result(self, state, action):
        # Return the resulting state for the chosen action
        return self.successor(state)[action]

    def successor(self, state):
        succ = {}
        man = state
        # (Name, (dx, dy))
        directions = [
            ('Up', (0, 1)), 
            ('Down', (0, -1)), 
            ('Left', (-1, 0)), 
            ('Right 2', (2, 0)), 
            ('Right 3', (3, 0))
        ]

        for name, (dx, dy) in directions:
            new_x, new_y = man[0] + dx, man[1] + dy
            
            # 1. Check boundary and wall at destination
            if not (0 <= new_x < self.n and 0 <= new_y < self.n and (new_x, new_y) not in self.walls):
                continue
            
            # 2. Check path clearance for "jumps"
            if name == 'Right 2':
                if (man[0] + 1, man[1]) in self.walls:
                    continue
            if name == 'Right 3':
                if (man[0] + 1, man[1]) in self.walls or (man[0] + 2, man[1]) in self.walls:
                    continue

            succ[name] = (new_x, new_y)
        return succ

# Fixed the entry point check
if __name__ == '__main__':
    try:
        n = int(input("Grid size (n): "))
        m = int(input("Number of walls (m): "))
        
        walls_list = []
        for i in range(m):
            wall_coords = tuple(map(int, input(f"Wall {i+1} (x,y): ").split(',')))
            walls_list.append(wall_coords)
        walls = tuple(walls_list)
        
        man_pos = tuple(map(int, input("Start position (x,y): ").split(',')))
        goal_pos = tuple(map(int, input("Goal position (x,y): ").split(',')))

        game = Game(man_pos, n, walls, goal_pos)
        
        # You can switch between breadth_first_graph_search and astar_search here
        result = breadth_first_graph_search(game)

        if result:
            print("\nPath found:", result.solution())
        else:
            print("\nNo Solution!")
            
    except ValueError:
        print("Invalid input format. Please use integers and x,y format.")
