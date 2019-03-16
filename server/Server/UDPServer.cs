using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using Newtonsoft.Json;
using System.Collections;

namespace Server
{

    public class UDPPacket
    {
        public int[] size { get; }
        public int[] frame;
        public int state { get; }

    }

    public class UPDServer
    {
        public const int START_CAPTURE = 0;
        public const int CAPTURING = 1;
        public const int END_CAPTURE = 2;

        public UPDServer(ref PythonHelper py)
        {
            byte[] data = new byte[1024];
            IPEndPoint ipep = new IPEndPoint(IPAddress.Any, 31419);
            UdpClient newsock = new UdpClient(ipep);

            Console.WriteLine("Waiting for a client...");

            IPEndPoint sender = new IPEndPoint(IPAddress.Any, 0);
            PipePacket p = null;
            ArrayList vid = new ArrayList();
            while (true)
            {
                data = newsock.Receive(ref sender);
                string input = Encoding.ASCII.GetString(data, 0, data.Length);
                UDPPacket recieved = JsonConvert.DeserializeObject<UDPPacket>(input);

                if (p == null || recieved.state == START_CAPTURE)
                {
                    p = new PipePacket(recieved.size);
                    vid = new ArrayList();
                }
                    

                p.data.Append(recieved.frame);
                
                if(recieved.state == END_CAPTURE)
                {
                    p.data = vid.OfType<int[]>().ToArray();
                    lock (py)
                    {
                        py.toSend.Add(p);

                    }
                    vid = new ArrayList();
                }

            }
        }
    }
}
