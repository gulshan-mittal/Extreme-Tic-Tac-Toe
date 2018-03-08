import random
import sys
import copy
import time

class Team58():
    
    def __init__(self):
        ''' Initialization row,colls, diagnals for winning'''
        self.max_depth = 4
        self.utility_val_mat = [[0,-1,-10,-100,-1000],[1,0,0,100,0],[10,0,0,0,0],[100,0,0,0,0],[1000,0,0,0,0]]
        self.Time_limit = 14.7 
        self.win_rows =[[[0,0],[0,1],[0,2],[0,3]],
                    [[1,0],[1,1],[1,2],[1,3]],
                    [[2,0],[2,1],[2,2],[2,3]],
                    [[3,0],[3,1],[3,2],[3,3]]
                    ]
        self.move_count = 0 
        self.symbol = None
        self.tic = 0
        self.toc = 0               
        self.win_cols =[[[0,0],[1,0],[2,0],[3,0]],
                    [[0,1],[1,1],[2,1],[3,1]],
                    [[0,2],[1,2],[2,2],[3,2]],
                    [[0,3],[1,3],[2,3],[3,3]]
                    ]
        self.count_block_win = {'p': 0,'o': 0}
        self.next_move = (0,0,0)
        self.alpha = -100000000000000.0
        self.beta = 100000000000000.0


    def MinMax(self, board, old_move, max_ply_node, flag, opponent_flag, depth, alpha, beta, best_row, best_coloumn):
        ''' Min Max with alpha beta pruning along with IDFS and goes till upto time limit'''
        if (time.time() - self.tic)> self.Time_limit:
            utility = 0
            return (utility, best_row, best_coloumn)


        if depth == self.max_depth:
            utility = self.utility_get(board, flag, opponent_flag)
            return (utility, best_row, best_coloumn)

        else:
            
            available_moves = board.find_valid_move_cells(old_move)
            random.shuffle(available_moves)
            
            if len(available_moves) == 0: 
                utility = self.utility_get(board, flag, opponent_flag)
                return (utility, best_row, best_coloumn)


            for move in available_moves:
                currrent_board = copy.deepcopy(board)
                sign = flag
                if not max_ply_node:
                    sign = opponent_flag

                currrent_board.update(old_move, move, sign)

                if max_ply_node==True:
                    max_ply_node1 = False
                else:
                    max_ply_node1 = True

                utility = self.MinMax(currrent_board, move, max_ply_node1, flag, opponent_flag, depth+1 , alpha, beta, best_row, best_coloumn) # agains call MinMax

                
                if max_ply_node == 1: 
                    if utility[0] > alpha:
                        alpha = utility[0]
                        best_row , best_coloumn = (move[0], move[1])
                       
                else:  
                    if utility[0] < beta:
                        beta = utility[0]
                        best_row, best_coloumn = (move[0] , move[1])

                if alpha > beta:
                    break;

                if (time.time() - self.tic) > self.Time_limit:
                    return (utility, best_row, best_coloumn)
            if max_ply_node:
                return (alpha, best_row, best_coloumn)
            else:
                return (beta, best_row, best_coloumn)

    def move(self, board, old_move, flag):
        ''' Move function for bot that return Coordinates for next turn'''
        if old_move == (-1, -1):
            return (10, 10)
        self.tic = time.time()
        if flag != 'o':
            opponent_flag = 'o'
        else:
            opponent_flag = 'x'
        self.move_count += 1

        self.count_block_win['p'] = sum(blocks.count(flag) for blocks in board.block_status)
        self.count_block_win['o'] = sum(blocks.count(opponent_flag) for blocks in board.block_status)

        self.symbol = flag
       
        currrent_board = copy.deepcopy(board)
       
        self.toc = (time.time() - self.tic)
        prev_move = (0,0,0)
        self.max_depth = 2
        while(self.toc < self.Time_limit):
           
            self.next_move = prev_move
            prev_move = self.MinMax(currrent_board, old_move, True, flag, opponent_flag, 0, self.alpha, self.beta, -1,
                                     -1)
            self.max_depth += 1
            self.toc = (time.time() - self.tic)
        Coordinates = (self.next_move[1], self.next_move[2])
        return Coordinates


    def utility_get(self, board, flag, opponent_flag):
        ''' Heuristic which calculate my wining state'''
        utility_values_block = []
        for i in range(16):
            utility_values_block.append(0)
            utility_values_block[i] = self.calc_utility(board, i, flag)
        
        val_gain = 0
        lim = 1000.0
        for i in range(16):
            utility_values_block[i] = utility_values_block[i]/lim
        
      
        for i in range(4):
            local_gain = 0
            count_sym = {'p' : 0 , 'n': 0}
            for j in range(4):
                local_gain += utility_values_block[j * 4 + i]
                if board.block_status[j][i] == flag:
                   count_sym['p'] += 1
                elif board.block_status[j][i] == opponent_flag:
                    count_sym['n'] += 1
            val_gain = self.get_factor(local_gain, val_gain)
            val_gain = self.calculate(count_sym['p'], count_sym['n'], val_gain,1)


        for j in range(4):
            local_gain = 0
            count_sym = {'p' : 0 , 'n': 0}
            for i in range(4):
                local_gain += utility_values_block[j * 4 + i]
                if board.block_status[j][i] == flag:
                    count_sym['p'] += 1
                elif board.block_status[j][i] == opponent_flag:
                    count_sym['n'] += 1
            val_gain = self.get_factor(local_gain, val_gain)
            val_gain = self.calculate(count_sym['p'], count_sym['n'], val_gain,1)

        for i in range(1,3):
            for j in range(0,2):
                local_gain = 0
                count_sym = {'p' : 0 , 'n': 0}
                local_gain += utility_values_block[j*4 + i]
                if board.block_status[i][j] == flag:
                    count_sym['p'] += 1
                elif board.block_status[i][j] == opponent_flag:
                    count_sym['n'] += 1

                local_gain += utility_values_block[(j+2) * 4 + i]                
                if board.block_status[i][j+2] == flag:
                    count_sym['p'] += 1
                elif board.block_status[i][j+2] == opponent_flag:
                    count_sym['n'] += 1
                    
                local_gain += utility_values_block[(j+1)*4 + i+1]                
                if board.block_status[i+1][j+1] == flag:
                    count_sym['p'] += 1
                elif board.block_status[i+1][j+1] == opponent_flag:
                    count_sym['n'] += 1

                local_gain += utility_values_block[(j+1)* 4 + (i-1)]                    
                if board.block_status[i-1][j+1] == flag:
                    count_sym['p'] += 1
                elif board.block_status[i-1][j+1] == opponent_flag:
                    count_sym['n'] += 1
                val_gain = self.get_factor(local_gain, val_gain)
                val_gain = self.calculate(count_sym['p'], count_sym['n'], val_gain,1)
        

        count_bwin1 = sum(blocks.count(flag) for blocks in board.block_status)
        count_bwin2 = sum(blocks.count(opponent_flag) for blocks in board.block_status)
        if self.count_block_win['p'] < count_bwin1 and count_bwin2 == self.count_block_win['o']:
            val_gain += 50
        elif count_bwin1 > self.count_block_win['p'] and (count_bwin1 - self.count_block_win['p']) < (count_bwin2 - self.count_block_win['o']):
            val_gain -= 20
        elif count_bwin1 < self.count_block_win['p'] and count_bwin2 > self.count_block_win['o']:
            val_gain -= 50
        return val_gain


    def calculate(self, positive, negative, gain, flag_m):
        '''hashing Store my best or optimum move'''
        if flag_m != 0:
            val_gain = gain + 10*self.utility_val_mat[positive][negative]
        elif flag_m == 0:
            val_gain = gain + self.utility_val_mat[positive][negative]
        return val_gain


    def calc_utility(self, board, boardno, flag):
        ''' Evaluation function for utility of nodes'''
        val_gain = 0
        dict_idx = {'x': boardno /4, 'y' : boardno %4 }
        dict_idx['x'] *= 4
        dict_idx['y'] *= 4

        for i in range(dict_idx['x'], dict_idx['x'] + 4):
            count_sym = { 'p' : 0 , 'n': 0, 'nu': 0 }
            for j in range(dict_idx['y'], dict_idx['y'] + 4):
                if board.board_status[i][j] == flag:
                    count_sym['p'] += 1
                elif board.board_status[i][j] == '-':
                    count_sym['nu'] += 1
                else:
                    count_sym['n'] += 1
            val_gain = self.calculate(count_sym['p'], count_sym['n'], val_gain,0)

        for j in range(dict_idx['y'], dict_idx['y'] + 4):
            count_sym = {'p' : 0 , 'n': 0 , 'nu': 0}
            for i in range(dict_idx['x'], dict_idx['x'] + 4):
                if board.board_status[i][j] == flag:
                    count_sym['p'] += 1
                elif board.board_status[i][j] == '-':
                    count_sym['nu'] += 1
                else:
                    count_sym['n'] += 1
            val_gain = self.calculate(count_sym['p'], count_sym['n'] , val_gain , 0)

        for i in range(1,3):
            for j in range(0,2):
                count_sym = {'p' : 0 , 'n': 0 , 'nu': 0}
                if board.board_status[dict_idx['x'] + i][dict_idx['y'] + j] == flag:
                    count_sym['p'] += 1
                elif board.board_status[dict_idx['x'] + i][dict_idx['y'] + j] == '-':
                    count_sym['nu'] += 1
                else:
                    count_sym['n'] += 1
                
                if board.board_status[dict_idx['x'] + i-1][dict_idx['y'] + j+1] == flag:
                    count_sym['p'] += 1
                elif board.board_status[dict_idx['x'] + i-1][dict_idx['y'] + j+1] == '-':
                    count_sym['nu'] += 1
                else:
                    count_sym['n'] += 1

                if board.board_status[dict_idx['x'] + i+1][dict_idx['y'] + j+1] == flag:
                    count_sym['p'] += 1
                elif board.board_status[dict_idx['x'] + i+1][dict_idx['y'] + j+1] == '-':
                    count_sym['nu'] += 1
                else:
                    count_sym['n'] += 1

                if board.board_status[dict_idx['x'] + i][dict_idx['y'] + j+2] == flag:
                    count_sym['p'] += 1
                elif board.board_status[dict_idx['x'] + i][dict_idx['y'] + j+2] == '-':
                    count_sym['nu'] += 1
                else:
                    count_sym['n'] += 1
                
                positive = count_sym['p']
                negative = count_sym['n']
                val_gain = self.calculate(positive, negative, val_gain,0)


        player_flag = flag
        if flag != 'x':
            oppo_flag = 'x'
        else:
            oppo_flag = 'o'
        
        i ,j = 0, 0
        tempx , tempy  = 0 ,0 
        for lineh in self.win_rows:
            for linev in self.win_cols:
                count_win_rcd = [0,0,0,0]
                for point in lineh:
                    tempx = point[0]
                    if board.board_status[dict_idx['x'] + point[0]][dict_idx['y'] + point[1]] == player_flag:
                        count_win_rcd[0] += 1
                    elif board.board_status[dict_idx['x'] + point[0]][dict_idx['y'] + point[1]] == oppo_flag:
                        count_win_rcd[1] += 1

                for point in linev:
                    tempy = point[1]
                    if board.board_status[dict_idx['x'] + point[0]][dict_idx['y'] + point[1]] == player_flag:
                        count_win_rcd[2] += 1
                    elif board.board_status[dict_idx['x'] + point[0]][dict_idx['y'] + point[1]] == oppo_flag:
                        count_win_rcd[3] += 1

                if count_win_rcd[3] == 0 and count_win_rcd[0] == 0:
                    if count_win_rcd[1] == 2 and count_win_rcd[2] == 3 and board.board_status[dict_idx['x'] + tempx][dict_idx['y'] + tempy] == player_flag:
                        val_gain += 10

                if count_win_rcd[2] == 0 and count_win_rcd[1] == 0:
                    if count_win_rcd[0] == 3 and count_win_rcd[3] == 2 and board.board_status[dict_idx['x'] + tempx][dict_idx['y'] + tempy] == player_flag:
                        val_gain += 10
        return val_gain


    def get_factor(self, p_gain, gain):
        ''' Rate of getting utility '''
        if p_gain < 1 and p_gain >= -1:
            gain += p_gain

        elif p_gain >= 3 and p_gain < 4:
            val = 100 + (p_gain - 3) * 900
            gain += val

        elif p_gain >= -2 and p_gain < -1:
            val = -1
            val = val - (abs(p_gain) - 1) * 9
            gain += val

        elif p_gain < -3 and p_gain >=-4:
            val = -100
            val = val - (abs(p_gain) - 3) * 900
            gain += val

        elif p_gain >= 1 and p_gain < 2:
            val = 1
            val = val + (p_gain - 1) * 9
            gain += val

        elif p_gain >= 4:
            val = 1000
            val = val + (p_gain - 4) * 9000
            gain += val
        elif p_gain >= 2 and p_gain < 3:
            val = 10
            val = val + (p_gain - 2) * 90
            gain += val

        elif p_gain < -4:
            val = -1000
            val = val - (abs(p_gain) - 4) * 9000
            gain += val

        elif p_gain >= -3 and p_gain < -2:
            val = -10
            val = val - (abs(p_gain) - 2) * 90
            gain += val
        return gain
