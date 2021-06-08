INSERT INTO "Customer" ("id","newsletter","newsletter_subscribed_on","newsletter_cancelled","language_code","verified","verification_token","verification_until","organisation_name","person_name","street","number","post_code","city","country_code","email_address","is_active") VALUES
	(1,1,'2021-01-01',0,'DE',1,'',NULL,'Kaninchenzüchter Plauen e.V.','Hans Müller','Holzweg','3','01234','Plauen','DE','hans.mueller@example.org',1),
	(2,1,'2021-05-01',0,'DE',1,'',NULL,'Gartensparte zum Spaten','Werner Schmidt','Am Wasser','7','01234','Plauen','DE','werner@example.org',1),
	(3,1,'2021-05-01',0,'DE',1,'',NULL,'Gartensparte Schneckenhain','Bernd Schmitz','Am Berg','2','01234','Plauen','DE','bernd.s@example.org',1),
	(4,1,'2021-05-01',0,'DE',1,'',NULL,'Sportverein Trimm Dich','Gunter Meier','An der Elster','22','01234','Plauen','DE','gunter.meier@example.org',1);
INSERT INTO "plan" ("id","periodLengthInMonths","currencyCode","costPerPeriod","noticePeriodTypeInDays","name") VALUES 
	(1,12,'EUR',50,14,'Basic'),
	(2,1,'EUR',5,7,'Mini'),
	(3,12,'EUR',300,14,'Pro');
INSERT INTO "instance" ("id","identifier","hostname","status","auto_renew","last_interaction","reserved_token","reserved_until","reserved_for_user_id","initial_password","port") VALUES
	(1,'344567','host0001','active',1,NULL,NULL,NULL,NULL,'',2000),
	(2,'238978','host0001','active',1,NULL,NULL,NULL,NULL,'',2001),
	(3,'785275','host0001','active',1,NULL,NULL,NULL,NULL,'',2002),
	(4,'862344','host0001','free',1,NULL,NULL,NULL,NULL,'',2003),
	(5,'119287','host0002','active',1,NULL,NULL,NULL,NULL,'',2000),
	(6,'239399','host0002','free',1,NULL,NULL,NULL,NULL,'',2001);
INSERT INTO "contract" ("id","start_date","end_date","auto_renew","customer_id","instance_id","plan_id") VALUES
	(1,'2021-06-05',NULL,1,1,1,2),
	(2,'2021-06-01',NULL,1,2,2,1),
	(3,'2021-06-01',NULL,1,3,3,1),
	(4,'2021-06-01',NULL,1,4,5,1);
