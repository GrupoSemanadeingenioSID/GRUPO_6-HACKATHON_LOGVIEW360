package com.hackathon.back.controller;

import com.hackathon.back.service.ICoreBankLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class CoreBankLogController {
    private final ICoreBankLogService service;


}
