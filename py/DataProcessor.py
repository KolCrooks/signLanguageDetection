import json
import os
import threading
import sys
import cv2
import numpy as np

bg = None

class DataProc:

    def replace_line(self, n_line):
        sys.stdout.write("\r" + n_line)
        sys.stdout.flush()

    def read_dataset(self, videos, directory, input_list):
        vid_cnt = 0
        aWeight = 0.5
        vid_loaded = []
        for vid in videos:
            vid = directory + vid
            frames = []
            frame_clones = []
            cap = cv2.VideoCapture(vid)
            while True:
                ret, frame = cap.read()
                if frame is None:
                    break
                frame = cv2.resize(frame, (self.img_rows, self.img_cols), interpolation=cv2.INTER_AREA)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.run_avg(gray, aWeight)

                frame_clones.append(gray)

            vid_cnt += 1
            self.printLock.acquire()
            try:
                sys.stdout.write(
                    "\r Loading " + directory + " (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + str(len(frames)))
                sys.stdout.flush()
            finally:
                self.printLock.release()

            frame_clones = self.correct_depth(frame_clones, directory, vid_cnt, len(videos))

            for frame in frame_clones:
                (thresholded, segmented) = self.segment(frame)
                frames.append(thresholded)
                cv2.imshow("f",frame)
            vid_loaded.append(frames)

        print("")
        print("Loading " + directory + " (" + str(len(videos)) + "/" + str(len(videos)) + ")\t Done.")
        print("")
        cap.release()
        cv2.destroyAllWindows()
        input = np.array(vid_loaded)
        # ipt = np.rollaxis(np.rollaxis(input, 2, 0), 2, 0)  # to make data in image row, image column, image depth
        self.lock.acquire()
        try:
            input_list.append(input)
        finally:
            self.lock.release()

    def correct_depth(self, frames, directory, vid_cnt, videos):
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
                        "\r Loading " + directory + " (" + str(vid_cnt) + "/" + str(videos) + ") " + loading[
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
                        "\r Loading " + directory + " (" + str(vid_cnt) + "/" + str(videos) + ") " + loading[
                            cnt2 % len(loading)])
                    sys.stdout.flush()
                finally:
                    self.printLock.release()
        return frames

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
                exit(-1)

        for t in threads:
            t.join()

        return (X_tr, indexes)

    # -------------------------------------------------------------------------------
    # Function - To segment the region of hand in the image
    # -------------------------------------------------------------------------------
    def segment(self, image, threshold=25):
        global bg
        # find the absolute difference between background and current frame
        diff = cv2.absdiff(bg.astype("uint8"), image)

        # threshold the diff image so that we get the foreground
        thresholded = cv2.threshold(diff,
                                    threshold,
                                    255,
                                    cv2.THRESH_BINARY)[1]

        # # get the contours in the thresholded image
        # (_, cnts, _) = cv2.findContours(thresholded.copy(),
        #                                 cv2.RETR_EXTERNAL)
        #
        # # return None, if no contours detected
        # if len(cnts) == 0:
        #     return
        # else:
        #     # based on contour area, get the maximum contour which is the hand
        #     segmented = max(cnts, key=cv2.contourArea)
        #     return thresholded, segmented
        return thresholded, None

    # -------------------------------------------------------------------------------
    # Function - To find the running average over the background
    # -------------------------------------------------------------------------------
    def run_avg(self, image, aWeight):
        global bg
        # initialize the background
        if bg is None:
            bg = image.copy().astype("float")
            return

        # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(image, bg, aWeight)

    def __init__(self, settings):
        self.img_rows, self.img_cols, self.img_depth = settings.img_size[2], settings.img_size[1], settings.img_size[0]
        self.lock = threading.Lock()
        self.printLock = threading.Lock()
        global loading
        loading = ["|", "/", "-", "\\"]
