using Backend;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;
using OpenCvSharp;
using TensorFlow;
using System.Collections;

namespace server
{
    class Session : IDisposable
    {
        private TFManager tf;
        private IPAddress address;
        private TcpClient client;
        private Thread thread;
        private NetworkStream netStream;
        private bool running = true;
        private List<byte> packetPool;
        public static Size size = new Size(60, 60);
        private string ip;
        private int chunks = 0;

        public Session(TcpClient client)
        {
            packetPool = new List<byte>();
            tf = new TFManager();
            this.client = client;
            ip = ((IPEndPoint)client.Client.RemoteEndPoint).Address.ToString();
            //Create thread to listen for specific client
            thread = new Thread(new ThreadStart(sessionThread));
            thread.Name = ip;
            thread.Start();
        }

        /**
         * 
         * Checks to see if the tcp stream has recieved any pools
         * PACKET FORMAT
         * BYTE[0]: 1 or 0   -  0 if pooling bytes, 1 if done pooling
         * BYTE[1:]: DATA IN FORMAT OF STRING, IN JSON
         */
        public Tuple<bool,packet> checkStream()
        {

            byte[] bytes = new byte[1400];

            //Get Data From stream
            var i = netStream.Read(bytes, 0, bytes.Length);

            //Check to see if message was recieved, if not return
            if (i == 0)
                return new Tuple<bool, packet>(false,null); 


            //Check if pooling and if so, add to pool and wait till next packet
            if(bytes[0] == 0x0)
            {
                chunks++;
                var temp = bytes.Slice(1, bytes.Length);
                Console.WriteLine("{0}: Adding chunk {1}, byte 0: {2}, packetPool: {3}", ip, chunks, temp[0], packetPool.Count);

                packetPool.AddRange(temp);
                return new Tuple<bool, packet>(false, null);
            }
            chunks = 0;

            packetPool.AddRange(bytes.Slice(1, bytes.Length));
            //Convert JSON data to a packet object
            string data = System.Text.Encoding.UTF8.GetString(packetPool.ToArray(), 0, packetPool.Count);
            
            packet p = JsonConvert.DeserializeObject<packet>(data);
            
            return new Tuple<bool,packet>(true,p);
        }

        public void Dispose()
        {
            client.Close();
            tf.Dispose();
            running = false;
        }
        /**
         * Looped thread that listens on socket. It will end when the client dissconnects
         */
        public void sessionThread()
        {
            netStream = client.GetStream();

            //Thread loop that listens for all data coming from the tcp client
            while (running)
            {

                Tuple<bool, packet> result = null;
                //Check the stream to see if there are any pools to test
                try
                {
                    result = checkStream();
                }
                catch(Exception e)
                {
                    Console.Error.WriteLine(e);
                    Console.WriteLine("IP:{0}   - Dissconected", ip);
                    this.Dispose();
                    return;
                }
                if (!result.Item1)
                    continue;

                packet p = result.Item2;
                

                //Process Frames
                int[][,] procStack = PreProc.ProcessStack(p.frames.ToArray(), size);

                //Convert 3D array to 5D so that we have the propper model input
                int[][][][][] tfInput = new int[1][][][][];

                int[][][] jaggedStack = new int[PreProc.depth][][];
                //The array is in int[][,] format and needs to be converted to int[][][]
                for(int i = 0; i < PreProc.depth; i++)
                {
                    jaggedStack[i] = procStack[i].ToJaggedArray();
                }
                //Make tensor input to be int[1][1][60][width][depth] with each pixel correct;
                tfInput[0] = new int[1][][][];
                tfInput[0][0] = jaggedStack;

                //Run Model with client input
                TFTensor tensor = new TFTensor(tfInput);
                tf.execute(tensor, ref netStream);
            }
            this.Dispose();
        }

    }
}
