using Xunit;
using Moq;
using Microsoft.AspNetCore.Mvc;
using QuizServiceAPI.Controllers;
using QuizServiceAPI.Models;
using QuizServiceAPI.Services;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using System.Linq;

namespace QuizServiceAPI.Tests
{
    public class QuizControllerTests
    {
        private readonly Mock<IQuizService> _mockQuizService;
        private readonly QuizController _controller;

        public QuizControllerTests()
        {
            _mockQuizService = new Mock<IQuizService>();
            _controller = new QuizController(_mockQuizService.Object);
        }

        [Fact]
        public async Task Get_ReturnsListOfQuizzes()
        {
            // Arrange
            var quizzes = new List<Quiz> { new Quiz { Id = "1", Name = "Test Quiz" } };
            _mockQuizService.Setup(service => service.GetAsync()).ReturnsAsync(quizzes);

            // Act
            var result = await _controller.Get();

            // Assert
            Assert.Equal(quizzes, result);
        }

        [Fact]
        public async Task Get_WithValidId_ReturnsQuiz()
        {
            // Arrange
            var quiz = new Quiz { Id = "1", Name = "Test Quiz" };
            _mockQuizService.Setup(service => service.GetAsync("1")).ReturnsAsync(quiz);

            // Act
            var result = await _controller.Get("1");

            // Assert
            var actionResult = Assert.IsType<ActionResult<Quiz>>(result);
            var okResult = Assert.IsType<OkObjectResult>(actionResult.Result);
            Assert.Equal(quiz, okResult.Value);
        }

        [Fact]
        public async Task Get_WithInvalidId_ReturnsNotFound()
        {
            // Arrange
            _mockQuizService.Setup(service => service.GetAsync("1")).ReturnsAsync((Quiz?)null);

            // Act
            var result = await _controller.Get("1");

            // Assert
            Assert.IsType<NotFoundResult>(result.Result);
        }

        [Fact]
        public async Task Update_WithValidQuiz_ReturnsNoContent()
        {
            // Arrange
            var quizId = "1";
            var existingQuiz = new Quiz { Id = quizId, Name = "Existing Quiz", CreatedBy = "user1" };
            var updatedQuiz = new Quiz { Id = quizId, Name = "Updated Quiz", CreatedBy = "user1" };

            _mockQuizService.Setup(service => service.GetAsync(quizId)).ReturnsAsync(existingQuiz);
            _mockQuizService.Setup(service => service.UpdateAsync(quizId, updatedQuiz)).Returns(Task.CompletedTask);

            var userClaims = new ClaimsPrincipal(new ClaimsIdentity(new Claim[]
            {
                new Claim("UserId", "user1")
            }, "mock"));

            _controller.ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext { User = userClaims }
            };

            // Act
            var result = await _controller.Update(quizId, updatedQuiz);

            // Assert
            Assert.IsType<NoContentResult>(result);
        }

        [Fact]
        public async Task Update_WithInvalidQuiz_ReturnsNotFound()
        {
            // Arrange
            var quizId = "1";
            var updatedQuiz = new Quiz { Id = quizId, Name = "Updated Quiz" };

            _mockQuizService.Setup(service => service.GetAsync(quizId)).ReturnsAsync((Quiz?)null);

            // Act
            var result = await _controller.Update(quizId, updatedQuiz);

            // Assert
            Assert.IsType<NotFoundResult>(result);
        }

        [Fact]
        public async Task Delete_WithValidQuiz_ReturnsNoContent()
        {
            // Arrange
            var quizId = "1";
            var existingQuiz = new Quiz { Id = quizId, Name = "Existing Quiz", CreatedBy = "user1" };

            _mockQuizService.Setup(service => service.GetAsync(quizId)).ReturnsAsync(existingQuiz);
            _mockQuizService.Setup(service => service.RemoveAsync(quizId)).Returns(Task.CompletedTask);

            var userClaims = new ClaimsPrincipal(new ClaimsIdentity(new Claim[]
            {
                new Claim("UserId", "user1")
            }, "mock"));

            _controller.ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext { User = userClaims }
            };

