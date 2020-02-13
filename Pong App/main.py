# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:08:15 2020

@author: maayag
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
    )
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint



class PongPaddle(Widget):
    score = NumericProperty(0)
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            
            

class PongBall(Widget):
    
    # velocity of the ball on the x and y axes
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    # referencelist property so we can use ball.velocity as a shorthand
    # just like w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    # move function will move the ball one step. this will be called in 
    # equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y
    
    
    
    def update(self, dt):
        self.ball.move()
        
        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        # bounce off top and bottom
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
        
        # went off to a side
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))
    


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
    
if __name__ == '__main__':
    PongApp().run()