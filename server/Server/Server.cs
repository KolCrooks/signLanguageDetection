using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using OpenCvSharp;
using server;
using TensorFlow;


namespace Backend
{
    class packet
    {
        public List<string> frames { get; set; }
        public List<int> size { get; set; }
    }

    class Server
    {

        TcpListener server;

        public Server(int port = 31419)
        {
            //Sessions
            Dictionary<string, Session> sessions = new Dictionary<string, Session>();

            IPAddress localAddr = IPAddress.Parse("127.0.0.1");

            //Create TCP Listener
            server = new TcpListener(localAddr, port);

            // Start listening for client requests.
            server.Start();

            //Accept Clients and give them their own session
            while (true)
            {
                TcpClient cl = server.AcceptTcpClient();
                string ip = ((IPEndPoint)cl.Client.RemoteEndPoint).Address.ToString();
                sessions.Remove(ip);

                sessions.Add(ip,new Session(cl));
                Console.WriteLine("IP:{0}   - Connected", ip);
            }
        }
    }
}
