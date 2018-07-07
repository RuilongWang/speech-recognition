from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
import snowboydecoder
import json

interrupted = False
class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        #PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception:
            print ("connection error")
        else:
            print ("connected")
            self.listen()

    switch = 0
    # print(messages)
    models = ["resources/ellbogen_mehr.pmdl", "resources/ellbogen_weniger.pmdl", "resources/hand_mehr.pmdl",
              "resources/hand_weniger.pmdl", "resources/halt.pmdl", "resources/stop.pmdl"]
    sensitivity = [0.47, 0.5, 0.43, 0.43, 0.4, 0.49]
    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

    def open(self):
        pass

    def interrupt_callback(self):
        global interrupted
        return interrupted

    def callback1(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 1}
        message = json.dumps(command)
        self.ws.write_message(message)
        print("command = ", message)

    def callback2(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 2}
        message = json.dumps(command)
        self.ws.write_message(message)
        print("command = ", message)

    def callback3(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 3}
        message = json.dumps(command)
        self.ws.write_message(message)
        print("command = ", message)

    def callback4(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 4}
        message = json.dumps(command)
        self.ws.write_message(message)
        print("command = ", message)

    def callback5(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        command = {'command': 5}
        message = json.dumps(command)
        self.ws.write_message(message)
        print("command = ", message)

    def callback6(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        global interrupted
        interrupted = True
        self.ws.write_message("terminate")
        print("terminate")

    def listen(self):

        # print(self.on_message("1"))
        callbacks = [self.callback1, self.callback2, self.callback3, self.callback4, self.callback5, self.callback6]

        print("say something")
        self.detector.start(detected_callback=callbacks,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.03)
        print("terminate")
        self.detector.terminate()


    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print ("connection closed")
                self.ws = None
                break

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")

if __name__ == "__main__":
    client = Client("ws://172.20.10.10:4233", 5)
    #client = Client("ws://localhost:1234", 5)
