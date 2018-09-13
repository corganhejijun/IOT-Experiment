package com.android.corgan.myiotapp;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.HttpURLConnection;
import java.net.URL;

public class WebThread implements Runnable {
    private String webUrl;
    private Handler handler;
    public WebThread(String url, Handler handler){
        webUrl = url;
        this.handler = handler;
        CookieManager cookieManager = new CookieManager();
        CookieHandler.setDefault(cookieManager);
    }
    @Override
    public void run() {
        while (true){
            try {
                URL url = new URL(webUrl);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                int code = conn.getResponseCode();
                if (code == 200){
                    InputStreamReader reader = new InputStreamReader(conn.getInputStream());
                    BufferedReader bfReader = new BufferedReader(reader);
                    StringBuilder strBuilder = new StringBuilder();
                    String line;
                    while ((line = bfReader.readLine()) != null) {
                        strBuilder.append(line);
                    }
                    bfReader.close();
                    reader.close();
                    conn.disconnect();
                    JSONObject obj = new JSONObject(strBuilder.toString());
                    Message msg = new Message();
                    msg.obj = obj;
                    msg.what = 1;
                    handler.sendMessage(msg);
                }
                else {
                    conn.disconnect();
                    throw new Exception(code + "");
                }
                Thread.sleep(2000);
            }
            catch (Exception e){
                Log.e("web thread error", e.toString());
            }
        }
    }
}
