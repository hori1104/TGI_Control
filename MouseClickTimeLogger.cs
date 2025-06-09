using System.Collections.Generic;
using UnityEngine;

public class MouseClickTimeLogger : MonoBehaviour
{
    // 左クリックと右クリックの elapsed_time を保持するリスト
    private List<float> leftClickTimes = new List<float>();
    private List<float> rightClickTimes = new List<float>();

    void Update()
    {
        // SocketManager のインスタンスを取得
        if (SocketManager.Instance == null)
        {
            Debug.LogError("SocketManager インスタンスが存在しません！");
            return;
        }

        // ラズパイからの elapsed_time を取得
        float elapsedTime = SocketManager.Instance.ElapsedTime;

        // 左クリックを検知
        if (Input.GetMouseButtonDown(0))
        {
            leftClickTimes.Add(elapsedTime);
            Debug.Log($"Left Click: {elapsedTime:F2} seconds from Raspberry Pi.");
        }

        // 右クリックを検知
        if (Input.GetMouseButtonDown(1))
        {
            rightClickTimes.Add(elapsedTime);
            Debug.Log($"Right Click: {elapsedTime:F2} seconds from Raspberry Pi.");
        }
    }

    // ゲーム終了時の処理
    void OnApplicationQuit()
    {
        Debug.Log("Game Ended! Displaying all recorded elapsed times:");

        Debug.Log("Left Click Times:");
        foreach (var time in leftClickTimes)
        {
            Debug.Log(time);
        }

        Debug.Log("Right Click Times:");
        foreach (var time in rightClickTimes)
        {
            Debug.Log(time);
        }
    }

    // クリック記録を取得するメソッド
    public List<float> GetLeftClickTimes()
    {
        return new List<float>(leftClickTimes);
    }

    public List<float> GetRightClickTimes()
    {
        return new List<float>(rightClickTimes);
    }
}
