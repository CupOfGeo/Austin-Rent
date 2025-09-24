package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)

}

func messageHandler(w http.ResponseWriter, r *http.Request) {
	var msgReq MessageRequest
	if err := json.NewDecoder(r.Body).Decode(&msgReq); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	fields := make([]EmbedField, 0, len(msgReq.Fields))
	for k, v := range msgReq.Fields {
		fields = append(fields, EmbedField{Name: k, Value: v, Inline: false})
	}

	logExplorerURL := fmt.Sprintf(
		"https://console.cloud.google.com/logs/query;query=resource.type%%20%%3D%%20%%22cloud_run_revision%%22%%0Aresource.labels.service_name%%20%%3D%%20%%22%s%%22%%0Aresource.labels.location%%20%%3D%%20%%22us-central1%%22%%0A%%20severity%%3E%%3DDEFAULT%%0A%%20;storageScope=project;cursorTimestamp=%s;customDuration=today?project=austin-rent",
		msgReq.AppName,
		msgReq.Timestamp.Format(time.RFC3339),
	)

	message := DiscordMessage{
		Content:  "Austin Rent Logger",
		Username: "Captain Hook",
		Embeds: []Embed{
			{
				Title:       msgReq.Title,
				Description: msgReq.Description,
				URL:         logExplorerURL,
				Color:       msgReq.Color,
				Fields:      fields,
				Author: EmbedAuthor{
					Name:    msgReq.AppName,
					URL:     fmt.Sprintf("https://console.cloud.google.com/run/detail/us-central1/%s/metrics?project=austin-rent", msgReq.AppName),
					IconURL: "",
				},
				Thumbnail: EmbedThumbnail{URL: "https://example.com/thumbnail.png"},
				Image:     EmbedImage{URL: "https://example.com/image.png"},
				Footer:    EmbedFooter{Text: "Footer Text", IconURL: ""},
				Timestamp: msgReq.Timestamp.Format(time.RFC3339),
			},
		},
		AllowedMentions: AllowedMentions{
			Parse: []string{"everyone"},
		},
	}

	sendRequest(message)
	w.WriteHeader(http.StatusOK)
	logrusLogger.Info("Message sent")
}
