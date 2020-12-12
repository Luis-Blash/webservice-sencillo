package com.example.frontend.Interface;

import com.example.frontend.Model.Posts;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;

public interface TasksApi {

    // le decimos de que parte del url
    @GET("tasks")
    // se encara de buscar nuestros atributos en nuestro model/Posts
    // llama para webserver http reponse
    Call<List<Posts>> getPosts();
}
