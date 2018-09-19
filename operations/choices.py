Vaccines = (
	(0, (
		#	at birth
			('bcg', 		'BCG'),
			('opv', 		'OPV0'),
			('hepb1',		'HEP-B 1'),
		),
	),
	
	(6, (
		#	6 weeks
			('dt1',			'DTwP 1'),
			('ipv1',		'IPV 1'),
			('hepb2',		'HEP-B 2'),
			('hib1',		'HIB 1'),
			('rota1',		'Rotavirus 1'),
			('pcv1',		'PCV 1'),
		),
	),

	(10, (
			('dt2',			'DTwP 2'),
			('ipv2',		'IPV 2'),
			('hib2',		'HIB 2'),
			('rota2',		'Rotavirus 2'),
			('pcv2',		'PCV 2'),
		),
	),

	(14, (
			('dt3',			'DTwP 3'),
			('ipv3',		'IPV 3'),
			('hib3',		'HIB 3'),
			('rota3',		'Rotavirus 3'),
			('pcv3',		'PCV 3'),
		),
	),

	(24, (
			('opv1',		'OPV 1'),
			('hepb3',		'HEP-B 3'),
		),
	),

	(36, (
			('opv2',		'OPV 2'),
			('mmr1',		'MMR-1'),
		),
	),
)

gender = (
	('male', 'Male'),
	('female', 'Female'),
)

Vaccine_status = (
	('pending', 'Pending'),
	('scheduled', 'Scheduled'),
	('administered', 'Administered'),
)

Blood_Group = (
	('a_positive', 'A Positive'),
	('a_negative', 'A Negative'),
	
	('b_positive', 'B Positive'),
	('b_negative', 'B Negative'),
	
	('o_positive', 'O Positive'),
	('o_negative', 'O Negative'),
	
	('ab_positive', 'AB positive'),
	('abnegative', 'AB negative'),
)