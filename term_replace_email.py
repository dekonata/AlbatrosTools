from asutils.webutils import  Adminwebsite


admindriver = AdminWebsite('Kriegler', 'Ludium99')
admindriver.create_term_availibilty_report('01-01-2021', '31-01-2021', 'test.csv')