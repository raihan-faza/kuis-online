package request

type QuizRequest struct {
	Recipient  string
	QuizName   string
	StartTime  string
	FinishTime string
}

type RegisterRequest struct {
	Recipient      string
	ActivationLink string
	AccessToken    string
	RefreshToken   string
}
