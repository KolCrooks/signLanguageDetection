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
        public static int[][,] ProcessStack(String[] Frames, ref Mat bg, Size resizeDims)
        {
            //Correct the depth of the stack
            Frames = correctDepth(Frames, depth);
            Mat[] mFrames = new Mat[depth];
            //Create Background for subtraction
            for(int i = 0; i < depth; i++)
            {
                byte[] image = Convert.FromBase64String(Frames[i]);
                mFrames[i] = Cv2.ImDecode(image, ImreadModes.Grayscale);
                run_avg(mFrames[i], ref bg);
            }
            //Threshold image and subract background
            for (int i = 0; i < depth; i++)
            {
                mFrames[i] = segment(mFrames[i], bg, resizeDims);
            }

            int[][,] procedFrames = new int[depth][,];

            for(int i = 0; i < depth; i++)
            {
                procedFrames[i] = new int[resizeDims.Width, resizeDims.Height];
                mFrames[i].GetArray(mFrames[i].Width, mFrames[i].Height, procedFrames[i]);
            }
            return procedFrames;
        }

        /**
         * Resizes The array to the correct depth
         */
        private static string[] correctDepth(string[] frames, int depth)
        {
            int index = 0;

            var tempFrames = frames.ToList();
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
        private static Mat segment(Mat frame, Mat bg, Size resizeDims, int threshold = 25)
        {
            Mat diff = new Mat();
            Cv2.Absdiff(bg, frame, diff);

            Mat thresholded = new Mat();
            Cv2.Threshold(diff, thresholded, threshold, 255, ThresholdTypes.Binary);

            return thresholded;
        }

    }
}
