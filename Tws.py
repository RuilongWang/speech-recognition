import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import snowboydecoder
import json


interrupted = False





class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    switch = 0
    #print(messages)
    models = ["resources/ellbogen_mehr.pmdl", "resources/ellbogen_weniger.pmdl", "resources/hand_mehr.pmdl",
              "resources/hand_weniger.pmdl", "resources/halt.pmdl", "resources/stop.pmdl"]
    sensitivity = [0.47, 0.5, 0.43, 0.43, 0.4,0.49]
    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

    def open(self):
        pass

    def interrupt_callback(self):
        global interrupted
        # self.checker()
        return interrupted

    def callback1(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 1}
        message = json.dumps(command)
        self.write_message(message)
        print("command = ", message)

    def callback2(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 2}
        message = json.dumps(command)
        self.write_message(message)
        print("command = ", message)

    def callback3(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 3}
        message = json.dumps(command)
        self.write_message(message)
        print("command = ", message)

    def callback4(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 4}
        message = json.dumps(command)
        self.write_message(message)
        print("command = ", message)

    def callback5(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 5}
        message = json.dumps(command)
        self.write_message(message)
        print("command = ", message)

    def callback6(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        global interrupted
        interrupted = True
        self.write_message("terminate")
        print("terminate")

    def listen(self):

        #print(self.on_message("1"))
        callbacks = [self.callback1, self.callback2, self.callback3, self.callback4, self.callback5, self.callback6]

        print("say something")
        self.detector.start(detected_callback=callbacks,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.03)
        print("terminate")
        self.detector.terminate()

    def on_message(self, message):


        print(message)
        # self.messages += str(message)
        # print(self.messages)
        # command = 0

        if message == "start":
            global interrupted
            interrupted = False
            self.switch = 1
            self.listen()

        if message == "stop":
            self.switch = 0



    def on_close(self):
        self.detector.terminate()
        self.close()




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
        ]

        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(1234)

    tornado.ioloop.IOLoop.instance().start()











