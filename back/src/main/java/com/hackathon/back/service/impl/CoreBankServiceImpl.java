package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogCoreBankDto;
import com.hackathon.back.repository.CoreBankLogJpaRepository;
import com.hackathon.back.service.ICoreBankLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CoreBankServiceImpl implements ICoreBankLogService {

    private final CoreBankLogJpaRepository jpaRepository;

    @Override
    public LogCoreBankDto save(LogCoreBankDto entity) {
        return null;
    }

    @Override
    public LogCoreBankDto findById(String id) {
        return null;
    }

    @Override
    public void deleteById(String id) {

    }

    @Override
    public void update(LogCoreBankDto entity) {

    }
}
