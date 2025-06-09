using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class colorsocket : MonoBehaviour
{
    private Renderer objectRenderer;
    private Material targetMaterial;

    public int materialIndex = 1;  

    
    public string tintColorPropertyName = "_TintColor";

    void Start()
    {
        objectRenderer = GetComponent<Renderer>();

        
        if (objectRenderer.materials.Length > materialIndex)
        {
            targetMaterial = objectRenderer.materials[materialIndex];
        }
        else
        {
            Debug.LogError("指定したインデックスのマテリアルが存在しません。");
        }
    }

    void Update()
    {
        if (SocketManager.Instance != null)
        {
            float elapsedTime = SocketManager.Instance.ElapsedTime;
            if (elapsedTime <= 30.0f)
            {
                SetTintAlpha(0.0f);
            }
            else if (elapsedTime <= 45.0f)
            {
                SetTintAlpha(0.02f);
            }
            else if (elapsedTime <= 57.5f)
            {
                SetTintAlpha(0.1f);
            }
            else if (elapsedTime <= 67.5f)
            {
                SetTintAlpha(0.2f);
            }
            else if (elapsedTime <= 75.0f)
            {
                SetTintAlpha(0.4f);
            }
            else if (elapsedTime <= 80.0f)
            {
                SetTintAlpha(1.0f);
            }
            else if (elapsedTime <= 87.5f)
            {
                SetTintAlpha(0.4f);
            }
            else if (elapsedTime <= 97.5f)
            {
                SetTintAlpha(0.2f);
            }
            else if (elapsedTime <= 110f)
            {
                SetTintAlpha(0.1f);
            }
            else if (elapsedTime <= 125f)
            {
                SetTintAlpha(0.02f);
            }
            else
            {
                SetTintAlpha(0.0f);
            }
        }
    }

    void SetTintAlpha(float alphaValue)
    {
        if (targetMaterial != null)
        {
          
            if (targetMaterial.HasProperty(tintColorPropertyName))
            {
                Color tintColor = targetMaterial.GetColor(tintColorPropertyName);
                tintColor.a = alphaValue;
                targetMaterial.SetColor(tintColorPropertyName, tintColor);
            }
            else
            {
                Debug.LogError($"指定したプロパティ '{tintColorPropertyName}' がマテリアルに存在しません。");
            }
        }
        else
        {
            Debug.LogError("targetMaterialが設定されていません。");
        }
    }
}