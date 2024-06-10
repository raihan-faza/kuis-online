using QuizServiceAPI.Models;
using QuizServiceAPI.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

namespace QuizServiceAPI.Controllers;

[ApiController]
[Route("[controller]")]
public class QuizController : ControllerBase
{
    private readonly QuizService _quizService;

    public QuizController(QuizService quizService) =>
        _quizService = quizService;

    [HttpGet]
    public async Task<List<Quiz>> Get() =>
        await _quizService.GetAsync();


    [HttpGet("user-quiz")]
    [Authorize]
    public async Task<List<Quiz>> GetUserQuiz()
    {
        var userId = User.Claims.FirstOrDefault(c => c.Type == "UserId")?.Value;
        if (userId is null) userId = "";
        var quiz = await _quizService.GetByCreatorAsync(userId);
        return quiz;
    }

    [HttpGet("{id:length(24)}")]
    public async Task<ActionResult<Quiz>> Get(string id)
    {
        var quiz = await _quizService.GetAsync(id);

        if (quiz is null)
        {
            return NotFound();
        }

        return Ok(quiz);
    }

    [Authorize]
    [HttpPost]
    public async Task<IActionResult> Post(Quiz newQuiz)
    {
        var userId = User.Claims.FirstOrDefault(c => c.Type == "UserId")?.Value;
        newQuiz.CreatedBy = userId;

        await _quizService.CreateAsync(newQuiz);

        return CreatedAtAction(nameof(Get), new { id = newQuiz.Id }, newQuiz);
    }

    [Authorize]
    [HttpPut("{id:length(24)}")]
    public async Task<IActionResult> Update(string id, Quiz updatedQuiz)
    {
        var quiz = await _quizService.GetAsync(id);
        if (quiz is null) return NotFound();

        var userId = User.Claims.FirstOrDefault(c => c.Type == "UserId")?.Value;
        if (quiz.CreatedBy != userId) return Forbid();

        updatedQuiz.CreatedBy = quiz.CreatedBy;
        updatedQuiz.Id = quiz.Id;

        await _quizService.UpdateAsync(id, updatedQuiz);

        return NoContent();
    }

    [Authorize]
    [HttpDelete("{id:length(24)}")]
    public async Task<IActionResult> Delete(string id)
    {
        var quiz = await _quizService.GetAsync(id);
        if (quiz is null) return NotFound();

        var userId = User.Claims.FirstOrDefault(c => c.Type == "UserId")?.Value;
        if (quiz.CreatedBy != userId) return Forbid();

        await _quizService.RemoveAsync(id);

        return NoContent();
    }





    // Question

    [HttpGet("{quizId:length(24)}/question")]
    public async Task<List<Question>> GetQuestionsAsync(string quizId)
    {
        var questions = await _quizService.GetQuestionsAsync(quizId);
        foreach (var q in questions)
        {
            q.CorrectOptionId = null;
        }
        return questions;
    }

    [HttpGet("{quizId:length(24)}/question/{id:length(24)}")]
    public async Task<ActionResult<Question>> GetQuestion(string quizId, string id)
    {
        var quiz = await _quizService.GetAsync(quizId);

        if (quiz is null)
        {
            return NotFound();
        }

        var question = await _quizService.GetQuestionAsync(id);

        if (question is null)
        {
            return NotFound();
        }

        question.CorrectOptionId = null;

        return question;
    }

    [HttpPost("{quizId:length(24)}/question")]
    public async Task<IActionResult> PostQuestion(string quizId, Question newQuestion)
    {
        var quiz = await _quizService.GetAsync(quizId);

        if (quiz is null)
        {
            return NotFound();
        }

        await _quizService.CreateQuestionAsync(quizId, newQuestion);

        return CreatedAtAction(nameof(GetQuestion), new { id = newQuestion.Id, quizId = quizId }, newQuestion);
    }

