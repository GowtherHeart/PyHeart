-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
create table internal(
	id int primary key generated always as identity,
	name name not null,
	value double precision not null default 0
);
CREATE UNIQUE INDEX uidx__internal__name on internal(name);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
drop index uidx__internal__name;
drop table internal;
-- +goose StatementEnd
