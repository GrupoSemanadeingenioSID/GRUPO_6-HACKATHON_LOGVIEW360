package com.hackathon.back.controller;

import com.hackathon.back.service.ILogSecureService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/logsecurecheck/")
public class LogSecureCheckController {

    private final ILogSecureService service;
    @GetMapping
    public ResponseEntity<Object> getall(@PageableDefault(size = 10,page = 0) Pageable pageable){
        return ResponseEntity.ok(service.findAll(pageable));
    }
}
