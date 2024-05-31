package controller

import (
	"log"
	"net/smtp"
	"notification/initializer"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
}

func SendNotification(recipient string, subject string, message string) {
	sender := os.Getenv("SENDER_NAME")
	auth := initializer.SetupSMTP()
	msg := "From: " + sender + "\n" +
		"To: " + strings.Join([]string{recipient}, ",") + "\n" +
		"Subject: " + subject + "\n\n" + message
	smtp.SendMail(recipient, auth, sender, []string{recipient}, []byte(msg))
}
