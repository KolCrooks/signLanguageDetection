using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using OpenCvSharp;
using TensorFlow;


namespace Backend
{
    class packet
    {
        public int[] size;
        public int[][] frame;
        public int state;
    }
    class session
    {
        public int[] size { get;  }
        public List<int[,]> frames = new List<int[,]>();
        public Mat bg;
        public session() { }
    
        public session(packet p, ref PreProc imgProc)
        {
            size = p.size;
            addFrame(p.frame, ref imgProc);
        }

        public void addFrame(int[][] frame, ref PreProc imgProc)
        {
            int[,] temp = new int[frame.Length, frame[0].Length];
            for (int i = 0; i < frame.Length; i++)
            {
                for (int j = 0; j < frame[i].Length; j++)
                    temp[i, j] = frame[i][j];
            }

            frames.Add(imgProc.ProcessSingle(temp, ref bg));
        }

    }
    class Server
    {
        public const int START_POOL = 0;
        public const int POOLING = 1;
        public const int END_POOL = 2;
        Size size = new Size(60, 60);

        public Server(int port = 31419)
        {
            UdpClient udpServer = new UdpClient(port);
            TFManager tf = new TFManager();
            Dictionary<string, session> sessions = new Dictionary<string, session>();
            PreProc preProc = new PreProc(size);

            while (true)
            {
                IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, port);
                byte[] data = udpServer.Receive(ref remoteEP); // listen
                Console.Write("receive data from " + remoteEP.ToString());

                string result = System.Text.Encoding.UTF8.GetString(data);

                packet p = JsonConvert.DeserializeObject<packet>(result);
                string sessionID = remoteEP.Address.ToString();

                switch (p.state)
                {
                    case START_POOL:
                        if (sessions.ContainsKey(sessionID))
                            sessions.Remove(sessionID);
                        sessions.Add(sessionID, new session(p, ref preProc));
                        break;
                    case POOLING:
                        sessions[sessionID].addFrame(p.frame, ref preProc);
                        break;
                    case END_POOL:
                        int[][,] processed = preProc.ProcessStack(sessions[sessionID].frames.ToArray(), sessions[sessionID].bg);
                        int[][][][][] send = new int[1][][][][];
                        foreach(int[,] i in processed)
                            send[0][0].Append<int[][]>(i.ToJaggedArray());

                        TFTensor tensor = new TFTensor(send);
                        tf.execute(tensor, udpServer);
                        sessions.Remove(sessionID);
                        break;
                }

            }
        }
    }
    internal static class ExtensionMethods
    {
        internal static T[][] ToJaggedArray<T>(this T[,] twoDimensionalArray)
        {
            int rowsFirstIndex = twoDimensionalArray.GetLowerBound(0);
            int rowsLastIndex = twoDimensionalArray.GetUpperBound(0);
            int numberOfRows = rowsLastIndex + 1;

            int columnsFirstIndex = twoDimensionalArray.GetLowerBound(1);
            int columnsLastIndex = twoDimensionalArray.GetUpperBound(1);
            int numberOfColumns = columnsLastIndex + 1;

            T[][] jaggedArray = new T[numberOfRows][];
            for (int i = rowsFirstIndex; i <= rowsLastIndex; i++)
            {
                jaggedArray[i] = new T[numberOfColumns];

                for (int j = columnsFirstIndex; j <= columnsLastIndex; j++)
                {
                    jaggedArray[i][j] = twoDimensionalArray[i, j];
                }
            }
            return jaggedArray;
        }
    }
}
