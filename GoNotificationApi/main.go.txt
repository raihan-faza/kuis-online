package main

import (
	"log"
	"notification/controller"

	"github.com/joho/godotenv"
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
}
func main() {
	controller.ScheduleMail("limectf@gmail.com", "test", "testing schduling", 2024, 06, 07, 16, 24, 00)
	//select {}
	//controller.SendNotification("limectf@gmail.com", "test", "testing notification")
	/*
		sender := os.Getenv("SENDER_NAME")
		username := os.Getenv("SENDER_EMAIL")
		password := os.Getenv("APP_PASSWORD")
		//host := os.Getenv("HOST")
		auth := smtp.PlainAuth("", username, password, "smtp.gmail.com")
		recipient := "limectf@gmail.com"
		subject := "test"
		message := "init"
		msg := "From: " + sender + "\n" +
			"To: " + strings.Join([]string{recipient}, ",") + "\n" +
			"Subject: " + subject + "\n\n" + message
		smtp.SendMail("smtp.gmail.com:587", auth, sender, []string{recipient}, []byte(msg))
	*/
	select {}
}
