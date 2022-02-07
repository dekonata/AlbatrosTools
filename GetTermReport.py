from asutils.webutils import  AdminWebsite  # noqa: E271


admindriver = AdminWebsite('Kriegler', 'Ludium99')
admindriver.create_term_availibilty_report('01-11-2021', '30-11-2021', './files/90_percent_clubs.csv')
