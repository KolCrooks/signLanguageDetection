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
        public Size resizeDims { get; set; }
        public double aWeight { get; set; }

        public PreProc(Size resizeDims)
        {
            this.resizeDims = resizeDims;
            aWeight = 0.5;
        }

        public int[,] ProcessSingle(int[,] frame, ref Mat bg)
        {
            int[,] output = new int[resizeDims.Width, resizeDims.Height];
            Mat mIn = new Mat(resizeDims.Width, resizeDims.Height, MatType.CV_8UC4, frame.Cast<int>().Select(c => c).ToArray());
            Mat mOut = new Mat();
            Cv2.Resize(mIn, mOut, resizeDims, interpolation: InterpolationFlags.Area);
            Cv2.CvtColor(mOut, mOut, ColorConversionCodes.BGR2GRAY);
            run_avg(mOut, ref bg);
            //TODO CORRECT DEPTH
            //TODO THRESHOLD
            mOut.GetArray(resizeDims.Width, resizeDims.Height, output);
            return output;
        }
        public int[][,] ProcessStack(int[][,] Frames, Mat bg)
        {
            //Correct the depth of the stack
            Frames = correctDepth(Frames, 60);
            //Threshold image
            for(int i = 0; i < Frames.Length; i++)
            {
                Frames[i] = segment(Frames[i], bg);
            }

            return Frames;
        }

        private int[][,] correctDepth(int[][,] frames, int depth)
        {
            int index = 0;
            while(frames.Length != depth)
            {
                var tempFrames = frames.Cast<int[,]>().ToList();
                if (frames.Length > depth)
                {
                    tempFrames.RemoveAt(index);
                    index++;
                }
                else
                {
                    tempFrames.Insert(index, frames[index]);
                    index += 2;
                }
                       
                frames = tempFrames.ToArray();
                    
                index %= frames.Length;
            }
            return frames;
        }

        private void run_avg(Mat image, ref Mat bg)
        {
            //initialize the background
            if (bg == null)
                bg = new Mat(image);

            //compute weighted average, accumulate it and update the background
            Cv2.AccumulateWeighted(image, bg, aWeight, new Mat());
        }
        private int[,] segment(int[,] frame, Mat bg, int threshold = 25)
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
