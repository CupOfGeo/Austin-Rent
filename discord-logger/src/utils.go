package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"

	"github.com/sirupsen/logrus"
)

func sendRequest(message DiscordMessage) {
	url := os.Getenv("DISCORD_URL")
	if url == "" {
		logrusLogger.Error("DISCORD_URL is not set")
		return
	}
	jsonData, err := json.Marshal(message)
	if err != nil {
		logrusLogger.Fatalf("Error marshaling JSON: %v", err)
		return
	}

	logrusLogger.WithFields(logrus.Fields{
		"jsonPayload": string(jsonData),
	}).Info("JSON Payload")

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		logrusLogger.Fatalf("Error creating request: %v", err)
		return
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logrusLogger.Fatalf("Error sending request: %v", err)
		return
	}
	defer resp.Body.Close()
}