    [HttpPut("{quizId:length(24)}/question/{id:length(24)}")]
    public async Task<IActionResult> UpdateQuestion(string quizId, string id, Question updatedQuestion)
    {
        var quiz = await _quizService.GetAsync(quizId);

        if (quiz is null)
        {
            return NotFound();
        }

        var question = await _quizService.GetQuestionAsync(id);

        if (question is null)
        {
            return NotFound();
        }

        if (question.QuizId != quizId)
        {
            return BadRequest();
        }

        updatedQuestion.Id = question.Id;
        updatedQuestion.QuizId = quizId;

        await _quizService.UpdateQuestionAsync(id, updatedQuestion);

        return NoContent();
    }

    [HttpDelete("{quizId:length(24)}/question/{id:length(24)}")]
    public async Task<IActionResult> DeleteQuestion(string quizId, string id)
    {
        var quiz = await _quizService.GetAsync(quizId);

        if (quiz is null)
        {
            return NotFound();
        }

        var question = await _quizService.GetQuestionAsync(id);

        if (question is null)
        {
            return NotFound();
        }

        if (question.QuizId != quizId)
        {
            return BadRequest();
        }

        await _quizService.RemoveQuestionAsync(id);

        return NoContent();
    }











    // Option

    [HttpGet("{questionId:length(24)}/option")]
    public async Task<List<Option>> GetOptions(string questionId)
    {
        var options = await _quizService.GetOptionsAsync(questionId);
        return options;
    }

    [HttpGet("{questionId:length(24)}/option/{id:length(24)}")]
    public async Task<ActionResult<Option>> GetOption(string questionId, string id)
    {
        var question = await _quizService.GetQuestionAsync(questionId);

        if (question is null)
        {
            return NotFound();
        }

        var option = await _quizService.GetOptionAsync(id);

        if (option is null)
        {
            return NotFound();
        }


        return option;
    }

    [HttpPost("{questionId:length(24)}/option")]
    public async Task<IActionResult> PostOption(string questionId, Option newOption)
    {
        var question = await _quizService.GetQuestionAsync(questionId);

        if (question is null)
        {
            return NotFound();
        }

        await _quizService.CreateOptionAsync(questionId, newOption);

        return CreatedAtAction(nameof(GetOption), new { id = newOption.Id, questionId = questionId }, newOption);
    }

    [HttpPut("{questionId:length(24)}/option/{id:length(24)}")]
    public async Task<IActionResult> UpdateOption(string questionId, string id, Option updatedOption)
    {
        var question = await _quizService.GetQuestionAsync(questionId);

        if (question is null)
        {
            return NotFound();
        }

        var option = await _quizService.GetOptionAsync(id);

        if (option is null)
        {
            return NotFound();
        }


        if (option.QuestionId != questionId)
        {
            return BadRequest();
        }

        updatedOption.Id = option.Id;
        updatedOption.QuestionId = questionId;

        await _quizService.UpdateOptionAsync(id, updatedOption);

        return NoContent();
    }

    [HttpDelete("{questionId:length(24)}/option/{id:length(24)}")]
    public async Task<IActionResult> DeleteOption(string questionId, string id)
    {
        var question = await _quizService.GetQuestionAsync(questionId);

        if (question is null)
        {
            return NotFound();
        }

        var option = await _quizService.GetOptionAsync(id);

        if (option is null)
        {
            return NotFound();
        }

        if (option.QuestionId != questionId)
        {
            return BadRequest();
        }

        await _quizService.RemoveOptionAsync(id);

        return NoContent();
    }









    // Answer

    [HttpGet("{quizId:length(24)}/answer")]
    public async Task<List<Question>> GetAnswersAsync(string quizId)
    {
        var questions = await _quizService.GetQuestionsAsync(quizId);
        return questions;
    }

    [HttpGet("{quizId:length(24)}/answer/{id:length(24)}")]
    public async Task<ActionResult<Question>> GetAnswer(string quizId, string id)
    {
        var quiz = await _quizService.GetAsync(quizId);

        if (quiz is null)
        {
            return NotFound();
        }

        var question = await _quizService.GetQuestionAsync(id);

        if (question is null)
        {
            return NotFound();
        }

        return question;
    }
}