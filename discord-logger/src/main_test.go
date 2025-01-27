package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestMessageHandler(t *testing.T) {
	// Create a sample request payload
	msgReq := MessageRequest{
		Title:       "Test Title",
		Description: "Test Description",
		AppName:     "Test App",
		Color:       16711680, // Red color
		Timestamp:   time.Now(),
		Fields: map[string]string{
			"Field1": "Value1",
			"Field2": "Value2",
		},
	}

	jsonData, err := json.Marshal(msgReq)
	if err != nil {
		t.Fatalf("Error marshaling JSON: %v", err)
	}

	// Create a new HTTP request
	req, err := http.NewRequest("POST", "/message", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Fatalf("Error creating request: %v", err)
	}

	// Create a ResponseRecorder to record the response
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(messageHandler)

	// Call the handler with the ResponseRecorder and request
	handler.ServeHTTP(rr, req)

	// Check the status code
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	// // Check the response body
	// expected := "Message sent\n"
	// if rr.Body.String() != expected {
	// 	t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
	// }
}
