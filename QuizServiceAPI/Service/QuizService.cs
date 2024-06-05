using QuizServiceAPI.Models;
using Microsoft.Extensions.Options;
using MongoDB.Driver;
using MongoDB.Bson;

namespace QuizServiceAPI.Services;

public class QuizService
{
    private readonly IMongoCollection<Quiz> _quizCollection;
    private readonly IMongoCollection<Question> _questionsCollection;
    private readonly IMongoCollection<Option> _optionsCollection;

    public QuizService(
        IOptions<QuizServiceDatabaseSettings> quizServiceDatabaseSettings)
    {
        var mongoClient = new MongoClient(
            quizServiceDatabaseSettings.Value.ConnectionString);

        var mongoDatabase = mongoClient.GetDatabase(
            quizServiceDatabaseSettings.Value.DatabaseName);

        _quizCollection = mongoDatabase.GetCollection<Quiz>(
            quizServiceDatabaseSettings.Value.QuizCollectionName);

        _questionsCollection = mongoDatabase.GetCollection<Question>(
            quizServiceDatabaseSettings.Value.QuestionsCollectionName);

        _optionsCollection = mongoDatabase.GetCollection<Option>(
            quizServiceDatabaseSettings.Value.OptionsCollectionName);
    }

    // Quiz

    public async Task<List<Quiz>> GetAsync() =>
        await _quizCollection.Find(_ => true).ToListAsync();

    public async Task<List<Quiz>> GetByCreatorAsync(string userId) =>
        await _quizCollection.Find(x => x.CreatedBy == userId).ToListAsync();

    public async Task<Quiz?> GetAsync(string id) =>
        await _quizCollection.Find(x => x.Id == id).FirstOrDefaultAsync();

    public async Task CreateAsync(Quiz newQuiz)
    {
        await _quizCollection.InsertOneAsync(newQuiz);
    }

    public async Task UpdateAsync(string id, Quiz updatedQuiz) =>
        await _quizCollection.ReplaceOneAsync(x => x.Id == id, updatedQuiz);

    public async Task RemoveAsync(string id) =>
        await _quizCollection.DeleteOneAsync(x => x.Id == id);





    // Question
    public async Task<Question?> GetQuestionAsync(string id) =>
        await _questionsCollection.Find(x => x.Id == id).FirstOrDefaultAsync();

    public async Task<List<Question>> GetQuestionsAsync(string quizId) =>
        await _questionsCollection.Find(x => x.QuizId == quizId).ToListAsync();

    public async Task CreateQuestionAsync(string id, Question newQuestion)
    {
        newQuestion.QuizId = id;
        await _questionsCollection.InsertOneAsync(newQuestion);
    }

    public async Task UpdateQuestionAsync(string id, Question updatedQuestion)
    {
        await _questionsCollection.ReplaceOneAsync(x => x.Id == id, updatedQuestion);
    }

    public async Task RemoveQuestionAsync(string id) =>
        await _questionsCollection.DeleteOneAsync(x => x.Id == id);





    // Option
    public async Task<Option?> GetOptionAsync(string id) =>
        await _optionsCollection.Find(x => x.Id == id).FirstOrDefaultAsync();

    public async Task<List<Option>> GetOptionsAsync(string questionId) =>
        await _optionsCollection.Find(x => x.QuestionId == questionId).ToListAsync();

    public async Task CreateOptionAsync(string id, Option newOption)
    {
        newOption.QuestionId = id;
        await _optionsCollection.InsertOneAsync(newOption);
    }

    public async Task UpdateOptionAsync(string id, Option updatedOption) =>
        await _optionsCollection.ReplaceOneAsync(x => x.Id == id, updatedOption);

    public async Task RemoveOptionAsync(string id) =>
        await _optionsCollection.DeleteOneAsync(x => x.Id == id);
}