using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace QuizServiceAPI.Models;

public class Option
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }
    public string? Text { get; set; }

    [BsonRepresentation(BsonType.ObjectId)]
    public string? QuestionId { get; set; }
}