using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using OpenCvSharp;


namespace Backend
{
    class PreProc
    {
        public static double aWeight = 0.5;
        public static int depth { get; } = 60;

        /**
         * Proccesses a stack of frames. Purpose is to process the frame pools recieved from the server.
         */
        public static int[][,] ProcessStack(int[][,] Frames, ref Mat bg, Size resizeDims)
        {
            //Correct the depth of the stack
            Frames = correctDepth(Frames, depth);

            //Create Background for subtraction
            foreach (int[,] i in Frames)
            {
                run_avg(new Mat(resizeDims.Width, resizeDims.Height, MatType.CV_8UC4, i.Cast<int>().Select(c => c).ToArray()), ref bg);
            }
            //Threshold image and subract background
            for (int i = 0; i < Frames.Length; i++)
            {
                Frames[i] = segment(Frames[i], bg, resizeDims);
            }


            return Frames;
        }

        /**
         * Resizes The array to the correct depth
         */
        private static int[][,] correctDepth(int[][,] frames, int depth)
        {
            int index = 0;

            var tempFrames = frames.Cast<int[,]>().ToList();
            while (tempFrames.Count != depth)
            {
                if (tempFrames.Count > depth)
                {
                    tempFrames.RemoveAt(index);
                    index++;
                }
                else
                {
                    tempFrames.Insert(index, frames[index]);
                    index += 2;
                }

                index %= tempFrames.Count;
            }

            return tempFrames.ToArray();
        }

        private static void run_avg(Mat image, ref Mat bg)
        {
            //initialize the background
            if (bg == null)
                bg = new Mat(image);

            //compute weighted average, accumulate it and update the background
            Cv2.AccumulateWeighted(image, bg, aWeight, new Mat());
        }
        private static int[,] segment(int[,] frame, Mat bg, Size resizeDims, int threshold = 25)
        {
            Mat mIn = new Mat(resizeDims.Width, resizeDims.Height, MatType.CV_8UC4, frame.Cast<int>().Select(c => c).ToArray());
            Mat diff = new Mat();
            Cv2.Absdiff(bg, mIn, diff);

            Mat thresholded = new Mat();
            Cv2.Threshold(diff, thresholded, threshold, 255, ThresholdTypes.Binary);
            int[,] output = new int[resizeDims.Width, resizeDims.Height];
            thresholded.GetArray(resizeDims.Width, resizeDims.Height, output);
            return output;
        }

    }
}
