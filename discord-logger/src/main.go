package main

import (
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"

	"github.com/sirupsen/logrus"
)

var logrusLogger = logrus.New()

func init() {
	logrusLogger.Out = os.Stdout
	logrusLogger.SetFormatter(&logrus.JSONFormatter{
		FieldMap: logrus.FieldMap{
			logrus.FieldKeyLevel: "severity",
			logrus.FieldKeyMsg:   "message",
		},
	})
	logrusLogger.SetLevel(logrus.InfoLevel)
}

// func doLogrusExample() {
// 	logrusLogger.WithFields(logrus.Fields{
// 		"stringKey":  "string value",
// 		"intKey":     123,
// 		"floatKey":   3.1415,
// 		"booleanKey": false,
// 		"mapKey":     []int{123, 456},
// 	}).Warn("logrus list message JSON")

// 	logrusLogger.Warn("logrus list message text")
// }

func main() {
	err := godotenv.Load(".env")
	if err != nil {
		logrusLogger.Fatalf("Failed to create logging client: %v", err)
	}
	r := mux.NewRouter()
	r.HandleFunc("/health", healthHandler).Methods("GET")
	r.HandleFunc("/message", messageHandler).Methods("POST")

	logrusLogger.Info("Server is listening on port 8080...")
	if err := http.ListenAndServe(":8080", r); err != nil {
		logrusLogger.Fatalf("Failed to start server: %v", err)
	}
}
