package com.hackathon.back.service;

import org.springframework.data.domain.Pageable;

import java.util.List;

public interface BaseService <T>{
    T save(T entity);

    T findById(String id);

    void deleteById(String id);

    void update(T entity);

    List<T> findAll(Pageable pageable);
}
