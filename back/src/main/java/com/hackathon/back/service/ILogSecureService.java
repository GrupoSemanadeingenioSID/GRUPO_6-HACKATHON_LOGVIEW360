package com.hackathon.back.service;

import com.hackathon.back.dto.LogSecureCheckDto;

import java.io.File;
import java.io.InputStream;
import java.util.List;

public interface ILogSecureService extends BaseService<LogSecureCheckDto>{
    List<LogSecureCheckDto> findAllByFile(InputStream filePath);
}
