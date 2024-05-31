package main

import (
	"fmt"
	"net/http"
	"notification/controller"
	"notification/initializer"
	"notification/request"

	"github.com/gin-gonic/gin"
)

func init() {
	initializer.SetupSMTP()
}

func main() {
	r := gin.Default()

	r.POST("/notif/quiz/created", func(ctx *gin.Context) {
		var request request.QuizRequest
		err := ctx.BindJSON(&request)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, gin.H{
				"message": "Bad Request",
			})
			return
		}
		subject := "Quiz Created"
		msg := fmt.Sprintf(`
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Hi %s</h1>
			<h2>Your quiz with the name of %s succesfully created. Here's the details</h2>
            <p>Quiz Name: %s</p>
            <p>Start Time: %s</p>
            <p>Stop Time: %s</p>
        </body>
        </html>
    `, request.Recipient, request.QuizName, request.QuizName, request.StartTime, request.StartTime)
		controller.SendNotification(request.Recipient, subject, msg)
		ctx.JSON(http.StatusOK, gin.H{
			"message": "Notification Sent",
		})

	})

	r.POST("/notif/auth/registration", func(ctx *gin.Context) {
		var request request.QuizRequest
		err := ctx.BindJSON(&request)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, gin.H{
				"message": "Bad Request",
			})
			return
		}
		subject := "Quiz Created"
		msg := fmt.Sprintf(`
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Hi %s</h1>
			<h2>You have been enrolled in a quiz. Here's the details</h2>
            <p>Quiz Name: %s</p>
            <p>Start Time: %s</p>
            <p>Stop Time: %s</p>
        </body>
        </html>
    `, request.Recipient, request.QuizName, request.StartTime, request.StartTime)
		controller.SendNotification(request.Recipient, subject, msg)
		ctx.JSON(http.StatusOK, gin.H{
			"message": "Notification Sent",
		})

	})
	r.POST("/notif/quiz/reminder", func(ctx *gin.Context) {
		var request request.QuizRequest
		err := ctx.BindJSON(&request)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, gin.H{
				"message": "Bad Request",
			})
			return
		}
		subject := "Quiz Created"
		msg := fmt.Sprintf(`
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Hi %s</h1>
			<h2>Don't forget you have quiz soon. Here's the details</h2>
            <p>Quiz Name: %s</p>
            <p>Start Time: %s</p>
            <p>Stop Time: %s</p>
        </body>
        </html>
    `, request.Recipient, request.QuizName, request.StartTime, request.StartTime)
		controller.SendNotification(request.Recipient, subject, msg)
		ctx.JSON(http.StatusOK, gin.H{
			"message": "Notification Sent",
		})

	})
	r.POST("/notif/register/verification", func(ctx *gin.Context) {
		var request request.RegisterRequest
		err := ctx.BindJSON(&request)
		if err != nil {
			ctx.JSON(http.StatusBadRequest, gin.H{
				"message": "Bad Request",
			})
			return
		}
		subject := "Quiz Created"
		msg := fmt.Sprintf(`
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Hi %s</h1>
			<h2>Dont share the token with anybody. Clink the link to activate your account. </h2>
            <p>Activation Link: %s</p>
            <p>Access Token: %s</p>
            <p>Refresh Token: %s</p>
        </body>
        </html>
    `, request.Recipient, request.ActivationLink, request.AccessToken, request.RefreshToken)
		controller.SendNotification(request.Recipient, subject, msg)
		ctx.JSON(http.StatusOK, gin.H{
			"message": "Notification Sent",
		})

	})
	r.Run()
}
