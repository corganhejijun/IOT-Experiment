package com.android.corgan.myiotapp;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;
import android.os.Handler;
import android.os.Message;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {
    Handler webHandler;
    WebThread webThread;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_activity);
        final TextView view_t = (TextView)findViewById(R.id.temperature);
        view_t.setText("当前温度：无数据");
        final TextView view_h = findViewById(R.id.humidity);
        view_h.setText("当前湿度：无数据");
        webHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                try {
                    switch (msg.what){
                        case 1:
                            JSONObject obj = (JSONObject)msg.obj;
                            double temperature = obj.getDouble("t");
                            double humidity = obj.getDouble("h");
                            view_h.setText("当前湿度：" + humidity);
                            view_t.setText("当前温度：" + temperature);
                            break;
                        default: break;
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        };
        webThread = new WebThread("http://192.168.2.131:8000/data?recv", webHandler);
        Thread thread = new Thread(webThread);
        thread.start();
    }
}
