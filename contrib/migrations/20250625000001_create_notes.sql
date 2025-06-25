-- +goose Up
-- +goose StatementBegin
SELECT 'Creating notes table';

CREATE TABLE notes (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    content TEXT,
    date_create TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_update TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create unique index on name for non-deleted notes
CREATE UNIQUE INDEX uidx__notes__name ON notes(name) WHERE deleted = FALSE;

-- Create index for better query performance on date_create
CREATE INDEX idx__notes__date_create ON notes(date_create);

-- Create index for filtering deleted records
CREATE INDEX idx__notes__deleted ON notes(deleted);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'Dropping notes table';

DROP INDEX IF EXISTS idx__notes__deleted;
DROP INDEX IF EXISTS idx__notes__date_create;
DROP INDEX IF EXISTS uidx__notes__name;
DROP TABLE IF EXISTS notes;

-- +goose StatementEnd
