using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class scalesocket : MonoBehaviour
{
    private AudioSource audioSource;

    void Start()
    {
        audioSource = GetComponent<AudioSource>();

        if (audioSource == null)
        {
            Debug.LogWarning("AudioSourceがアタッチされていません。このスクリプトをAudioSourceが含まれるオブジェクトにアタッチしてください。");
        }
    }

    void Update()
    {
        if (SocketManager.Instance != null)
        {
            float elapsedTime = SocketManager.Instance.ElapsedTime;
            Debug.Log($"Elapsed Time scale: {elapsedTime}");

            if (elapsedTime <= 30.0f)
            {
                SetScale(0.04f);
                SetVolume(0.05f);
            }
            else if (elapsedTime <= 45.0f)
            {
                SetScale(0.05f);
                SetVolume(0.1f);
            }
            else if (elapsedTime <= 57.5f)
            {
                SetScale(0.075f);
                SetVolume(0.25f);
            }
            else if (elapsedTime <= 67.5f)
            {
                SetScale(0.100f);
                SetVolume(0.50f);
            }
            else if (elapsedTime <= 75.0f)
            {
                SetScale(0.125f);
                SetVolume(0.75f);
            }
            else if (elapsedTime <= 80.0f)
            {
                SetScale(0.150f);
                SetVolume(1.0f);
            }
            else if (elapsedTime <= 87.5f)
            {
                SetScale(0.125f);
                SetVolume(0.75f);
            }
            else if (elapsedTime <= 97.5f)
            {
                SetScale(0.100f);
                SetVolume(0.50f);
            }
            else if (elapsedTime <= 110.0f)
            {
                SetScale(0.075f);
                SetVolume(0.25f);
            }
            else if (elapsedTime <= 125.0f)
            {
                SetScale(0.050f);
                SetVolume(0.1f);
            }
            else
            {
                SetScale(0.040f);
                SetVolume(0.05f);
            }
        }
    }

    void SetScale(float scaleValue)
    {
        transform.localScale = new Vector3(scaleValue, scaleValue, scaleValue);
    }

    void SetVolume(float volume)
    {
        if (audioSource != null)
        {
            audioSource.volume = volume;
        }
    }
}
