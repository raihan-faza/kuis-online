package controller

import (
	"fmt"
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
	smtp_host := os.Getenv("HOST")
	smtp_port := os.Getenv("PORT")
	auth := initializer.SetupSMTP()
	msg := "From: " + sender + "\n" +
		"To: " + strings.Join([]string{recipient}, ",") + "\n" +
		"Subject: " + subject + "\n\n" + message
	host := fmt.Sprintf("%s:%s", smtp_host, smtp_port)
	smtp.SendMail(host, auth, sender, []string{recipient}, []byte(msg))
}
