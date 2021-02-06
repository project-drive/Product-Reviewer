using System.Collections;
using UnityEngine;
using UnityEngine.Networking;


public class ApiRequest : MonoBehaviour
{
    [HideInInspector]
    public string uri, productName;

    void Start()
    {
        productName = transform.parent.name;
        uri = "https:/" + "/safe-harbor-09269.herokuapp.com/?year=%22" + productName + "%22";
        StartCoroutine(GetRequest(uri));
    }

    IEnumerator GetRequest(string uri)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
        {
            // Request and wait for the desired page.
            yield return webRequest.SendWebRequest();

            string[] pages = uri.Split('/');
            int page = pages.Length - 1;

            switch (webRequest.result)
            {
                case UnityWebRequest.Result.ConnectionError:
                case UnityWebRequest.Result.DataProcessingError:
                    Debug.LogError(pages[page] + ": Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.ProtocolError:
                    Debug.LogError(pages[page] + ": HTTP Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.Success:
                    Debug.Log(pages[page] + ":\nReceived: " + webRequest.downloadHandler.text);
                    this.gameObject.SetActive(false);
                    break;
            }
        }
    }
}
