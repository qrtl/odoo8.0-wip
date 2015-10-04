

class Application(http.Controller):
    @http.route('/page/application2/', auth='public')
    def index(self, **kw):
        return http.request.render('crm_lead_aadjust.application_z0925')
        