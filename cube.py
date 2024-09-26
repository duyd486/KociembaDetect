
from vpython import *
import numpy as np
import random
from solve_3d_cube import *
from solve_2d_cube import *
import cv2

class Rubic_Cube():
    def __init__(self):
        self.running = True
        self.tiles = []
        self.dA = np.pi/40
        #center
        scene = canvas(width=1481, height=650, background = vector(0.77,0.69,0.88), ambiant= vector(1,1,1), light = [])
        #center ball
        sphere(pos=vector(0,0,0),size=vector(3,3,3),color=vector(0,0,0))
        # vi tri cac manh mat
        tile_pos = [[vector(-1, 1, 1.5),vector(0, 1, 1.5),vector(1, 1, 1.5),           #front
                     vector(-1, 0, 1.5),vector(0, 0, 1.5),vector(1, 0, 1.5),
                     vector(-1, -1, 1.5),vector(0, -1, 1.5),vector(1, -1, 1.5), ],
                    [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),         # right
                     vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
                     vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1), ],
                    [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),       # back
                     vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
                     vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5), ],
                    [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),          # left
                     vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
                     vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1), ],
                    [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),          # top
                     vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
                     vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1), ],
                    [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),          # bottom
                     vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
                     vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1), ],
                    ]
        colors = [vector(0,1,0),vector(1,0,0),vector(0,0,1),vector(1,0.5,0),vector(1,1,1),vector(1,1,0)]
        angle = [(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(np.pi/2,vector(1,0,0)),(np.pi/2,vector(1,0,0))]
        #sides
        for rank,side in enumerate(tile_pos):
            for vec in side:
                tile = box(pos=vec,size=vector(0.98,0.98,0.1),color=colors[rank])
                tile.rotate(angle = angle[rank][0],axis=angle[rank][1])
                self.tiles.append(tile)
        #positions
        self.positions = {'front':[],'right':[],'back':[],'left':[],'top':[],'bottom':[]}
        #variables
        self.rotate = [None,0,0]
        self.moves = []
        #my code
        self.step = 0
        self.firstCall = True
        self.values = ""
        self.re_conv = {
            "F" : "F'",
            "F'" : "F",
            "F2" : "F2",
            "R" : "R'",
            "R2" : "R2",
            "R'" : "R",
            "B" : "B'",
            "B2" : "B2",
            "B'" : "B",
            "L" : "L'",
            "L2" : "L2",
            "L'" : "L",
            "U" : "U'",
            "U2" : "U2",
            "U'" : "U",
            "D" : "D'",
            "D2" : "D2",
            "D'" : "D",
        }
        self.state = {
            'up': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'right': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'front': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'down': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'left': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'back': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ]
        }
        self.stickers = {
            'main': [
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ],
            'left': [
                [50, 280], [94, 280], [138, 280],
                [50, 324], [94, 324], [138, 324],
                [50, 368], [94, 368], [138, 368]
            ],
            'front': [
                [188, 280], [232, 280], [276, 280],
                [188, 324], [232, 324], [276, 324],
                [188, 368], [232, 368], [276, 368]
            ],
            'right': [
                [326, 280], [370, 280], [414, 280],
                [326, 324], [370, 324], [414, 324],
                [326, 368], [370, 368], [414, 368]
            ],
            'up': [
                [188, 128], [232, 128], [276, 128],
                [188, 172], [232, 172], [276, 172],
                [188, 216], [232, 216], [276, 216]
            ],
            'down': [
                [188, 434], [232, 434], [276, 434],
                [188, 478], [232, 478], [276, 478],
                [188, 522], [232, 522], [276, 522]
            ],
            'back': [
                [464, 280], [508, 280], [552, 280],
                [464, 324], [508, 324], [552, 324],
                [464, 368], [508, 368], [552, 368]
            ],
        }
        self.check_state = []
        self.solved = False
        self.speed = 30

    def reset_positions(self):
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for tile in self.tiles:
            if tile.pos.z > 0.4:
                self.positions['front'].append(tile)
            if tile.pos.x > 0.4:
                self.positions['right'].append(tile)
            if tile.pos.z < -0.4:
                self.positions['back'].append(tile)
            if tile.pos.x < -0.4:
                self.positions['left'].append(tile)
            if tile.pos.y > 0.4:
                self.positions['top'].append(tile)
            if tile.pos.y < -0.4:
                self.positions['bottom'].append(tile)
        for key in self.positions.keys():
            self.positions[key] = set(self.positions[key])
    def animations(self):
        if self.rotate[0] == 'front_counter' :
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,0,1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_counter' :
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_counter' :
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,0,-1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_counter' :
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(-1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_counter' :
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_counter' :
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,-1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'front_clock' :
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,0,1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_clock' :
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_clock' :
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,0,-1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_clock' :
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(-1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_clock' :
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_clock' :
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,-1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        if self.rotate[1] + self.dA/2 > self.rotate[2] and \
            self.rotate[1] - self.dA/2 < self.rotate[2]:
            self.rotate = [None,0,0]
            self.reset_positions()
    def rotate_front_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['front_counter',0,np.pi/2]
    def rotate_right_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['right_counter',0,np.pi/2]
    def rotate_back_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['back_counter',0,np.pi/2]
    def rotate_left_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['left_counter',0,np.pi/2]
    def rotate_top_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['top_counter',0,np.pi/2]
    def rotate_bottom_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['bottom_counter',0,np.pi/2]
    def rotate_front_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['front_clock',0,np.pi/2]
    def rotate_right_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['right_clock',0,np.pi/2]
    def rotate_back_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['back_clock',0,np.pi/2]
    def rotate_left_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['left_clock',0,np.pi/2]
    def rotate_top_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['top_clock',0,np.pi/2]
    def rotate_bottom_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['bottom_clock',0,np.pi/2]
    def move(self):
        possible_moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        if self.rotate[0] == None and len(self.moves) > 0:
            if self.moves[0] == possible_moves[0]:
                self.rotate_front_clock()
            elif self.moves[0] == possible_moves[1]:
                self.rotate_right_clock()
            elif self.moves[0] == possible_moves[2]:
                self.rotate_back_clock()
            elif self.moves[0] == possible_moves[3]:
                self.rotate_left_clock()
            elif self.moves[0] == possible_moves[4]:
                self.rotate_top_clock()
            elif self.moves[0] == possible_moves[5]:
                self.rotate_bottom_clock()
            elif self.moves[0] == possible_moves[6]:
                self.rotate_front_counter()
            elif self.moves[0] == possible_moves[7]:
                self.rotate_right_counter()
            elif self.moves[0] == possible_moves[8]:
                self.rotate_back_counter()
            elif self.moves[0] == possible_moves[9]:
                self.rotate_left_counter()
            elif self.moves[0] == possible_moves[10]:
                self.rotate_top_counter()
            elif self.moves[0] == possible_moves[11]:
                self.rotate_bottom_counter()
            self.moves.pop(0)
    def scramble(self):
        possible_moves = ["F","R","B","L","U","D","F'","R'","B'","L'","U'","D'"]
        for i in range(25):
            self.moves.append(random.choice(possible_moves))

    def solution(self):
        solve(self.tiles)
    def solve(self):
        self.speed = 300
        #gan dap an vao solve cua code ben kia
        values = solve(self.tiles)
        values = list(values.split(" "))
        #chay string dap an
        for value in values:
            lis_value = list(value)
            if lis_value[-1] == '2':
                lis_value.pop(-1)
                value = ''.join(lis_value)
                self.moves.append(value)
                self.moves.append(value)
            else:
                self.moves.append(value)
    def step_solve(self):
        self.speed = 30
        #ham khi duoc goi lan dau se tim loi giai, tu lan 2 se chi thuc hien cac buoc
        if self.firstCall:
            self.values = solve(self.tiles)
            self.values = list(self.values.split(" "))
            self.firstCall = False
        lis_value = list(self.values[self.step])
        #kiem tra neu co duoi la 2 thi quay 2 lan
        if lis_value[-1] == '2':
            lis_value.pop(-1)
            self.values[self.step] = ''.join(lis_value)
            self.moves.append(self.values[self.step])
            self.moves.append(self.values[self.step])
        else:
            self.moves.append(self.values[self.step])
        #sang buoc tiep theo
        self.step += 1

        #khi da giai xong, reset lai cac thuoc tinh
        if self.step == len(self.values):
            self.step = 0
            self.firstCall = True

    def rubik_detect(self):
        print("Hi im rubik detect")
        print("Wait a second")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        while True:
            hsv=[]
            current_state=[]
            ret,img=cap.read()
            #img=cv2.flip(img,1)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = np.zeros(frame.shape, dtype=np.uint8)

            draw_stickers(img,self.stickers,'main')
            draw_stickers(img,self.stickers,'current')
            draw_preview_stickers(preview,self.stickers)
            fill_stickers(preview,self.stickers,self.state)
            texton_preview_stickers(preview,self.stickers)
            for i in range(9):
                hsv.append(frame[self.stickers['main'][i][1]+10][self.stickers['main'][i][0]+10])

            a=0
            for x,y in self.stickers['current']:
                color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
                cv2.rectangle(img,(x,y),(x+30,y+30),color[color_name],-1)
                a+=1
                current_state.append(color_name)

            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                break
            elif k ==ord('u'):
                self.state['up']=current_state
                self.check_state.append('u')
            elif k ==ord('r'):
                self.check_state.append('r')
                self.state['right']=current_state
            elif k ==ord('l'):
                self.check_state.append('l')
                self.state['left']=current_state
            elif k ==ord('d'):
                self.check_state.append('d')
                self.state['down']=current_state
            elif k ==ord('f'):
                self.check_state.append('f')
                self.state['front']=current_state
            elif k ==ord('b'):
                self.check_state.append('b')
                self.state['back']=current_state
            elif k == ord('\r'):
                # process(["R","R'"])
                if len(set(self.check_state))==6:
                    #Scan xong, lưu kết quả vào biến state
                    print("hi")
                    #lay cong thuc giai, dao nguoc va cho khoi rubik chay
                    try:
                        values = detect_solve(self.state)
                        values = list(values.split(" "))
                        values.reverse()
                        self.speed = 300
                        # print(values)
                        for value in values:
                            value = self.re_conv[value]
                            lis_value = list(value)
                            if lis_value[-1] == '2':
                                lis_value.pop(-1)
                                value = ''.join(lis_value)
                                self.moves.append(value)
                                self.moves.append(value)
                            else:
                                self.moves.append(value)
                        break

                    except:
                        print("rubik error, scan again, maybe wrong something idiot!")


                else:
                    #Chưa scan xong, thiếu mặt cần scan
                    print("")
                    print("left to scan:",6-len(set(self.check_state)))
            cv2.imshow('preview',preview)
            cv2.imshow('frame',img[0:500,0:500])
        cv2.destroyAllWindows()



    def control(self):
        button(bind=self.rotate_front_clock, text='F')
        button(bind=self.rotate_front_counter,text="F'")
        button(bind=self.rotate_right_clock, text='R')
        button(bind=self.rotate_right_counter, text="R'")
        button(bind=self.rotate_back_clock, text='B')
        button(bind=self.rotate_back_counter, text="B'")
        button(bind=self.rotate_left_clock, text='L')
        button(bind=self.rotate_left_counter, text="L'")
        button(bind=self.rotate_top_clock, text='U')
        button(bind=self.rotate_top_counter, text="U'")
        button(bind=self.rotate_bottom_clock, text='D')
        button(bind=self.rotate_bottom_counter, text="D'")
        button(bind=self.scramble, text='random_move')
        button(bind=self.rubik_detect, text='rubik detect')
        button(bind=self.solution, text='solution')
        button(bind=self.solve, text='solve it!')
        button(bind=self.step_solve, text='solve by step')

    def update(self):
        rate(self.speed)
        self.animations()
        self.move()
    def start(self):
        self.reset_positions()
        self.control()
        while self.running:
            self.update()