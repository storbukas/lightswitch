package no.storbukas.lightswitch;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.text.Html;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;

/**
 * @authors Lars Erik Storbukås, Ole Eirik Heggelund
 * @mails larserik.storbukas@gmail.com, oeheggel@gmail.com
 * @date_changed 21/05 - 2015
 * @course INF219 Informatics Project
 * @description Main Activity
 *
 **/
public class MainActivity extends ActionBarActivity {
    final Context context = this;
    public String IP; //= "192.168.0.101";
    private Client tcpClient;
    public static final String PREFS_NAME = "SavedIP";

    // small change, just for testing

    public String text = "";

    private Switch[] buttons = new Switch[6];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Restore preferences
        SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
        String ip = settings.getString("IP", "10.0.0.100");
        this.IP = ip;

        ActionBar actionBar = getSupportActionBar();
        actionBar.setLogo(R.drawable.lightbulb_nobackground);
        actionBar.setDisplayUseLogoEnabled(true);
        actionBar.setDisplayShowHomeEnabled(true);

        buttons[0] = (Switch) findViewById(R.id.switch1);
        buttons[1] = (Switch) findViewById(R.id.switch2);
        buttons[2] = (Switch) findViewById(R.id.switch3);
        buttons[3] = (Switch) findViewById(R.id.switch4);
        buttons[4] = (Switch) findViewById(R.id.switch5);
        buttons[5] = (Switch) findViewById(R.id.switch6);

        new connectTask().execute("");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) { // TODO change to something sensible
            changeIP();
            return true;
        }
        if(id == R.id.action_refresh) {
            tcpClient.sendMessage("info");
            return true;
        }
        if(id == R.id.action_disconnect) {
            tcpClient.stopClient();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void onToggleClicked(View view) {
        // Is the toggle on?
        boolean action = ((Switch) view).isChecked();

        int button_nr = 0;
        for(int i = 0; i < 6; i++) {
            if(view == buttons[i]) {
                button_nr = i;
                break;
            }
        }

        toggleSwitch(button_nr+1, action);
    }

    public void toggleSwitch(int switch_nr, boolean action) {
        // turns the respective switch on/off
        String on_off = "off";
        if(action) on_off = "on";

        tcpClient.sendMessage(on_off + " " + switch_nr);
    }

    public void turnON(View view) {
        for(Switch button : buttons) {
            button.setChecked(true);
        }

        tcpClient.sendMessage("on all");
    }

    public void turnOFF(View view) {
        for(Switch button : buttons) {
            button.setChecked(false);
        }
        tcpClient.sendMessage("off all");
    }

    public void changeIP() {
        startupDialog();
    }

    protected void startupDialog() {
        PromptDialog dlg = new PromptDialog(MainActivity.this, R.string.title, R.string.comment) {
            @Override
            public boolean onOkClicked(String input) {
                IP = input;

                // We need an Editor object to make preference changes.
                // All objects are from android.context.Context
                SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
                SharedPreferences.Editor editor = settings.edit();
                editor.putString("IP", input);

                // Commit the edits!
                editor.commit();

                Context context = getApplicationContext();
                CharSequence text = input;
                int duration = Toast.LENGTH_SHORT;

                Toast toast = Toast.makeText(context, text, duration);
                toast.show();

                return true; // true = close dialog
            }
        };
        dlg.show();
    }

    public class connectTask extends AsyncTask<String,String,Client> {

        @Override
        protected Client doInBackground(String... message) {

            //we create a TCPClient object and
            tcpClient = new Client(new Client.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    publishProgress(message);
                }
            });
            tcpClient.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);

            Log.i("Light Switch", "Message received " + values[0]);
            int i = 0;
            for(char value : values[0].toCharArray()) {
                if(value == '|') continue;
                boolean action = (value == '1') ? true : false;
                buttons[i++].setChecked(action);
            }
        }
    }
}