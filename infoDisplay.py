#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import requests, json

class displayInfo(SampleBase):
    def __init__(self, *args, **kwargs):
        super(displayInfo, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        rootDir = "/home/pi/rpi-rgb-led-matrix"
        font3x5 = graphics.Font()
        font3x5.LoadFont(rootDir + "/fonts/tom-thumb.bdf")
        font5x7 = graphics.Font()
        font5x7.LoadFont(rootDir + "/fonts/5x7.bdf")
        textColor = graphics.Color(255, 255, 0)
        colorWhite = graphics.Color(255, 255, 255)

        while True:
            offscreen_canvas.Clear()
            t=time.time()
            clock = time.strftime('%H:%M', time.localtime(t))
            #Fill in before running
            apiKey =""
            zipCode=""
            x = requests.get("http://api.openweathermap.org/data/2.5/weather?appid="+apiKey+"&zip="+zipCode).json()
            if x["cod"] != "404":
                y = x["main"]
                weather = str(round((y["temp"]-273.15)*9/5)+32)
            else:
                weather = "Err"
            page = 0
            
            if(page == 0):
                #Clock
                graphics.DrawText(offscreen_canvas, font5x7, 4, 7, textColor, clock)
                
                #Day of Week
                for day in range(0,7):
                    if day == int(time.strftime('%w')):
                        graphics.DrawLine(offscreen_canvas,day*3+6,8,day*3+7,8,colorWhite)
                    else:
                        graphics.DrawLine(offscreen_canvas,day*3+6,8,day*3+7,8,textColor)
                
                #Temperature
                graphics.DrawText(offscreen_canvas, font3x5, 1, 15, colorWhite, weather)
                graphics.DrawCircle(offscreen_canvas,10,11,1,colorWhite)

            time.sleep(2)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
def dot(x,y,clr):
    graphics.DrawLine(offscreen_canvas,x,y,x,y,clr);
# Main function
if __name__ == "__main__":
    run_text = displayInfo()
    if (not run_text.process()):
        run_text.print_help()
