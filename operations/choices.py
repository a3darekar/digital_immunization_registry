Vaccinations = (
	(0, (
		#	at birth
			('bcg', 		'BCG'),
			('opv', 		'OPV 0'),
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

Gender = (
	('male', 'Male'),
	('female', 'Female'),
)

Vaccine_Status = (
	('pending', 'Pending'),
	('scheduled', 'Scheduled'),
	('administered', 'Administered'),
)

vaccine_record_status = (
	('cancelled', 'Cancelled'),
	('scheduled', 'Scheduled'),
	('administered', 'Administered'),
)

Appointment_status = (
	('completed', 'Completed'),
	('scheduled', 'Scheduled'),
	('partial', 'Partially Completed'),
	('cancelled', 'Cancelled')
)

BloodGroup = (
	('a_positive', 'A Positive'),
	('a_negative', 'A Negative'),
	('b_positive', 'B Positive'),
	('b_negative', 'B Negative'),
	('o_positive', 'O Positive'),
	('o_negative', 'O Negative'),
	('ab_positive', 'AB Positive'),
	('ab_negative', 'AB Negative'),
)


Vaccine_names = (
	
#	at birth
	('bcg', 		'BCG'),
	('opv', 		'OPV0'),
	('hepb1',		'HEP-B 1'),

#	6 weeks
	('dt1',			'DTwP 1'),
	('ipv1',		'IPV 1'),
	('hepb2',		'HEP-B 2'),
	('hib1',		'HIB 1'),
	('rota1',		'Rotavirus 1'),
	('pcv1',		'PCV 1'),
# 10
	('dt2',			'DTwP 2'),
	('ipv2',		'IPV 2'),
	('hib2',		'HIB 2'),
	('rota2',		'Rotavirus 2'),
	('pcv2',		'PCV 2'),
# 14
	('dt3',			'DTwP 3'),
	('ipv3',		'IPV 3'),
	('hib3',		'HIB 3'),
	('rota3',		'Rotavirus 3'),
	('pcv3',		'PCV 3'),
# 24
	('opv1',		'OPV 1'),
	('hepb3',		'HEP-B 3'),
# 36
	('opv2',		'OPV 2'),
	('mmr1',		'MMR-1'),
)

NotificationType = (
	('info', 'info'),
	('success', 'success'),
	('error', 'error'),
	('danger', 'danger'),
)