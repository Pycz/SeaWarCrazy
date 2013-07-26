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


class superthreading:
    def __init__(self, funct):
        self.fun = funct
        
    def __call__(self, *args, **kargs):
        return wx.CallAfter(self.fun, *args, **kargs)


class Is_Float_and_time(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self):
        return Is_Float_and_time()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        
        try:
            f = float(text)
            if 0.0 <= f <= 10.0:
                return True
            else:
                textCtrl.SetValue(min(f, 10) if f > 10 else max(0, f))
                return False 
        except ValueError:
            textCtrl.SetValue("")
            return False
        else:
            return True


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
            wx.Frame.__init__(self, None, -1, size=(790, 620), title = "SeaWar Judge", pos = (300, 60))
            self.panel = wx.Panel(self, -1)
            self.judge = None
            self.field_top = 30
            self.field_left = 30
            self.field_down = self.field_top + 400
            self.field1 = Field( Map(), self.panel, (self.field_left, self.field_top), 30)
            self.field2 = Field( Map(), self.panel, (400, self.field_top), 30)

            
            self.b_add_bot1 = wx.Button(self.panel, -1, "Choose bot 1", pos = (self.field_left + 30,
                                                                               self.field_down),
                                        size = (300, 40))
            
            self.Bind(wx.EVT_BUTTON, self.on_add_bot1, self.b_add_bot1)
            
            self.b_add_bot2 = wx.Button(self.panel, -1, "Choose bot 2", pos = (430,
                                                                               self.field_down),
                                        size = (300, 40))
            
            self.Bind(wx.EVT_BUTTON, self.on_add_bot2, self.b_add_bot2)
            
            
            wildcard = "Python files (*.py)|*.py|All files (*.*)|*.*"
            self.dialog = wx.FileDialog(None, "Choose a bot executable", os.getcwd(),
                                   "", wildcard, wx.OPEN)
            
            self.bot1_path = None
            self.bot2_path = None
            
            self.bot1_name = None
            self.bot2_name = None
            
            self.l_bot1_name = wx.StaticText(self.panel, -1, "?BOT1?", pos = (self.field_left + self.field1.size,
                                                                               self.field_top - 20))
            
            self.l_bot2_name = wx.StaticText(self.panel, -1, "?BOT2?", pos = (400 + self.field2.size,
                                                                               self.field_top - 20))
            
            self.big_font = wx.Font(18, wx.DEFAULT, wx.DEFAULT, wx.DEFAULT)
            self.small_font = wx.Font(8, wx.DEFAULT, wx.DEFAULT, wx.DEFAULT)
            self.bold_font = wx.Font(40, wx.DEFAULT, wx.BOLD, wx.DEFAULT)
            self.l_bot1_name.SetForegroundColour("Green")
            self.l_bot2_name.SetForegroundColour("Red")
            self.l_bot1_name.SetFont(self.big_font)
            self.l_bot2_name.SetFont(self.big_font)
            
            
            self.l_bot1_wins = wx.StaticText(self.panel, -1, "0", pos = (self.field_left + 70,
                                                                               self.field_down - 70))
            
            self.l_wins = wx.StaticText(self.panel, -1, ":", pos = (390, self.field_down - 70))
            self.l_wins.SetFont(self.bold_font)
            self.l_wins.SetForegroundColour("Blue")
            
            self.l_bot2_wins = wx.StaticText(self.panel, -1, "0", pos = (470, self.field_down - 70))
            self.l_bot1_wins.SetFont(self.bold_font)
            self.l_bot2_wins.SetFont(self.bold_font)
            self.l_bot1_wins.SetForegroundColour("Green")
            self.l_bot2_wins.SetForegroundColour("Red")
            
            self.winlist = [0, 0, 0]
            self.maplist = [Map(), Map(), 0]
            
            self.b_start_chemp = wx.Button(self.panel, -1, "START!", pos = (self.field_left + 240,
                                                                               self.field_down + 60),
                                                                        size = (250, 100))
            
            self.b_start_chemp.SetFont(self.bold_font)
            
            self.Bind(wx.EVT_BUTTON, self.on_start_chemp, self.b_start_chemp)
            
            
            
            self.c_rounds = wx.SpinCtrl(self.panel, 
                                        -1, 
                                        value = '',
                                        pos = (self.field_left + 630, self.field_down + 55), 
                                        size = (70, 30),
                                        style = wx.SP_ARROW_KEYS,
                                        min = 1, 
                                        max = 10000, 
                                        initial = 1)
            
            self.l_rounds = wx.StaticText(self.panel, -1, "How many rounds:",
                                          pos = (self.field_left + 500, self.field_down + 65))
            
            self.c_round_pause = wx.TextCtrl(self.panel, -1, value = "0", 
                                             pos = (self.field_left + 630, self.field_down + 95),
                                             size = (70, 30), 
                                             validator = Is_Float_and_time())
            
            self.l_round_pause = wx.StaticText(self.panel, -1, "Pause between rounds:",
                                          pos = (self.field_left + 500, self.field_down + 105))
            
            self.l_round_pause.SetFont(self.small_font)
            
            self.l_turn_pause = wx.StaticText(self.panel, -1, "Pause between turns:",
                                          pos = (self.field_left + 500, self.field_down + 145))
            
            self.l_turn_pause.SetFont(self.small_font)
            
            self.c_turn_pause = wx.TextCtrl(self.panel, -1, value = "0", 
                                             pos = (self.field_left + 630, self.field_down + 135),
                                             size = (70, 30), 
                                             validator = Is_Float_and_time())
            
            self.b_pause_play = wx.Button(self.panel, -1, "Pause", pos = (self.field_left + 30,
                                                                               self.field_down + 120),
                                                                        size = (65, 40))
            
            self.Bind(wx.EVT_BUTTON, self.on_pause_play, self.b_pause_play)
            
            self.b_stop = wx.Button(self.panel, -1, "STOP", pos = (self.field_left + 95,
                                                                               self.field_down + 120),
                                                                        size = (65, 40))
            
            self.Bind(wx.EVT_BUTTON, self.on_stop, self.b_stop)
            
            self.b_flush = wx.Button(self.panel, -1, "Default", pos = (self.field_left + 165,
                                                                               self.field_down + 120),
                                                                        size = (65, 40))
            
            self.Bind(wx.EVT_BUTTON, self.on_default, self.b_flush)
            
            self.g_progress = wx.Gauge(self.panel, -1, 100, 
                                        pos = (self.field_left + 30, self.field_down + 70),
                                        size = (200, 40),
                                        style = wx.GA_HORIZONTAL)
            
            self.status_bar = self.CreateStatusBar()
            self.status_bar.SetStatusText('Hello there! Choose bots and click "START!"')
            
            self.lock = threading.Lock()
            self.running = True
            
            
            self.graphic_tread = threading.Thread(target = self.refresh)
            self.graphic_tread.daemon = True
            self.graphic_tread.start()
            
            
            self.Bind(wx.EVT_CLOSE, self.on_close, self)
         
            self.enable_disable_set = [self.b_add_bot1,
                                       self.b_add_bot2,
                                       self.b_start_chemp,
                                       self.b_flush,
                                       self.c_round_pause,
                                       self.c_rounds,
                                       self.c_turn_pause]
            
            self.play_thread_alive = [True, ]
            self.str_for_statusbar = 'Hello! Choose bots and press "START!"'
         
            self.make_elements_active(False, *[self.b_pause_play, self.b_stop])
        
        def make_elements_active(self, active = False, *els):
            for el in els:
                el.Enable(active) 
                
        def on_stop(self, event):
            self.play_thread_alive[0] = False
            
               
        def on_default(self, event):
            self.flush_all_to_default()
            self.str_for_statusbar = "All settings flushed to default"
        
        def on_pause_play(self, event):
            if self.b_pause_play.GetLabel() == "Play":
                self.b_pause_play.SetLabel("Pause")
                self.str_for_statusbar = "Computing continued... "
                self.lock.release()
            else:
                self.b_pause_play.SetLabel("Play")
                self.str_for_statusbar = "Computing paused... "
                self.lock.acquire()
            
        def on_close(self, event):
            self.running = False
            wx.Exit()
        
        def flush_for_start(self):
            self.make_elements_active(True, *self.enable_disable_set)
            self.b_pause_play.SetLabel("Pause")
            
            
            self.lock.acquire()
            self.winlist[0] = 0
            self.winlist[1] = 0
            self.winlist[2] = 0
            self.maplist[0] = Map()
            self.maplist[1] = Map()
            self.maplist[2] = 0
            self.lock.release()
            
            self.start_judge()
            self.l_bot1_wins.SetLabel("0")
            self.l_bot2_wins.SetLabel("0")
            
            
            self.g_progress.SetRange(100)
            self.g_progress.SetValue(0)  
                          
        def flush_all_to_default(self):
            self.make_elements_active(True, *self.enable_disable_set)
            self.b_pause_play.SetLabel("Pause")
            self.judge = None
            self.bot1_path = None
            self.bot2_path = None
            self.bot1_name = None
            self.bot2_name = None
            
            self.lock.acquire()
            self.winlist[0] = 0
            self.winlist[1] = 0
            self.winlist[2] = 0
            self.maplist[0] = Map()
            self.maplist[1] = Map()
            self.maplist[2] = 0
            self.lock.release()
            
            self.l_bot1_name.SetLabel("?BOT1?")
            self.l_bot2_name.SetLabel("?BOT2?")
            self.l_bot1_wins.SetLabel("0")
            self.l_bot2_wins.SetLabel("0")
            
            self.b_add_bot1.SetLabel("Choose bot 1")
            self.b_add_bot2.SetLabel("Choose bot 2")
            
            self.c_round_pause.SetValue("0")
            self.c_rounds.SetValue(1)
            self.c_turn_pause.SetValue("0")
            
            self.g_progress.SetRange(100)
            self.g_progress.SetValue(0)
            
            
            #self.lock.release()
               
        def get_round_pause(self):
            x = self.c_round_pause.GetValue()
            try:
                x = float(x)
                if 0 <= x <= 10:
                    return x
                else:
                    self.c_round_pause.SetValue(str(min(x, 10) if x > 10 else max(0, x)))
                    self.str_for_statusbar = "Warning! Pause must be between 0 and 10 sec! "
                    return float(min(x, 10) if x > 10 else max(0, x))
            except:
                self.str_for_statusbar = "Error! Pause must be a float number between 0 and 10 sec! "
                return None
            
        def get_turn_pause(self):
            x = self.c_turn_pause.GetValue()
            try:
                x = float(x)
                if 0 <= x <= 10:
                    return x
                else:
                    self.c_turn_pause.SetValue(str(min(x, 10) if x > 10 else max(0, x)))
                    self.str_for_statusbar = "Warning! Pause must be between 0 and 10 sec! "
                    return float(min(x, 10) if x > 10 else max(0, x))
            except:
                self.str_for_statusbar = "Error! Pause must be a float number between 0 and 10 sec! "
                return None        
                    
        def start_judge(self):
            if self.bot1_path and self.bot2_path:
                try:
                    self.play_thread_alive[0] = True
                    self.judge = Judge(self.bot1_path, self.bot2_path, 
                                   self.get_turn_pause(),
                                   self.get_round_pause(), 
                                   self.lock,
                                   self.play_thread_alive)
                    self.bot1_name = self.judge.bot1.name
                    self.l_bot1_name.SetLabel(self.bot1_name + " (1)")
                    self.bot2_name = self.judge.bot2.name
                    self.l_bot2_name.SetLabel(self.bot2_name + " (2)")
                except:
                    self.flush_all_to_default()
                    self.str_for_statusbar = "Error! You choose wrong file or file isn't a Bot program"
        
        def on_add_bot1(self, event):
            if self.b_add_bot1.GetLabel() != "OK":
                if self.dialog.ShowModal() == wx.ID_OK:
                    self.bot1_path = self.dialog.GetPath()
                    self.b_add_bot1.SetLabel("OK")
                    self.start_judge()
                    self.str_for_statusbar = "Bot 1 choosed"
                                       
        def on_add_bot2(self, event):
            if self.b_add_bot2.GetLabel() != "OK":
                if self.dialog.ShowModal() == wx.ID_OK:
                    self.bot2_path = self.dialog.GetPath()
                    self.b_add_bot2.SetLabel("OK")
                    self.start_judge()
                    self.str_for_statusbar = "Bot 2 choosed"
                
        def start_chemp(self, *args):
            self.flush_for_start()
            self.make_elements_active(False, *self.enable_disable_set)
            self.make_elements_active(True, *[self.b_pause_play, self.b_stop])
            self.g_progress.SetRange(args[0])
            self.g_progress.SetValue(0)
            self.str_for_statusbar = "Start computing..."
            try:
                self.judge.play_championship(*args)
            except:
                pass
            self.make_elements_active(True, *self.enable_disable_set)
            self.make_elements_active(False, *[self.b_pause_play, self.b_stop])
            if not self.play_thread_alive[0]:
                self.str_for_statusbar = "Stopped."
            else:
                self.str_for_statusbar = "Complete!"
        
        def on_start_chemp(self, event):
            if self.judge:
                t = threading.Thread(target = self.start_chemp,
                                      args = (self.c_rounds.GetValue(), self.maplist, self.winlist))
                #self.judge.play_championship(3, self.maplist, self.winlist)
                t.start()
                
                           
        def refresh(self):
            qmap = 0
            qwin = 0
            while self.running:
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
                
                wx.CallAfter(self.g_progress.SetValue, self.winlist[2]) 
                wx.CallAfter(self.status_bar.SetStatusText, self.str_for_statusbar)                     
                wx.CallAfter(self.field1.refresh)
                wx.CallAfter(self.field2.refresh)
                #self.Refresh()
                
                self.lock.release()
                time.sleep(0.1)
                
                
class My_app(wx.App):
    
    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show(True)
        return True
    
#    def OnExit(self):
#        self.frame.running = False
#        time.sleep(5)
                        
if __name__ == '__main__':
    app = My_app()
    app.MainLoop()