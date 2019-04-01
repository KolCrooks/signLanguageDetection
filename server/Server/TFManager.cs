using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using TensorFlow;
using Newtonsoft.Json;

namespace Backend
{
    class TFManager : IDisposable
    {
        private byte[] model;
        private TFGraph graph;
        private TFSession session;
        public TFManager(string model = @"C:\Users\kolcr\Desktop\Programming\signLanguageDetection\py\model\v1.0\model.pb")
        {
            //Set up tensorflow Objects
            this.model = File.ReadAllBytes(model);
            graph = new TFGraph();
            graph.Import(this.model);
            session = new TFSession(graph);
        }

        public void Dispose()
        {
            graph.Dispose();
            session.Dispose();
        }

        public void execute(TFTensor input, ref NetworkStream client)
        {
            //Start Timer
            var stopwatch = new Stopwatch();
            

            //Run Graph with data
            var runner = session.GetRunner();
            runner.AddInput(graph["conv3d_1_input"][0], input);
            runner.Fetch(graph["activation_1/Softmax"][0]);
            
            TFTensor output = runner.Run()[0];


            //Create packet with JSON format
            string outString = "{data:[";

            foreach (int i in ((int[][])output.GetValue(jagged: true))[0])
                outString += i + ",";

            outString += "]}";

            byte[] outb = Encoding.UTF8.GetBytes(outString);

            //Send Packet
            client.Write(outb, 0, outb.Length);


            //End Timer
            stopwatch.Stop();
            var elapsed_time = stopwatch.ElapsedMilliseconds;
            Console.WriteLine(Thread.CurrentThread.Name + ": Classified in " + elapsed_time + "ms");

        }

    }
}
