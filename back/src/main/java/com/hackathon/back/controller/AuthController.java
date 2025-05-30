package com.hackathon.back.controller;

import com.hackathon.back.dto.UserDto;
import com.hackathon.back.util.JwtUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.User;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/auth/")
public class AuthController {
    private final JwtUtils jwtUtils;
    private final AuthenticationManager manager;

    @PostMapping("/login")
    public ResponseEntity<Object> login(@RequestBody UserDto dto){
        try{
            Authentication authentication = manager.authenticate(
                    new UsernamePasswordAuthenticationToken(dto.getUsername(), dto.getPassword())
            );
            User user = (User) authentication.getPrincipal();
            String token = jwtUtils.generateToken(user.getUsername());

            Map<String,Object> response = new HashMap<>();
            response.put("token", token);
            response.put("username", user.getUsername());
            return ResponseEntity.ok(response);
        }catch (Exception e){
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED.value()).body("Invalid credentials");
        }
    }

}
