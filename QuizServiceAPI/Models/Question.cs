using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace QuizServiceAPI.Models;

public class Question
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }

    public string? Prompt { get; set; }

    [BsonRepresentation(BsonType.ObjectId)]
    public string? CorrectOptionId { get; set; }

    [BsonRepresentation(BsonType.ObjectId)]
    public string? QuizId { get; set; }
}