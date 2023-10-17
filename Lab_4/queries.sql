select * from Producer
join Show on Show.producerID = Producer.id
where Producer.firstname like "Zack";

insert into Actor
(firstname, lastname, age)
values
("Dominic","Purcell","53");

select a.firstname, p.firstname
from Show s
join Actor a on s.actorID = a.ID
join Producer p on s.producerID = p.ID
where s.title = 'Money Heist';