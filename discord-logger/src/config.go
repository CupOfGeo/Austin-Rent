package main

import (
	"log"
	"os"
)

type Config struct {
	Environment string
	DBHost      string
	DBPass      string
}

// LoadConfig loads configuration from environment variables
// All secrets are already decrypted by GitHub Actions at deployment time
func LoadConfig() *Config {
	config := &Config{
		Environment: getEnv("ENVIRONMENT", "DEV"),
	}

	log.Printf("Config loaded for environment: %s", config.Environment)
	return config
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}