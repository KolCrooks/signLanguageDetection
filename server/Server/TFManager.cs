using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using TensorFlow;

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
            using (TFGraph graph = new TFGraph())
            {
                graph.Import(model);
                TFSession session = new TFSession(graph);

                var runner = session.GetRunner();
                runner.AddInput(graph["input"][0], input);
                runner.Fetch(graph["output"][0]);

                TFTensor output = runner.Run()[0];
                session.Dispose();
            }
        }
    }
}
