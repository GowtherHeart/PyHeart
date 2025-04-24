-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
CREATE UNIQUE INDEX uidx__notes__name on notes(name);
CREATE UNIQUE INDEX uidx__tasks__name on tasks(name);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP INDEX uidx__notes__name;
DROP INDEX uidx__tasks__name;
-- +goose StatementEnd
