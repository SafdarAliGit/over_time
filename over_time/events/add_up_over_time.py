import frappe


def submit(self, method):
    employee = frappe.get_doc("Employee", self.employee)
    employee.custom_over_time = self.custom_over_time if self.custom_over_time else 0
    employee.save()

def cancel(self, method):
    employee = frappe.get_doc("Employee", self.employee)
    employee.custom_over_time = 0
    employee.save()