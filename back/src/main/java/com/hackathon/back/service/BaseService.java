package com.hackathon.back.service;

public interface BaseService <T>{
    T save(T entity);

    T findById(String id);

    void deleteById(String id);

    void update(T entity);
}
