namespace QuizServiceAPI.Models;

public class QuizServiceDatabaseSettings
{
    public string ConnectionString { get; set; } = null!;

    public string DatabaseName { get; set; } = null!;

    public string QuizCollectionName { get; set; } = null!;
    public string QuestionsCollectionName { get; set; } = null!;
    public string OptionsCollectionName { get; set; } = null!;
}