            // Act
            var result = await _controller.Delete(quizId);

            // Assert
            Assert.IsType<NoContentResult>(result);
        }

        [Fact]
        public async Task Delete_WithInvalidQuiz_ReturnsNotFound()
        {
            // Arrange
            var quizId = "1";

            _mockQuizService.Setup(service => service.GetAsync(quizId)).ReturnsAsync((Quiz?)null);

            // Act
            var result = await _controller.Delete(quizId);

            // Assert
            Assert.IsType<NotFoundResult>(result);
        }

        [Fact]
        public async Task Post_ValidQuiz_ReturnsCreatedAtAction()
        {
            // Arrange
            var userId = "user1";
            var newQuiz = new Quiz { Name = "New Quiz" };
            var userClaims = new ClaimsPrincipal(new ClaimsIdentity(new Claim[]
            {
                new Claim("UserId", userId)
            }, "mock"));

            _controller.ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext { User = userClaims }
            };

            _mockQuizService.Setup(service => service.CreateAsync(It.IsAny<Quiz>())).Returns(Task.CompletedTask);

            // Act
            var result = await _controller.Post(newQuiz);

            // Assert
            var actionResult = Assert.IsType<CreatedAtActionResult>(result);
            Assert.Equal(newQuiz, actionResult.Value);
            Assert.Equal(nameof(_controller.Get), actionResult.ActionName);
        }

        [Fact]
        public async Task Update_ValidQuiz_ReturnsNoContent()
        {
            // Arrange
            var quizId = "1";
            var userId = "user1";
            var existingQuiz = new Quiz { Id = quizId, Name = "Existing Quiz", CreatedBy = userId };
            var updatedQuiz = new Quiz { Id = quizId, Name = "Updated Quiz", CreatedBy = userId };

            _mockQuizService.Setup(service => service.GetAsync(quizId)).ReturnsAsync(existingQuiz);
            _mockQuizService.Setup(service => service.UpdateAsync(quizId, updatedQuiz)).Returns(Task.CompletedTask);

            var userClaims = new ClaimsPrincipal(new ClaimsIdentity(new Claim[]
            {
                new Claim("UserId", userId)
            }, "mock"));

            _controller.ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext { User = userClaims }
            };

            // Act
            var result = await _controller.Update(quizId, updatedQuiz);

            // Assert
            Assert.IsType<NoContentResult>(result);
        }

        [Fact]
        public async Task Delete_ValidQuiz_ReturnsNoContent()
        {
            // Arrange
            var quizId = "1";
            var userId = "user1";
            var existingQuiz = new Quiz { Id = quizId, Name = "Existing Quiz", CreatedBy = userId };

            _mockQuizService.Setup(service => service.GetAsync(quizId)).ReturnsAsync(existingQuiz);
            _mockQuizService.Setup(service => service.RemoveAsync(quizId)).Returns(Task.CompletedTask);

            var userClaims = new ClaimsPrincipal(new ClaimsIdentity(new Claim[]
            {
                new Claim("UserId", userId)
            }, "mock"));

            _controller.ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext { User = userClaims }
            };

            // Act
            var result = await _controller.Delete(quizId);

            // Assert
            Assert.IsType<NoContentResult>(result);
        }

        [Fact]
        public async Task GetOptions_ValidQuestionId_ReturnsOptions()
        {
            // Arrange
            var questionId = "q1";
            var options = new List<Option>
            {
                new Option { Id = "o1", Text = "Option 1", QuestionId = questionId },
                new Option { Id = "o2", Text = "Option 2", QuestionId = questionId }
            };

            _mockQuizService.Setup(service => service.GetOptionsAsync(questionId)).ReturnsAsync(options);

            // Act
            var result = await _controller.GetOptions(questionId);

            // Assert
            var actionResult = Assert.IsType<ActionResult<List<Option>>>(result);
            var okResult = Assert.IsType<OkObjectResult>(actionResult.Result);
            var returnedOptions = Assert.IsAssignableFrom<List<Option>>(okResult.Value);
            Assert.Equal(options.Count, returnedOptions.Count);
            Assert.Equal(questionId, returnedOptions[0].QuestionId); // Verify question ID
        }

        [Fact]
        public async Task GetOption_ValidQuestionIdAndOptionId_ReturnsOption()
        {
            // Arrange
            var questionId = "q1";
            var optionId = "o1";
            var option = new Option { Id = optionId, Text = "Option 1", QuestionId = questionId };

            _mockQuizService.Setup(service => service.GetQuestionAsync(questionId)).ReturnsAsync(new Question { Id = questionId });
            _mockQuizService.Setup(service => service.GetOptionAsync(optionId)).ReturnsAsync(option);

            // Act
            var result = await _controller.GetOption(questionId, optionId);

            // Assert
            var actionResult = Assert.IsType<ActionResult<Option>>(result);
            var okResult = Assert.IsType<OkObjectResult>(actionResult.Result);
            var returnedOption = Assert.IsType<Option>(okResult.Value);
            Assert.Equal(optionId, returnedOption.Id);
            Assert.Equal(questionId, returnedOption.QuestionId);
        }

        [Fact]
        public async Task PostOption_ValidQuestionIdAndOption_ReturnsCreatedAtAction()
        {
            // Arrange
            var questionId = "q1";
            var newOption = new Option { Text = "New Option" };

            _mockQuizService.Setup(service => service.GetQuestionAsync(questionId)).ReturnsAsync(new Question { Id = questionId });
            _mockQuizService.Setup(service => service.CreateOptionAsync(questionId, newOption)).Returns(Task.CompletedTask);

            // Act
            var result = await _controller.PostOption(questionId, newOption);

            // Assert
            var actionResult = Assert.IsType<CreatedAtActionResult>(result);
            Assert.Equal(newOption, actionResult.Value);
            Assert.Equal(nameof(_controller.GetOption), actionResult.ActionName);
        }

        [Fact]
        public async Task UpdateOption_ValidQuestionIdAndOptionId_ReturnsNoContent()
        {
            // Arrange
            var questionId = "q1";
            var optionId = "o1";
            var updatedOption = new Option { Id = optionId, Text = "Updated Option", QuestionId = questionId };
            var option = new Option { Id = optionId, Text = "Option 1", QuestionId = questionId };

            _mockQuizService.Setup(service => service.GetQuestionAsync(questionId)).ReturnsAsync(new Question { Id = questionId });
            _mockQuizService.Setup(service => service.GetOptionAsync(optionId)).ReturnsAsync(option);
            _mockQuizService.Setup(service => service.UpdateOptionAsync(optionId, updatedOption)).Returns(Task.CompletedTask);

            // Act
            var result = await _controller.UpdateOption(questionId, optionId, updatedOption);

            // Assert
            Assert.IsType<NoContentResult>(result);
        }

        [Fact]
        public async Task DeleteOption_ValidQuestionIdAndOptionId_ReturnsNoContent()
        {
            // Arrange
            var questionId = "q1";
            var optionId = "o1";
            var option = new Option { Id = optionId, Text = "Option 1", QuestionId = questionId };

            _mockQuizService.Setup(service => service.GetQuestionAsync(questionId)).ReturnsAsync(new Question { Id = questionId });
            _mockQuizService.Setup(service => service.GetOptionAsync(optionId)).ReturnsAsync(option);
            _mockQuizService.Setup(service => service.RemoveOptionAsync(optionId)).Returns(Task.CompletedTask);

            // Act
            var result = await _controller.DeleteOption(questionId, optionId);

            // Assert
            Assert.IsType<NoContentResult>(result);
        }
    }
}
