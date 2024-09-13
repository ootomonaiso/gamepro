from flask import Blueprint, jsonify, render_template, request
from game2048 import Game2048
import time
import random

app = Blueprint('automate', __name__)

game = Game2048()

def expectimax(game, depth=3):
    """
    期待値最大化アルゴリズムによる最適解の導出
    """
    def max_value(state, depth):
        if state.game_over or depth == 0:
            return state.get_state()['score']
        
        best_value = float('-inf')
        for move in ['up', 'down', 'left', 'right']:
            child_state = state.copy()
            child_state.move(move)
            value = expect_value(child_state, depth - 1)
            best_value = max(best_value, value)
        
        return best_value
    
    def expect_value(state, depth):
        if state.game_over or depth == 0:
            return state.get_state()['score']
        
        moves = ['up', 'down', 'left', 'right']
        total_value = 0
        num_possible_moves = len(moves)
        
        for move in moves:
            child_state = state.copy()
            child_state.move(move)
            total_value += max_value(child_state, depth - 1)
        
        return total_value / num_possible_moves

    best_move = None
    best_value = float('-inf')
    for move in ['up', 'down', 'left', 'right']:
        child_state = game.copy()
        child_state.move(move)
        move_value = expect_value(child_state, depth - 1)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    
    return best_move
