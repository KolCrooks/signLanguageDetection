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
    class TFManager
    {
        byte[] model;
        public TFManager(string model = @"C:\Users\kolcr\Desktop\signLanguageDetection\py\model\v1.0\model.pb")
        {
            this.model = File.ReadAllBytes(model);
        }

        public void execute(TFTensor input, UdpClient udpServer)
        {
            Thread t = new Thread(()=>run(input, udpServer, model));
            t.Start();
        }
        private void run(TFTensor input, UdpClient udpServer, byte[] model)
        {
            Thread.CurrentThread.Name = udpServer.ToString();

            var stopwatch = new Stopwatch();
            using (TFGraph graph = new TFGraph())
            {
                graph.Import(model);
                TFSession session = new TFSession(graph);

                var runner = session.GetRunner();
                runner.AddInput(graph["input"][0], input);
                runner.Fetch(graph["output"][0]);

                stopwatch.Stop();

                TFTensor output = runner.Run()[0];
                session.Dispose();
                string outString = "{data:[";

                foreach (int i in ((int[][])output.GetValue(jagged: true))[0])
                    outString += i + ",";

                outString += "]}";

                byte[] outb = Encoding.ASCII.GetBytes(outString);
                udpServer.SendAsync(outb, outb.Length);

            }
            stopwatch.Stop();
            var elapsed_time = stopwatch.ElapsedMilliseconds;
            Console.WriteLine(Thread.CurrentThread.Name + ": Classified in " + elapsed_time + "ms");

        }

    }
}
