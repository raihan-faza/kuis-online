using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace QuizServiceAPI.Models;

public class Quiz
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }

    [BsonElement("Name")]
    public string? Name { get; set; }

    public string? Description { get; set; }

    public int DurationMinute { get; set; }

    public DateTime OpenTime { get; set; }

    public DateTime CloseTime { get; set; }
    public string? CreatedBy { get; set; }
}