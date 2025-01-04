app_name = "over_time"
app_title = "Over Time"
app_publisher = "Safdar Ali"
app_description = "this app to calcualte employee over time"
app_email = "safdar211@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------
doctype_js = {"Shift Type": "public/js/shift_type.js"}
# include js, css files in header of desk.html
# app_include_css = "/assets/over_time/css/over_time.css"
# app_include_js = "/assets/over_time/js/over_time.js"

# include js, css files in header of web template
# web_include_css = "/assets/over_time/css/over_time.css"
# web_include_js = "/assets/over_time/js/over_time.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "over_time/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "over_time/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "over_time.utils.jinja_methods",
# 	"filters": "over_time.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "over_time.install.before_install"
# after_install = "over_time.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "over_time.uninstall.before_uninstall"
# after_uninstall = "over_time.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "over_time.utils.before_app_install"
# after_app_install = "over_time.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "over_time.utils.before_app_uninstall"
# after_app_uninstall = "over_time.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "over_time.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "Timesheet": {
        "before_submit": "over_time.events.add_up_over_time.submit",
        "on_cancel": "over_time.events.add_up_over_time.cancel",
    }

}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"over_time.tasks.all"
# 	],
# 	"daily": [
# 		"over_time.tasks.daily"
# 	],
# 	"hourly": [
# 		"over_time.tasks.hourly"
# 	],
# 	"weekly": [
# 		"over_time.tasks.weekly"
# 	],
# 	"monthly": [
# 		"over_time.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "over_time.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "over_time.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "over_time.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["over_time.utils.before_request"]
# after_request = ["over_time.utils.after_request"]

# Job Events
# ----------
# before_job = ["over_time.utils.before_job"]
# after_job = ["over_time.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"over_time.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

required_apps = ["hrms"]
