# Дадена е табла 8x6, каде што се поставени човече и топка. Потребно е човечето со туркање на топката да ја доведе до голот кој е обележан со сива боја. На таблата дополнително има противници кои се обележани со сина боја. Противниците се статични и не се движат.
# Човечето може да се движи во пет насоки: up, down, right, up-right and down-right за една позиција. При движењето, доколку пред него се наоѓа топката, може да ја турне топката во насоката во која се движи. Човечето не може да се наоѓа на истото поле како топката
# или некој од противниците. Топката исто така не може да се наоѓа на поле кое е соседно со некој од противниците 
# (хоризнотално, вертикално или дијагонално) или на исто поле со некој од противниците.

# За сите тест примери големината на таблата е иста, а позицијата на човечето и топката се менуваат и се читаат од стандарден влез. Позицијата на противниците и голот е иста за сите тест примери. Ваша задача е да го имплементирате поместувањето на човечето (со тоа и туркањето на топката) во successor функцијата. Акциите се именуваат како „Move man up/down/right/up-right/down-right“ ако се поместува човечето, или како „Push ball up/down/right/up-right/down-right“ ако при поместувањето на чoвечето се турнува и топката. Дополнително, потребно е 
# да проверите дали сте стигнале до целта, односно да ја имплементирате функцијата goal_test и да проверите дали состојбата е валидна, односно да ја дополните функцијата check_valid. Треба да примените неинформирано пребарување за да најдете решение со најмал број на чекори. 


# Input
# example
# 0,1
# 1,2
# ['Move man up', 'Move man up', 'Push ball down-right', 'Move man down', 'Push ball right', 'Push ball right', 'Push ball right', 'Move man down', 'Push ball up-right', 'Push ball up-right

# Output
# no solution
# 0,1
# 0,2
# No Solution!


from pickletools import dis
from unittest import result

from searching_framework import Problem, breadth_first_graph_search #, just an example, import whatever you actually need from the searching framework
# note that your program won't work if you copy paste classes instead of import them via the above statement

# define your Problem class here
class Game(Problem):
    def __init__(self, initial,opp1,opp2,goal):
        super().__init__(initial,goal = None)
        self.opp1 = opp1
        self.opp2 = opp2
        self.goal = goal

    def goal_test(self, state):
        man, ball = state
        return ball in self.goal


    def check_valid(self, state):
        man, ball = state
        if not(0 <= man[0] < 8 and 0 <= man[1] < 6):
            return False

        if man == self.opp1 or man == self.opp2:
            return False

        
        if not (0 <= ball[0] < 8 and 0 <= ball[1] < 6):
            return False
        
        

        for x in [-1,0,1]:
            for y in [-1,0,1]:
                if (self.opp1[0] + x,self.opp1[1] + y) == ball or (self.opp2[0] + x,self.opp2[1] + y) == ball:
                    return False

        return True


    def successor(self, state):
        succ = {}
        man, ball = state

        directions = [("up",(0,1)),
                       ("down",(0,-1)),
                        ("right",(1,0)),
                         ("up-right",(1,1)),
                         ("down-right",(1,-1))]

        for name, (dx,dy) in directions:
            new_man = man[0] + dx, man[1] + dy
            new_ball = ball

            if new_man == ball:
                new_ball = ball[0] + dx, ball[1] + dy

            new_state = new_man, new_ball
            if self.check_valid(new_state):
                if ball == new_ball:
                    succ["Move man " + name] = new_state
                else:
                    succ["Push ball " + name] = new_state

        return succ

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

if __name__ == '__main__':

    man_pos = tuple(map(int, input().split(',')))
    ball_pos = tuple(map(int, input().split(',')))

    state = man_pos, ball_pos

    game = Game(state, (3,3),(5,4),((7,2),(7,3)))
    result = breadth_first_graph_search(game)

    if result:
        print(result.solution())
    else:
        print("No Solution!")

