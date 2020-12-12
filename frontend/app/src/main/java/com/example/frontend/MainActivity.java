package com.example.frontend;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import com.example.frontend.Interface.TasksApi;
import com.example.frontend.Model.Posts;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    private TextView mJsonTxtView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // mi textview
        mJsonTxtView = findViewById(R.id.jsonText);
        // llamamos nuestro metodo
        getPosts();
    }

    // metodo para hacer get
    private void getPosts(){

        //creamos una instancia de retrofit
        // base url ira el url de nuestra api, sin donde lo tomara, eso hara nuestra interface/TasksApi
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.100.10:5000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        // llamamos nuestra interface
        TasksApi tasksApi = retrofit.create(TasksApi.class);
        Call<List<Posts>> call = tasksApi.getPosts();
        call.enqueue(new Callback<List<Posts>>() {
            @Override
            public void onResponse(Call<List<Posts>> call, Response<List<Posts>> response) {

                if(!response.isSuccessful()){
                    mJsonTxtView.setText("Codigo: "+response.code());
                    return;
                }

                List<Posts> postsList = response.body();

                for (Posts post: postsList) {
                    String content = "";
                    content += "id: " + post.getId() + "\n";
                    content += "title: " + post.getTitle() + "\n";
                    content += "description: " + post.getDescription() + "\n\n";
                    mJsonTxtView.append(content);
                }
            }

            @Override
            public void onFailure(Call<List<Posts>> call, Throwable t) {
                mJsonTxtView.setText(t.getMessage());
            }
        });

    }
}