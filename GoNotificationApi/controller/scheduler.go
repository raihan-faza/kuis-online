package controller

import (
	"time"
)

func ScheduleMail(recipient string, subject string, message string, year int, date int, day int, hour int, minute int, second int) {
	Jakarta, err := time.LoadLocation("Asia/Jakarta")
	if err != nil {
		panic(err)
	}
	send_time := time.Date(year, time.Month(date), day, hour, minute, second, 0, Jakarta)
	now := time.Now().In(Jakarta)
	delay := send_time.Sub(now)

	go func() {
		time.Sleep(delay)
		SendNotification(recipient, subject, message)
	}()
}
