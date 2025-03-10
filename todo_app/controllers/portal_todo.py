from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
class PortalTodo(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        values['todos_count'] = 100
        return values
    
    @http.route(['/my/todo'], type='http', auth="user", website=True)
    def portal_my_todo(self, **kwargs):
        user_todos = request.env['todo_app.todo_app'].sudo().search([('user_id', '=', request.env.user.id)])
        return request.render("todo_app.portal_todo_list", {'todos': user_todos})

#     # @http.route(['/my/todo/<int:task_id>'], type='http', auth="user", website=True)
#     # def portal_todo_detail(self, task_id, **kwargs):
#     #     task = request.env['todo.task'].sudo().browse(task_id)
#     #     return request.render("todo_app.portal_todo_detail", {'task': task})
