-- password is: Test1234!
INSERT INTO auth_user ('id','password','is_superuser', 'is_staff', 'username', 'email', 'is_active', 'first_name', 'last_name', 'date_joined') VALUES
    (2,'pbkdf2_sha256$260000$gbppPUYGKnb6W0o7w1CVW1$PR01ycCSgSGyQWek6UjFyDDky00mZWLKbm1QrGBAcxE=',0,0,'customer1','hans.mueller@example.org',1,'','',date('now')),
    (3,'pbkdf2_sha256$260000$gbppPUYGKnb6W0o7w1CVW1$PR01ycCSgSGyQWek6UjFyDDky00mZWLKbm1QrGBAcxE=',0,0,'customer2','werner@example.org',1,'','',date('now')),
    (4,'pbkdf2_sha256$260000$gbppPUYGKnb6W0o7w1CVW1$PR01ycCSgSGyQWek6UjFyDDky00mZWLKbm1QrGBAcxE=',0,0,'customer3','bernd.s@example.org',1,'','',date('now')),
    (5,'pbkdf2_sha256$260000$gbppPUYGKnb6W0o7w1CVW1$PR01ycCSgSGyQWek6UjFyDDky00mZWLKbm1QrGBAcxE=',0,0,'customer4','gunter.meier@example.org',1,'','',date('now'));
INSERT INTO "saas_product" ("id", "slug", "name", "activationurl", "is_active") VALUES
	(1, "kanboard", "Kanboard", "https://kanboard.example.org/activate", 1);
INSERT INTO "saas_plan" ("id","product_id","periodLengthInMonths","currencyCode","costPerPeriod","noticePeriodInDays","name","language","descr_target","descr_caption","descr_1","descr_2","descr_3","descr_4") VALUES
	(1,1,12,'EUR',50,14,'Basic','DE','Für jeden','Alles was man so braucht','Nächtliche Backups','Support im öffentlichen Forum','Immer wieder Aktualisierungen auf die aktuelle Version','Zugriff über automatisch vergebene URL'),
	(2,1,1,'EUR',5,7,'Mini','DE','Für Anfänger','Nur zum Ausprobieren','Nächtliche Backups','Support im öffentlichen Forum','Immer wieder Aktualisierungen auf die aktuelle Version','Zugriff über automatisch vergebene URL'),
	(3,1,12,'EUR',300,14,'Pro','DE','Für Profis','Mit allem Schnickschnack','Stündliche Backups','Support über Ticket-System, mit 3 Std. inkl.','Aktualisierungen mit Ihnen abgesprochen','Zugriff über eigene URL'),
	(4,1,12,'EUR',50,14,'Basic','EN','For everyone','Everything you need','Nightly Backups','Support in the public forum','Regular Updates to latest release','Access via automatic url'),
	(5,1,1,'EUR',5,7,'Mini','EN','For starters','Just experimenting','Nightly Backups','Support in the public forum','Regular Updates to latest release','Access via automatic url'),
	(6,1,12,'EUR',300,14,'Pro','EN','For Professionals','With all bells and whistles','Hourly Backups','Support with Ticketing system, 3 hours incl.','Updates coordinated with you','Access via your own url');
INSERT INTO "saas_customer" ("id","user_id","newsletter","newsletter_subscribed_on","newsletter_cancelled","language_code","verified","verification_token","verification_until","organisation_name","first_name","last_name","street","number","post_code","city","country_code","email_address","is_active") VALUES
	(1,2,1,'2021-01-01',0,'DE',1,'',NULL,'Kaninchenzüchter Plauen e.V.','Hans','Müller','Holzweg','3','01234','Plauen','DE','hans.mueller@example.org',1),
	(2,3,1,'2021-05-01',0,'DE',1,'',NULL,'Gartensparte zum Spaten','Werner','Schmidt','Am Wasser','7','01234','Plauen','DE','werner@example.org',1),
	(3,4,1,'2021-05-01',0,'DE',1,'',NULL,'Gartensparte Schneckenhain','Bernd','Schmitz','Am Berg','2','01234','Plauen','DE','bernd.s@example.org',1),
	(4,5,1,'2021-05-01',0,'DE',1,'',NULL,'Sportverein Trimm Dich','Gunter','Meier','An der Elster','22','01234','Plauen','DE','gunter.meier@example.org',1);
INSERT INTO "saas_instance" ("id","product_id","identifier","hostname","status","auto_renew","last_interaction","reserved_token","reserved_until","reserved_for_user_id","initial_password","db_password","port") VALUES
	(1,1,'344567','host0001','active',1,NULL,NULL,NULL,NULL,'','topsecret',2000),
	(2,1,'238978','host0001','active',1,NULL,NULL,NULL,NULL,'','topsecret',2001),
	(3,1,'785275','host0001','active',1,NULL,NULL,NULL,NULL,'','topsecret',2002),
	(4,1,'862344','host0001','free',1,NULL,NULL,NULL,NULL,'','topsecret',2003),
	(5,1,'119287','host0002','active',1,NULL,NULL,NULL,NULL,'','topsecret',2000),
	(6,1,'239399','host0002','free',1,NULL,NULL,NULL,NULL,'','topsecret',2001);
INSERT INTO "saas_contract" ("id","start_date","end_date","auto_renew","customer_id","instance_id","plan_id") VALUES
	(1,'2021-06-05',NULL,1,1,1,2),
	(2,'2021-06-01',NULL,1,2,2,1),
	(3,'2021-06-01',NULL,1,3,3,1),
	(4,'2021-06-01',NULL,1,4,5,1);
