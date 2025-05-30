package com.hackathon.back.controller;

import com.hackathon.back.service.IMidFlowLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/api/v1/midflowlog/")
@RestController
@RequiredArgsConstructor
public class LogMidFlowController {
    private final IMidFlowLogService midFlowLogService;

    @GetMapping
    public ResponseEntity<Object> getAll(@PageableDefault(size = 10,page = 0) Pageable pageable){
        return ResponseEntity.ok(midFlowLogService.findAll(pageable));
    }
}
