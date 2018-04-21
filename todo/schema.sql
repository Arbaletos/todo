drop table if exists tasks;
create table tasks (
  id integer primary key autoincrement,
  task text not null,
  done integer
);