create table public.areas
(
    area_id   serial
        primary key,
    area_name text not null
);

alter table public.areas
    owner to admin;

create table public.employees
(
    employee_id   serial
        primary key,
    employee_name text not null,
    employee_age  integer,
    area_id       integer
        constraint fk_areas
            references public.areas
);

alter table public.employees
    owner to admin;

create table public.tasks
(
    task_id         serial
        primary key,
    task_name       text not null,
    completed       boolean,
    due_date        date,
    completion_date date,
    priority        integer,
    employee_id     integer
        constraint fk_employees
            references public.employees
);

alter table public.tasks
    owner to admin;

