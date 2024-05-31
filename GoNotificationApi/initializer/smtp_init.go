package initializer

import (
	"log"
	"net/smtp"
	"os"

	"github.com/joho/godotenv"
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

}
func SetupSMTP() smtp.Auth {
	username := os.Getenv("SENDER_EMAIL")
	password := os.Getenv("APP_PASSWORD")
	host := os.Getenv("HOST")
	auth := smtp.PlainAuth("", username, password, host)
	return auth
}
