using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.IO.Pipes;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Server
{
    public class PipePacket
    {
        public int[] size { get; }
        public int[][] data;
        public PipePacket(int[] size) => this.size = size;

    }
    public class PythonHelper
    {

        public ArrayList toSend = new ArrayList();

        public PythonHelper()
        {
            // Open the named pipe.
            var server = new NamedPipeServerStream("NPtest");
            Console.WriteLine("Waiting for python connection...");
            server.WaitForConnection();


            Console.WriteLine("Connected.");
            var br = new BinaryReader(server);
            var bw = new BinaryWriter(server);

            while (true)
            {
                try
                {
                    var len = (int)br.ReadUInt32();            // Read string length
                    var str = new string(br.ReadChars(len));    // Read string

                    Console.WriteLine("Read: \"{0}\"", str);
                    lock (toSend)
                    {
                        foreach (PipePacket s in toSend)
                        {

                            string json = JsonConvert.SerializeObject(s);
                            var buf = Encoding.ASCII.GetBytes(json);     // Get ASCII byte array     
                            bw.Write((uint)buf.Length);                // Write string length
                            bw.Write(buf);                              // Write string
                        }
                    }
                }
                catch (EndOfStreamException)
                {
                    break;                    // When client disconnects
                }
            }

            

            Console.WriteLine("Client disconnected.");
            server.Close();
            server.Dispose();

        }
    }
}
