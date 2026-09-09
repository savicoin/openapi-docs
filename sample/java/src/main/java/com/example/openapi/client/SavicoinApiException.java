package com.example.openapi.client;

/**
 * Savicoin API 异常类
 */
public class SavicoinApiException extends Exception {
    
    public SavicoinApiException(String message) {
        super(message);
    }
    
    public SavicoinApiException(String message, Throwable cause) {
        super(message, cause);
    }
}
