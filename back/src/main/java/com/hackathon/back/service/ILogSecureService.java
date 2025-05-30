package com.hackathon.back.service;

import com.hackathon.back.dto.LogSecureCheckDto;

import java.util.List;

public interface ILogSecureService extends BaseService<LogSecureCheckDto>{
    List<LogSecureCheckDto> findAllByFile(String filePath);
}
