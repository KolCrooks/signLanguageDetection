using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace server
{
    class packet
    {
        public int[] size;
        public uint[] frame;
        public int state;
    }
    class session
    {
        public int[] size { get;  }
        public ArrayList frames;
        public session() { }
        public session(packet p, ref PreProc imgProc)
        {
            size = p.size;
            frames.Add(imgProc.process(p.frame));
        }

    }
    class Server
    {
        public const int START_POOL = 0;
        public const int POOLING = 0;
        public const int END_POOL = 0;

        public Server(int port = 31419)
        {
            UdpClient udpServer = new UdpClient(port);
            TFManager tf = new TFManager();
            Dictionary<string, session> sessions = new Dictionary<string, session>();
            while (true)
            {
                IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, port);
                byte[] data = udpServer.Receive(ref remoteEP); // listen
                Console.Write("receive data from " + remoteEP.ToString());

                string result = System.Text.Encoding.UTF8.GetString(data);

                packet p = JsonConvert.DeserializeObject<packet>(result);
                string sessionIP = remoteEP.Address.ToString();

                switch (p.state)
                {
                    case START_POOL:
                        if (sessions.ContainsKey(sessionIP))
                            sessions.Remove(sessionIP);
                        sessions.Add(sessionIP, new session(p, ));
                        break;
                    case POOLING:
                        sessions[sessionIP].frames.Add(p.)
                }

            }
        }
    }
}
