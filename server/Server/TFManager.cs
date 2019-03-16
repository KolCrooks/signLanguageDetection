using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using TensorFlow;

namespace server
{
    class TFManager : IDisposable
    {
        TFGraph graph;
        TFSession session;
        public TFManager(string model = @"C:\Users\kolcr\Desktop\signLanguageDetection\py\model\v1.0\model.pb")
        {
            graph = new TFGraph();
            graph.Import(File.ReadAllBytes(model));
            session = new TFSession(graph);
        }

        public void Dispose()
        {
            graph.Dispose();
            session.Dispose();
        }

        public async Task<TFTensor> execute(TFTensor input)
        {
            var runner = session.GetRunner();
            runner.AddInput(graph["input"][0], input);
            runner.Fetch(graph["output"][0]);

            TFTensor output = runner.Run()[0];
            return output;
        }
    }
}
