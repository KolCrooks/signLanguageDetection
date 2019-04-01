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
        public static int depth { get; } = 30;

        /**
         * Proccesses a stack of frames. Purpose is to process the frame pools recieved from the server.
         */
        public static int[][,] ProcessStack(String[] Frames, Size resizeDims)
        {
            //Correct the depth of the stack
            Frames = correctDepth(Frames, depth);
            Mat[] mFrames = new Mat[depth];
            Mat bg = null;
            //Create Background for subtraction
            for(int i = 0; i < depth; i++)
            {
                byte[] image = Convert.FromBase64String(Frames[i]);
                mFrames[i] = Cv2.ImDecode(image, ImreadModes.Grayscale);
                mFrames[i].ConvertTo(mFrames[i], MatType.CV_32FC1);
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
                byte[,] test = new byte[resizeDims.Width, resizeDims.Height];
                Mat temp = new Mat();
                mFrames[i].ConvertTo(temp, MatType.CV_8UC3);
                temp.GetArray(0, 0, test);
                for(int j = 0; j < resizeDims.Width; j++)
                {
                    for(int k = 0; k < resizeDims.Height; k++)
                    {
                        procedFrames[i][j, k] = test[j, k];
                    }
                }
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
                    index %= tempFrames.Count;
     
                }
                else
                {
                    tempFrames.Insert(index, frames[index]);
                    index += 2;
                    index %= frames.Length;

                }

            }

            return tempFrames.ToArray();
        }

        private static void run_avg(Mat image, ref Mat bg)
        {
            //initialize the background
            if (bg == null)
            {
                bg = image.Clone();
            }

            //compute weighted average, accumulate it and update the background
            Cv2.AccumulateWeighted(image, bg, aWeight, null);
            
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
