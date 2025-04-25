<div align="center">
<img hight="300" width="700" alt="GIF" align="center" src="https://github.com/GowtherHeart/PyHeart/blob/main/_assets/1.gif">
</div>

### Directory Overview
1. **src/**: The main source directory containing all the application logic and components.
   - **cmd/**: Contains command-line and HTTP command implementations.
     - **cli/**: Implements CLI commands.
     - **http/**: Implements HTTP commands.
   - **config/**: Configuration-related modules.
   - **controllers/**: Handles the application's business logic and request processing.
     - **internal/**: Internal controllers for handling specific operations.
     - **notes/**: Controllers related to note operations.
     - **tasks/**: Controllers related to task operations.
   - **entity/**: Defines the data entities used throughout the application.
     - **db/**: Database-related entities.
       - **types/**: Type definitions for database entities.
   - **internal/**: Internal utilities and components.
     - **exception/**: Custom exception definitions.
     - **fastapi/**: FastAPI-related utilities.
   - **models/**: Data models for requests, responses, and database interactions.
     - **db/**: Database models.
     - **request/**: Request models.
     - **response/**: Response models.
   - **pkg/**: Package utilities and abstract base classes.
     - **abc/**: Abstract base classes for various components.
     - **context/**: Context management utilities.
     - **core/**: Core utilities and exceptions.
     - **driver/**: Database and cache drivers.
       - **postgres/**: PostgreSQL driver.
       - **redis/**: Redis driver.
     - **fastapi/**: FastAPI middleware and utilities.
     - **logging/**: Logging setup and configuration.
   - **repository/**: Data access layer for interacting with the database.
     - **_startup/**: Initialization queries.
     - **internal/**: Internal data access logic.
     - **notes/**: Data access logic for notes.
     - **tasks/**: Data access logic for tasks.
   - **usecase/**: Business logic and use case implementations.
