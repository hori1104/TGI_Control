using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

public class SocketManager : MonoBehaviour
{
    private TcpClient client;
    private StreamReader reader;
    private bool isRunning = true;

    public float ElapsedTime { get; private set; }

    private static SocketManager _instance;
    public static SocketManager Instance
    {
        get
        {
            if (_instance == null)
            {
                Debug.LogError("SocketManagerインスタンスが存在しません。シーンにアタッチする必要があります。");
            }
            return _instance;
        }
    }

    private void Awake()
    {
        if (_instance == null)
        {
            _instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    async void Start()
    {
        try
        {
            string host = "192.168.1.152";
            int port = 12345;

            client = new TcpClient();
            await client.ConnectAsync(host, port);
            reader = new StreamReader(client.GetStream(), Encoding.UTF8);
            Debug.Log("Connected to Raspberry Pi!");

            _ = ReadDataAsync();
        }
        catch (Exception e)
        {
            Debug.LogError($"Failed to connect: {e.Message}");
        }
    }

    async Task ReadDataAsync()
    {
        try
        {
            StringBuilder dataBuffer = new StringBuilder();

            while (isRunning && client.Connected)
            {
                char[] buffer = new char[1024];
                int bytesRead = await reader.ReadAsync(buffer, 0, buffer.Length);

                if (bytesRead > 0)
                {
                    dataBuffer.Append(buffer, 0, bytesRead);

                    string data = dataBuffer.ToString();
                    int newlineIndex;

                   
                    while ((newlineIndex = data.IndexOf('\n')) != -1)
                    {
                        string completeMessage = data.Substring(0, newlineIndex).Trim();

                        if (float.TryParse(completeMessage, out float parsedTime))
                        {
                            UnityMainThreadDispatcher.Instance.Enqueue(() =>
                            {
                                ElapsedTime = parsedTime;
                                Debug.Log($"Elapsed Time: {ElapsedTime}");
                            });
                        }
                        else
                        {
                            Debug.LogError($"Failed to parse elapsed time: {completeMessage}");
                        }

                        data = data.Substring(newlineIndex + 1);
                        dataBuffer.Clear();
                        dataBuffer.Append(data);
                    }
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"Error receiving data: {e.Message}");
        }
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        if (reader != null) reader.Close();
        if (client != null) client.Close();
    }
}
