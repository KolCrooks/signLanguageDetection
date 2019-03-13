import json
import os
import threading
import sys
import cv2
import numpy as np


class DataProc:

    def replace_line(self, n_line):
        sys.stdout.write("\r" + n_line)
        sys.stdout.flush()

    def read_dataset(self, videos, directory, input_list):
        vid_cnt = 0
        for vid in videos:
            vid = directory + vid
            framesBS = []
            frames = []
            cap = cv2.VideoCapture(vid)
            backSub = cv2.createBackgroundSubtractorKNN()
            while True:
                ret, frame = cap.read()
                if frame is None:
                    break
                frame = cv2.resize(frame, (self.img_rows, self.img_cols), interpolation=cv2.INTER_AREA)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                framesBS.append(gray)
                backSub.apply(gray)

            for frame in framesBS:
                frames.append(backSub.apply(frame))

            vid_cnt += 1
            self.printLock.acquire()
            try:
                sys.stdout.write(
                    "\r Loading " + directory + " (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + str(len(frames)))
                sys.stdout.flush()
            finally:
                self.printLock.release()

            cnt = 0
            cnt2 = 0
            if len(frames) > self.img_depth:
                while len(frames) > self.img_depth:
                    del frames[cnt]
                    cnt += 1
                    cnt2 += 1
                    cnt %= len(frames)
                    self.printLock.acquire()
                    try:
                        sys.stdout.write(
                            "\r Loading " + directory + " (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + loading[
                                cnt2 % len(loading)])
                        sys.stdout.flush()
                    finally:
                        self.printLock.release()
            else:
                while len(frames) < self.img_depth:
                    frames.insert(cnt, frames[cnt])
                    cnt += 2
                    cnt2 += 1
                    cnt %= len(frames)
                    self.printLock.acquire()
                    try:
                        sys.stdout.write(
                            "\r Loading " + directory + " (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + loading[
                                cnt2 % len(loading)])
                        sys.stdout.flush()
                    finally:
                        self.printLock.release()
        print("")
        print("Loading " + directory + " (" + str(len(videos)) + "/" + str(len(videos)) + ")\t Done.")
        print("")
        cap.release()
        cv2.destroyAllWindows()
        input = np.array(frames)
        # ipt = np.rollaxis(np.rollaxis(input, 2, 0), 2, 0)  # to make data in image row, image column, image depth
        self.lock.acquire()
        try:
            input_list.append(input)
        finally:
            self.lock.release()

    def load_folders(self, data):
        X_tr = []
        # handMoving Data set
        indexes = []
        threads = []
        for p in data:
            listing = os.listdir(p)
            indexes.append(len(listing))
            try:
                t = threading.Thread(target=self.read_dataset, args=(listing, p, X_tr))
                t.start()
                threads.append(t)
            except:
                print("Error in starting threads")
                exit(-1);

        for t in threads:
            t.join()

        return (X_tr, indexes)

    def __init__(self, settings):
        self.img_rows, self.img_cols, self.img_depth = settings.img_size[2], settings.img_size[1], settings.img_size[0]
        self.lock = threading.Lock()
        self.printLock = threading.Lock()
        global loading
        loading = ["|", "/", "-", "\\"]
