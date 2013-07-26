'''
Created on 25.07.2013

@author: pycz
'''
import os
import time
import threading
import wx
from map import Map, State
from judge import Judge

class Field:
    def __init__(self, bot_map, parent, coords, size = 30):
        self.map = bot_map
        self.parent = parent
        
        self.pos = (coords[0] + size//2 - 5, coords[1] + size//2 - 5)
        self.coords = (coords[0] + size, coords[1] + size)
        
        self.img_shooted = wx.Image("shooted.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.img_unshooted = wx.Image("unshooted.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.img_killed = wx.Image("killed.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        
       
        
        self.size = size  #height or weight
        
        self.btns = [[wx.StaticBitmap(self.parent,
                                      -1, 
                                      self.img_unshooted, 
                                      size = (self.size, self.size),
                                      style = 0,
                                      pos = (self.coords[0]+(i * self.size),  self.coords[1]+(j * self.size)))
                      for j in xrange(10)] for i in xrange(10)]
        
        #self.btns[0][4].SetBitmapLabel(self.img_killed, False)
        #self.btns[1][1].SetBitmapLabel(self.img_shooted, False)
        #self.btns[3][7].SetBitmapLabel(self.img_killed, False)
        
        self.letter_lbls = [wx.StaticText(self.parent, 
                                    -1, 
                                    chr(ord('A') + j),
                                    pos = (self.pos[0] + (j+1)*self.size, self.pos[1]),
                                    size = (self.size, self.size),
                                    style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
                      for j in xrange(10)]
        self.num_lbls = [wx.StaticText(self.parent, 
                                    -1, 
                                    str(j + 1),
                                    pos = (self.pos[0], self.pos[1] + (j+1)*self.size),
                                    size = (self.size, self.size),
                                    style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
                      for j in xrange(10)]
    
        
    def refresh(self):
        for i in xrange(10):
            for j in xrange(10):
                st = self.map.get_state_by_coords(i, j)
                if st == State.kill:
                    self.btns[i][j].SetBitmap(self.img_killed)
                elif st == State.miss:
                    self.btns[i][j].SetBitmap(self.img_shooted)
                    
    def make_empty(self, new_map):
        for i in xrange(10):
            for j in xrange(10):
                self.btns[i][j].SetBitmap(self.img_unshooted)   
        self.map = new_map            
                    
class MyFrame(wx.Frame):
    
        def __init__(self):
            wx.Frame.__init__(self, None, -1, size=(800, 600), title = "SeaWar Judge")
            self.panel = wx.Panel(self, -1)
            self.judge = None
            self.field_top = 60
            self.field_left = 30
            self.field_down = self.field_top + 400
            self.field1 = Field( Map(), self.panel, (self.field_left, self.field_top), 30)
            self.field2 = Field( Map(), self.panel, (400, self.field_top), 30)

            
            self.b_add_bot1 = wx.Button(self.panel, -1, "Choose bot 1", pos = (self.field_left,
                                                                               self.field_down))
            
            self.Bind(wx.EVT_BUTTON, self.on_add_bot1, self.b_add_bot1)
            
            self.b_add_bot2 = wx.Button(self.panel, -1, "Choose bot 2", pos = (400,
                                                                               self.field_down))
            
            self.Bind(wx.EVT_BUTTON, self.on_add_bot2, self.b_add_bot2)
            
            
            wildcard = "All files (*.*)|*.*"
            self.dialog = wx.FileDialog(None, "Choose a bot executable", os.getcwd(),
                                   "", wildcard, wx.OPEN)
            
            self.bot1_path = None
            self.bot2_path = None
            
            self.bot1_name = None
            self.bot2_name = None
            
            self.l_bot1_name = wx.StaticText(self.panel, -1, "?BOT1?", pos = (self.field_left,
                                                                               self.field_top - 20))
            
            self.l_bot2_name = wx.StaticText(self.panel, -1, "?BOT2?", pos = (400,
                                                                               self.field_top - 20))
        
            self.l_bot1_wins = wx.StaticText(self.panel, -1, "0", pos = (self.field_left,
                                                                               self.field_down + 40))
            
            self.l_bot2_wins = wx.StaticText(self.panel, -1, "0", pos = (400,
                                                                               self.field_down + 40))
            
            self.winlist = [0, 0, 0]
            self.maplist = [Map(), Map(), 0]
            
            self.b_start_chemp = wx.Button(self.panel, -1, "START!!!", pos = (self.field_left,
                                                                               self.field_down + 80))
            
            self.Bind(wx.EVT_BUTTON, self.on_start_chemp, self.b_start_chemp)
            
            
            self.lock = threading.Lock()
            
            self.graphic_tread = threading.Thread(target = self.refresh)
            self.graphic_tread.daemon = True
            self.graphic_tread.start()
            
                
        def start_judge(self):
            if self.bot1_path and self.bot2_path:
                self.judge = Judge(self.bot1_path, self.bot2_path, 0.05, 0.5, self.lock)
                self.bot1_name = self.judge.bot1.name
                self.l_bot1_name.SetLabel(self.bot1_name + " (1)")
                self.bot2_name = self.judge.bot2.name
                self.l_bot2_name.SetLabel(self.bot2_name + " (2)")
        
        def on_add_bot1(self, event):
            if self.b_add_bot1.GetLabel() != "OK":
                if self.dialog.ShowModal() == wx.ID_OK:
                    self.bot1_path = self.dialog.GetPath()
                    self.b_add_bot1.SetLabel("OK")
                    self.start_judge()
                    
                    
        def on_add_bot2(self, event):
            if self.b_add_bot2.GetLabel() != "OK":
                if self.dialog.ShowModal() == wx.ID_OK:
                    self.bot2_path = self.dialog.GetPath()
                    self.b_add_bot2.SetLabel("OK")
                    self.start_judge()
         
        
        def on_start_chemp(self, event):
            t = threading.Thread(target = self.judge.play_championship,
                                  args = (10, self.maplist, self.winlist))
            #self.judge.play_championship(3, self.maplist, self.winlist)
            t.start()
                    
        def refresh(self):
            qmap = 0
            qwin = 0
            while True:
                self.lock.acquire()
                
                if self.maplist[2] != qmap:
                    qmap = self.maplist[2]
                    wx.CallAfter(self.field1.make_empty, self.maplist[0])
                    wx.CallAfter(self.field2.make_empty, self.maplist[1])
                    #self.field1.make_empty(self.maplist[0])
                    #self.field2.make_empty(self.maplist[1])
                if self.winlist[2] != qwin:
                    qwin = self.winlist[2]
                    wx.CallAfter(self.l_bot1_wins.SetLabel, str(self.winlist[0]))
                    wx.CallAfter(self.l_bot2_wins.SetLabel, str(self.winlist[1]))                       
                wx.CallAfter(self.field1.refresh)
                wx.CallAfter(self.field2.refresh)
                #self.Refresh()
                
                self.lock.release()
                time.sleep(0.1)
                
                
                
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()