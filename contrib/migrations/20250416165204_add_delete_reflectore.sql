-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
alter table notes add column deleted boolean not null default false;
alter table tasks add column deleted boolean not null default false;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
alter table notes drop column deleted;
alter table tasks drop column deleted;
-- +goose StatementEnd
