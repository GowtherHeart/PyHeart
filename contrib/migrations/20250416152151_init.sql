-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';


create table notes(
	id int primary key generated always as identity,
	name name not null,
	content varchar(1024),
	date_create timestamp without time zone not null default now(),
	date_update timestamp without time zone not null default now()
);

create table tasks(
	id int primary key generated always as identity,
	name name not null,
	content varchar(1024),
	complete boolean not null default false,
	date_create timestamp without time zone not null default now(),
	date_update timestamp without time zone not null default now()
);


-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
drop table notes;
drop table tasks;

-- +goose StatementEnd
