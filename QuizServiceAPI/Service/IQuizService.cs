using System.Collections.Generic;
using System.Threading.Tasks;
using QuizServiceAPI.Models;

namespace QuizServiceAPI.Services
{
    public interface IQuizService
    {
        // Quiz methods
        Task<List<Quiz>> GetAsync();
        Task<List<Quiz>> GetByCreatorAsync(string userId);
        Task<Quiz?> GetAsync(string id);
        Task CreateAsync(Quiz newQuiz);
        Task UpdateAsync(string id, Quiz updatedQuiz);
        Task RemoveAsync(string id);

        // Question methods
        Task<Question?> GetQuestionAsync(string id);
        Task<List<Question>> GetQuestionsAsync(string quizId);
        Task CreateQuestionAsync(string id, Question newQuestion);
        Task UpdateQuestionAsync(string id, Question updatedQuestion);
        Task RemoveQuestionAsync(string id);

        // Option methods
        Task<Option?> GetOptionAsync(string id);
        Task<List<Option>> GetOptionsAsync(string questionId);
        Task CreateOptionAsync(string id, Option newOption);
        Task UpdateOptionAsync(string id, Option updatedOption);
        Task RemoveOptionAsync(string id);
    }
}






