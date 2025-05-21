from starlette import status

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.tasks import TasksCustomTyping, TasksTyping
from src.internal.fastapi.controller import HttpController
from src.models.request import tasks as task_req
from src.models.response.tasks import TasksCoreRespModel
from src.pkg.abc.controller import router
from src.usecase.tasks import TasksV1US


class TasksCoreControllerV1(HttpController):
    """HTTP API controller for task management (version 1).

    This controller provides RESTful endpoints for complete task management including
    creation, retrieval, updating, and deletion operations. It follows REST conventions
    and integrates with the TasksV1US use case for business logic execution.

    The controller handles:
    - GET /tasks/ - Retrieve tasks with optional filtering and pagination
    - POST /tasks/ - Create new tasks
    - PATCH /tasks/ - Update existing tasks
    - DELETE /tasks/ - Delete tasks

    All endpoints return standardized responses using TasksCoreRespModel and handle
    appropriate HTTP status codes and error conditions.

    Attributes:
        prefix (str): URL prefix for all task endpoints ('/tasks')
        tags (list[str]): OpenAPI tags for documentation grouping

    Examples:
        # The controller is automatically registered with FastAPI
        # Endpoints are available at:
        # GET /v1/tasks/?limit=10&offset=0
        # POST /v1/tasks/ with JSON payload
        # PATCH /v1/tasks/ with JSON payload
        # DELETE /v1/tasks/?name=TaskName
    """

    prefix = "/tasks"
    tags = ["tasks"]

    @router(path="/", status_code=status.HTTP_200_OK)
    async def get(
        self,
        name: TasksCustomTyping.name = None,
        date_create: TasksCustomTyping.date_create = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> list[TasksCoreRespModel]:
        """Retrieve a list of tasks with optional filtering and pagination.

        This endpoint allows clients to retrieve tasks from the database with support for:
        - Optional filtering by name (partial or exact match)
        - Optional filtering by creation date
        - Pagination with configurable limit and offset
        - Default limit of 100 items per request

        The endpoint returns a list of tasks matching the specified criteria, sorted by
        creation date in descending order (newest first).

        Query Parameters:
            name (str, optional): Filter tasks by name. Supports partial matching.
                                 Example: ?name=deploy will match "Deploy to Production"
            date_create (datetime, optional): Filter tasks created on or after this date.
                                            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
            limit (int, optional): Maximum number of tasks to return. Default: 100, Max: 1000
            offset (int, optional): Number of tasks to skip for pagination. Default: 0

        Returns:
            list[TasksCoreRespModel]: Array of task objects containing:
                - name: The task's title/name
                - content: The task's description/details
                - complete: Boolean indicating if the task is completed
                - date_create: When the task was created (ISO 8601 format)
                - date_update: When the task was last updated (ISO 8601 format)
                - deleted: Boolean indicating if the task is soft-deleted

        Example Requests:
            GET /v1/tasks/                           # Get all tasks (first 100)
            GET /v1/tasks/?limit=10&offset=20        # Get 10 tasks starting from 21st
            GET /v1/tasks/?name=deploy               # Get tasks with 'deploy' in name
            GET /v1/tasks/?date_create=2024-01-01    # Get tasks created after Jan 1, 2024

        Example Response:
            [
                {
                    "name": "Deploy to Production",
                    "content": "Deploy version 2.1.0 to production environment",
                    "complete": false,
                    "date_create": "2024-01-15T10:30:00Z",
                    "date_update": "2024-01-15T10:30:00Z",
                    "deleted": false
                },
                {
                    "name": "Code Review",
                    "content": "Review pull request #123 for authentication feature",
                    "complete": true,
                    "date_create": "2024-01-14T15:45:00Z",
                    "date_update": "2024-01-14T16:20:00Z",
                    "deleted": false
                }
            ]
        """
        model = task_req.GetPrmModel(
            name=name,
            date_create=date_create,
            limit=limit,
            offset=offset,
        )
        result = await TasksV1US().get(model=model)
        return [TasksCoreRespModel(**e.model_dump()) for e in result]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: task_req.CreatePldModel) -> TasksCoreRespModel:
        """Create a new task with the provided data.

        This endpoint creates a new task in the database with the specified name and content.
        The task will be automatically assigned:
        - A unique identifier
        - Creation timestamp (current time)
        - Update timestamp (same as creation time)
        - Completion status (false by default)
        - Deleted status (false by default)

        The operation is performed within a database transaction to ensure consistency.

        Request Body (JSON):
            name (str, required): The title/name of the task.
                                 Must be between 1-255 characters.
                                 Example: "Deploy to Production"
            content (str, required): The task description/details.
                                   Can contain multiple lines and special characters.
                                   Example: "Deploy version 2.1.0 to production environment..."

        Returns:
            TasksCoreRespModel: The created task object containing:
                - name: The task's title/name
                - content: The task's description/details
                - complete: Always false for new tasks
                - date_create: When the task was created (ISO 8601 format)
                - date_update: When the task was created (same as date_create)
                - deleted: Always false for new tasks

        Status Codes:
            201: Task created successfully
            400: Invalid request data (missing required fields, validation errors)
            500: Internal server error during creation

        Example Request:
            POST /v1/tasks/
            Content-Type: application/json

            {
                "name": "Code Review",
                "content": "Review pull request #123 for authentication feature implementation"
            }

        Example Response (201):
            {
                "name": "Code Review",
                "content": "Review pull request #123 for authentication feature implementation",
                "complete": false,
                "date_create": "2024-01-15T14:30:00Z",
                "date_update": "2024-01-15T14:30:00Z",
                "deleted": false
            }
        """
        result = await TasksV1US().create(payload=payload)
        return TasksCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: task_req.UpdatePldModel) -> TasksCoreRespModel:
        """Update an existing task with new data.

        This endpoint updates an existing task by matching the provided name and updating
        its properties. The update operation:
        - Finds the task by exact name match
        - Updates the content and/or completion status
        - Sets the update timestamp to current time
        - Preserves the original creation timestamp
        - Maintains other existing properties

        The operation is performed within a database transaction to ensure consistency.

        Request Body (JSON):
            name (str, required): The exact name of the task to update.
                                 Must match an existing task's name exactly.
                                 Example: "Deploy to Production"
            content (str, required): The new description to replace existing content.
                                   Can contain multiple lines and special characters.
            complete (bool, optional): Whether the task is completed.
                                     If not provided, completion status remains unchanged.

        Returns:
            TasksCoreRespModel: The updated task object containing:
                - name: The task's title/name (unchanged)
                - content: The task's updated description
                - complete: Updated completion status
                - date_create: Original creation timestamp (unchanged)
                - date_update: When the task was updated (current timestamp)
                - deleted: Current deletion status (unchanged)

        Status Codes:
            200: Task updated successfully
            400: Invalid request data (missing required fields, validation errors)
            404: Task not found (no task with matching name)
            500: Internal server error during update

        Example Request:
            PATCH /v1/tasks/
            Content-Type: application/json

            {
                "name": "Code Review",
                "content": "Completed review of pull request #123 - approved with minor suggestions",
                "complete": true
            }

        Example Response (200):
            {
                "name": "Code Review",
                "content": "Completed review of pull request #123 - approved with minor suggestions",
                "complete": true,
                "date_create": "2024-01-15T14:30:00Z",
                "date_update": "2024-01-15T16:45:00Z",
                "deleted": false
            }
        """
        result = await TasksV1US().update(payload=payload)
        return TasksCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: TasksTyping.name) -> TasksCoreRespModel:
        """Soft delete a task by marking it as deleted.

        This endpoint performs a soft delete operation on a task, which means:
        - The task is not physically removed from the database
        - The 'deleted' flag is set to true
        - The task remains accessible for audit purposes
        - The task will be filtered out from normal retrieval operations
        - The update timestamp is set to the current time

        The operation finds the task by exact name match and marks it as deleted.

        Query Parameters:
            name (str, required): The exact name of the task to delete.
                                 Must match an existing task's name exactly.
                                 Example: ?name=Deploy to Production

        Returns:
            TasksCoreRespModel: The deleted task object containing:
                - name: The task's title/name (unchanged)
                - content: The task's description (unchanged)
                - complete: Current completion status (unchanged)
                - date_create: Original creation timestamp (unchanged)
                - date_update: When the task was deleted (current timestamp)
                - deleted: Set to true to indicate deletion

        Status Codes:
            200: Task deleted successfully
            400: Invalid request data (missing or invalid name parameter)
            404: Task not found (no task with matching name)
            500: Internal server error during deletion

        Example Request:
            DELETE /v1/tasks/?name=Code Review

        Example Response (200):
            {
                "name": "Code Review",
                "content": "Review pull request #123 for authentication feature",
                "complete": true,
                "date_create": "2024-01-15T14:30:00Z",
                "date_update": "2024-01-15T17:20:00Z",
                "deleted": true
            }

        Note:
            To permanently delete tasks, use the internal administrative endpoints
            or database maintenance procedures. This endpoint only performs soft deletion
            to maintain data integrity and audit trails.
        """
        model = task_req.DeletePrmModel(name=name)
        result = await TasksV1US().delete(model=model)
        return TasksCoreRespModel(**result.model_dump())
