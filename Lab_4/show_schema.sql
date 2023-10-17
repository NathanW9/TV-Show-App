create table Show (
 id	      integer primary key autoincrement,
 title 	varchar(64) not null,
 date  varchar(64) not null,
 description 	varchar(128),
 actorID		integer not null,
 producerID     integer not null,
    foreign key (actorID) references Actor(id),
    foreign key (producerID) references Producer(id)
);

create table  Actor (
    id          integer primary key autoincrement,
    firstname 	varchar(64) not null,
	lastname 	varchar(64) not null,
    age         varchar(64) not null
);

create table Producer (
    id          integer primary key autoincrement,
    firstname 	varchar(64) not null,
	lastname 	varchar(64) not null
);

create table ActorToShow (
	id	      integer primary key autoincrement,
 	actorID integer not null,
	showID  integer not null,
	foreign key (showID) references Show(id),
	foreign key (actorID) references Actor(id)
);

create table ProducerToShow (
	id	      integer primary key autoincrement,
 	producerID integer not null,
	showID  integer not null,
	foreign key (showID) references Show(id),
	foreign key (producerID) references Producer(id)
);